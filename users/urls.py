from django.urls import path
from .views import UserDetailView, UserView, UserLendingView, UserDeleteView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/<int:pk>/delete/", UserDeleteView.as_view()),
    path("users/<int:pk>/", UserDetailView.as_view()),
    path("users/<int:pk>/lending/", UserLendingView.as_view()),
    path("users/login/", jwt_views.TokenObtainPairView.as_view()),
]
