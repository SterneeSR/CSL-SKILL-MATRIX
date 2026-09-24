from django.urls import path
from .views import StudentProfileView, StudentSkillsView

urlpatterns = [
    path("profile/", StudentProfileView.as_view(), name="student-profile"),
    path("skills/", StudentSkillsView.as_view(), name="student-skills"),
]

