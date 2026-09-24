from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import User, StudentProfile
from .serializers import StudentProfileSerializer


class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != User.Role.STUDENT:
            return Response(
                {"detail": "Only students can access this profile."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Ensure student profile exists for the user
        profile, _ = StudentProfile.objects.get_or_create(
            user=user,
            defaults={
                "registration_number": f"CSL{user.id:04d}",
                "first_name": user.first_name or "Student",
                "last_name": user.last_name or "",
            },
        )

        serializer = StudentProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentSkillsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != User.Role.STUDENT:
            return Response(
                {"detail": "Only students can access skills."},
                status=status.HTTP_403_FORBIDDEN,
            )

        profile, _ = StudentProfile.objects.get_or_create(
            user=user,
            defaults={
                "registration_number": f"CSL{user.id:04d}",
                "first_name": user.first_name or "Student",
                "last_name": user.last_name or "",
            },
        )

        if not profile.course:
            return Response(
                {
                    "course": None,
                    "batch": None,
                    "skills": [],
                },
                status=status.HTTP_200_OK,
            )

        course_data = {
            "id": profile.course.id,
            "name": profile.course.name,
            "code": profile.course.code,
        }
        batch_data = (
            {
                "id": profile.batch.id,
                "name": profile.batch.name,
            }
            if profile.batch
            else None
        )

        course_skills = list(
            profile.course.course_skills.select_related(
                "skill", "skill__category", "sub_skill"
            ).order_by(
                "skill__category__name",
                "skill__name",
                "sub_skill__display_order",
                "sub_skill__id",
            )
        )

        skills_map = {}
        for cs in course_skills:
            sk = cs.skill
            if sk.id not in skills_map:
                skills_map[sk.id] = {
                    "id": sk.id,
                    "name": sk.name,
                    "category": sk.category.name if sk.category else "",
                    "status": "UNASSESSED",
                    "subskills": [],
                }
            if cs.sub_skill is not None:
                skills_map[sk.id]["subskills"].append(
                    {
                        "id": cs.sub_skill.id,
                        "name": cs.sub_skill.name,
                        "status": "UNASSESSED",
                    }
                )

        return Response(
            {
                "course": course_data,
                "batch": batch_data,
                "skills": list(skills_map.values()),
            },
            status=status.HTTP_200_OK,
        )

