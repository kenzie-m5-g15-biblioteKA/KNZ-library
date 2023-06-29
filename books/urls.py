from django.urls import path
from .views import BookView, BookDetailView


urlpatterns = [
    path("books/", BookView.as_view()),
    path("books/<int:pk>/", BookDetailView.as_view()),
]
