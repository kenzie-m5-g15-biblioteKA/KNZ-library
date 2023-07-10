from django.urls import path

from lendings import views

urlpatterns = [
    path("lending/history/", views.LendingHistoryView.as_view()),
    path("lending/<int:lending_id>/", views.LendingDetailView.as_view()),
    path("lending/<int:lending_id>/return/", views.LendingReturnView.as_view()),
    path("lending/check_overdue/", views.LendingCheckOverdueView.as_view()),
    path("copies/<int:pk>/lending/", views.LendingCreateView.as_view()),
    path(
        "users/<int:user_id>/lending_history/",
        views.LendingHistoryByUserView.as_view(),
    ),
]
