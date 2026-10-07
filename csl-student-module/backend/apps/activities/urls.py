from django.urls import path
from .views import StudentActivitiesListView, StudentActivityDetailView

urlpatterns = [
    path("", StudentActivitiesListView.as_view(), name="student-activities-list"),
    path("<int:pk>/", StudentActivityDetailView.as_view(), name="student-activity-detail"),
]
