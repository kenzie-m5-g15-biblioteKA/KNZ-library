from django.urls import path
from assessments.views import CreateAssessmentsView
from .views import BookView, BookDetailView, BookFollowView, BookUnfollowView


urlpatterns = [
    path("books/", BookView.as_view()),
    path("books/<int:pk>/", BookDetailView.as_view()),
    path("users/follow/<int:pk>/", BookFollowView.as_view()),
    path("users/unfollow/<int:pk>/", BookUnfollowView.as_view()),
    path("books/<int:pk>/assessments/", CreateAssessmentsView.as_view()),
]
