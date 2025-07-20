from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from .models import CustomUser
from .serializers import UserSerializer


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CreateUserView(generics.CreateAPIView):
    """
    View to create a new user.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    View to retrieve or update the authenticated user's data.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retrieve and return the authenticated user.
        """
        return self.request.user
