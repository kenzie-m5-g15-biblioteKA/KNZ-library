from django.urls import path
from assessments.views import ListAssessmentsView, AssessmentsDetailView


urlpatterns = [
    path("assessments/", ListAssessmentsView.as_view()),
    path("assessments/<int:pk>/", AssessmentsDetailView.as_view()),
]
