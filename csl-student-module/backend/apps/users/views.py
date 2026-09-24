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
