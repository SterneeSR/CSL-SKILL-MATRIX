from datetime import datetime, timedelta, timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.courses.models import Course, Batch
from apps.skills.models import SkillCategory, Skill, SubSkill
from apps.users.models import StudentProfile
from .models import Activity, Task, Assessment, TaskSkill

User = get_user_model()


class StudentActivitiesAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Admin / Tutor
        self.tutor = User.objects.create_user(
            username="tutor_act@example.com",
            email="tutor_act@example.com",
            password="testpassword123",
            first_name="Prof",
            role=User.Role.TUTOR,
            status=User.AccountStatus.ACTIVE,
        )

        # Student A
        self.student_a = User.objects.create_user(
            username="student_a@example.com",
            email="student_a@example.com",
            password="testpassword123",
            first_name="Alice",
            last_name="A",
            role=User.Role.STUDENT,
            status=User.AccountStatus.ACTIVE,
        )
        # Student B
        self.student_b = User.objects.create_user(
            username="student_b@example.com",
            email="student_b@example.com",
            password="testpassword123",
            first_name="Bob",
            last_name="B",
            role=User.Role.STUDENT,
            status=User.AccountStatus.ACTIVE,
        )

        # Courses and Batches
        self.course_1 = Course.objects.create(name="Computer Science", code="CS101")
        self.course_2 = Course.objects.create(name="Data Science", code="DS101")

        self.batch_1 = Batch.objects.create(course=self.course_1, name="2026-A", start_date="2026-01-01")
        self.batch_2 = Batch.objects.create(course=self.course_1, name="2026-B", start_date="2026-01-01")

        # Assign Student A to Course 1, Batch 1
        self.profile_a = StudentProfile.objects.create(
            user=self.student_a,
            registration_number="CSL0001",
            first_name="Alice",
            last_name="A",
            course=self.course_1,
            batch=self.batch_1,
        )

        # Student B is in Course 2 (or unassigned batch)
        self.profile_b = StudentProfile.objects.create(
            user=self.student_b,
            registration_number="CSL0002",
            first_name="Bob",
            last_name="B",
            course=self.course_2,
            batch=None,
        )

        # Skills
        self.cat = SkillCategory.objects.create(name="Programming")
        self.skill = Skill.objects.create(category=self.cat, name="Python")
        self.sub = SubSkill.objects.create(skill=self.skill, name="Functions", display_order=1)

        # Activities for Course 1
        # Activity 1: Course-wide (batch=None), Active
        self.act_course_wide = Task.objects.create(
            title="Course-wide Python Task",
            description="Complete the basics",
            course=self.course_1,
            batch=None,
            created_by=self.tutor,
            max_marks=100,
            status=Activity.Status.ACTIVE,
            deadline=datetime.now(timezone.utc) + timedelta(days=7),
        )
        TaskSkill.objects.create(task=self.act_course_wide, skill=self.skill, sub_skill=self.sub)

        # Activity 2: Batch 1 specific, Active
        self.act_batch_1 = Task.objects.create(
            title="Batch 1 Python Task",
            description="For Batch 1 only",
            course=self.course_1,
            batch=self.batch_1,
            created_by=self.tutor,
            max_marks=50,
            status=Activity.Status.ACTIVE,
        )

        # Activity 3: Batch 2 specific, Active
        self.act_batch_2 = Task.objects.create(
            title="Batch 2 Python Task",
            description="For Batch 2 only",
            course=self.course_1,
            batch=self.batch_2,
            created_by=self.tutor,
            max_marks=50,
            status=Activity.Status.ACTIVE,
        )

        # Activity 4: Draft (should not be visible to students)
        self.act_draft = Task.objects.create(
            title="Draft Task",
            description="Under preparation",
            course=self.course_1,
            batch=self.batch_1,
            created_by=self.tutor,
            max_marks=20,
            status=Activity.Status.DRAFT,
        )

        # Activity 5: For Course 2
        self.act_course_2 = Task.objects.create(
            title="Data Science Task",
            description="Course 2 only",
            course=self.course_2,
            batch=None,
            created_by=self.tutor,
            max_marks=100,
            status=Activity.Status.ACTIVE,
        )

    def test_unauthenticated_request_fails(self):
        response = self.client.get("/api/student/activities/")
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_non_student_access_rejected(self):
        self.client.force_authenticate(user=self.tutor)
        response = self.client.get("/api/student/activities/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_activities_list_visibility(self):
        self.client.force_authenticate(user=self.student_a)
        response = self.client.get("/api/student/activities/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("activities", data)
        activity_ids = [act["id"] for act in data["activities"]]

        # Student A should see Course-wide and Batch 1 activities
        self.assertIn(self.act_course_wide.id, activity_ids)
        self.assertIn(self.act_batch_1.id, activity_ids)

        # Student A should NOT see Batch 2, Draft, or Course 2 activities
        self.assertNotIn(self.act_batch_2.id, activity_ids)
        self.assertNotIn(self.act_draft.id, activity_ids)
        self.assertNotIn(self.act_course_2.id, activity_ids)

    def test_empty_activity_list_for_unassigned_student(self):
        unassigned_student = User.objects.create_user(
            username="unassigned@example.com",
            email="unassigned@example.com",
            password="testpassword123",
            role=User.Role.STUDENT,
            status=User.AccountStatus.ACTIVE,
        )
        self.client.force_authenticate(user=unassigned_student)
        response = self.client.get("/api/student/activities/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["activities"], [])

    def test_student_activity_detail_accessible(self):
        self.client.force_authenticate(user=self.student_a)
        response = self.client.get(f"/api/student/activities/{self.act_course_wide.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["id"], self.act_course_wide.id)
        self.assertEqual(data["title"], "Course-wide Python Task")
        self.assertEqual(data["type"], "TASK")
        self.assertEqual(data["course"], "Computer Science")
        self.assertEqual(data["max_marks"], 100)
        self.assertEqual(data["status"], "PENDING")

        # Verify covered skills
        self.assertEqual(len(data["skills_covered"]), 1)
        self.assertEqual(data["skills_covered"][0]["name"], "Python")
        self.assertEqual(data["skills_covered"][0]["subskills"][0]["name"], "Functions")

    def test_student_cannot_access_inaccessible_activity(self):
        # Student A attempts to access Batch 2's activity
        self.client.force_authenticate(user=self.student_a)
        response = self.client.get(f"/api/student/activities/{self.act_batch_2.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Student A attempts to access Course 2's activity
        response2 = self.client.get(f"/api/student/activities/{self.act_course_2.id}/")
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

        # Student A attempts to access Draft activity
        response3 = self.client.get(f"/api/student/activities/{self.act_draft.id}/")
        self.assertEqual(response3.status_code, status.HTTP_404_NOT_FOUND)
