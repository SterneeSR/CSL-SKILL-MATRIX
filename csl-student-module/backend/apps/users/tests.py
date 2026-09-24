from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.courses.models import Course, Batch
from apps.users.models import StudentProfile

User = get_user_model()


class StudentProfileAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student_user = User.objects.create_user(
            username="student1@example.com",
            email="student1@example.com",
            password="testpassword123",
            first_name="Alice",
            last_name="Smith",
            role=User.Role.STUDENT,
            status=User.AccountStatus.ACTIVE,
        )
        self.tutor_user = User.objects.create_user(
            username="tutor1@example.com",
            email="tutor1@example.com",
            password="testpassword123",
            first_name="Bob",
            role=User.Role.TUTOR,
            status=User.AccountStatus.ACTIVE,
        )

    def test_unauthenticated_request_fails(self):
        response = self.client.get("/api/student/profile/")
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_student_profile_without_course_and_batch(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get("/api/student/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["name"], "Alice Smith")
        self.assertEqual(data["email"], "student1@example.com")
        self.assertIn("CSL", data["student_id"])
        self.assertIsNone(data["course"])
        self.assertIsNone(data["batch"])
        # Ensure password or internal credentials are NOT exposed
        self.assertNotIn("password", data)
        self.assertNotIn("role", data)
        self.assertNotIn("status", data)

    def test_student_profile_with_course_and_batch(self):
        course = Course.objects.create(name="Full Stack Dev", code="FSD101")
        batch = Batch.objects.create(course=course, name="Batch 2026-A", start_date="2026-01-01")
        profile = StudentProfile.objects.create(
            user=self.student_user,
            registration_number="CSL2026001",
            first_name="Alice",
            last_name="Smith",
            course=course,
            batch=batch,
        )

        self.client.force_authenticate(user=self.student_user)
        response = self.client.get("/api/student/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["student_id"], "CSL2026001")
        self.assertEqual(data["course"], "Full Stack Dev")
        self.assertEqual(data["batch"], "Batch 2026-A")

    def test_non_student_cannot_access_student_profile(self):
        self.client.force_authenticate(user=self.tutor_user)
        response = self.client.get("/api/student/profile/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
