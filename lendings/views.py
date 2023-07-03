from rest_framework import generics

from .models import Lending
from .serializers import LendingSerializer

# from rest_framework_simplejwt.authentication import JWTAuthentication


class LendingView(generics.ListCreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = []

    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

    def perform_create(self, serializer: LendingSerializer):
        return_date = serializer.instance.get_return_date()
        serializer.save(return_date=return_date, user=self.request.user)
