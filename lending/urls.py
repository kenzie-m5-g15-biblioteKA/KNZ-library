from django.urls import path
from .views import (
    LendingView,
    CreateLendingView,
    LendingDetailView,
    DevolutionLendingView,
    updateLendingView,
    DeleteRetriveUpdateLendingView,
)


urlpatterns = [
    path("lending/", LendingView.as_view()),
    path("book/<int:pk>/lending/", CreateLendingView.as_view()),
    path("user/lending/", LendingDetailView.as_view()),
    path("user/lending/<int:pk>/", DevolutionLendingView.as_view()),
    path("lending/update/", updateLendingView.as_view()),
    path("lending/<int:pk>/", DeleteRetriveUpdateLendingView.as_view()),
]
