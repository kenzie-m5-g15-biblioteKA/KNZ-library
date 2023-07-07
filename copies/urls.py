from django.urls import path
from .views import CopyView, CopyDetailView, CreateCopyView

urlpatterns = [
    path("copies/", CopyView.as_view()),
    path("books/<int:pk>/copies", CreateCopyView.as_view()),
    path("copies/<int:pk>/", CopyDetailView.as_view()),
]
