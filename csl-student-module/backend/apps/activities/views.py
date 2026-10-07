from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.users.models import User, StudentProfile
from .models import Activity
from .serializers import StudentActivityListSerializer, StudentActivityDetailSerializer


class StudentActivitiesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != User.Role.STUDENT:
            return Response(
                {"detail": "Only students can access activities."},
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
            return Response({"activities": []}, status=status.HTTP_200_OK)

        # Activities applicable to student:
        # Same course, is_active=True, status!=DRAFT,
        # and batch is either NULL (course-wide) or matches student's batch.
        batch_filter = Q(batch__isnull=True)
        if profile.batch:
            batch_filter = batch_filter | Q(batch=profile.batch)

        activities = (
            Activity.objects.filter(
                course=profile.course,
                is_active=True,
                status=Activity.Status.ACTIVE,
            )
            .filter(batch_filter)
            .select_related("course", "batch")
            .order_by("deadline", "-created_at")
        )

        serializer = StudentActivityListSerializer(
            activities,
            many=True,
            context={"student_profile": profile},
        )
        return Response({"activities": serializer.data}, status=status.HTTP_200_OK)


class StudentActivityDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        if user.role != User.Role.STUDENT:
            return Response(
                {"detail": "Only students can access activities."},
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
                {"detail": "Activity not found or not accessible."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check accessibility
        batch_filter = Q(batch__isnull=True)
        if profile.batch:
            batch_filter = batch_filter | Q(batch=profile.batch)

        try:
            activity = (
                Activity.objects.filter(
                    id=pk,
                    course=profile.course,
                    is_active=True,
                    status=Activity.Status.ACTIVE,
                )
                .filter(batch_filter)
                .select_related("course", "batch")
                .get()
            )
        except Activity.DoesNotExist:
            return Response(
                {"detail": "Activity not found or not accessible."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = StudentActivityDetailSerializer(
            activity,
            context={"student_profile": profile},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
