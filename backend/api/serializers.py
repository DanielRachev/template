from .models import CustomUser
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    """
    Serializer for the CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "last_name", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Create and return a new user with an encrypted password.
        """
        user = CustomUser.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        return user
