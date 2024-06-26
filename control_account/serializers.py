from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class CreateUserSearializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.

    This serializer validates the input data for creating a new user and
    utilizes Django's built-in UserManager for secure password handling.

    Args:
        serializers.ModelSerializer: A subclass of the ModelSerializer in Django REST framework.

    Attributes:
        password2 (serializers.CharField): A field for confirming the password.

    Raises:
        serializers.ValidationError: Raised when passwords do not match or the user already exists.

    Returns:
        User: The newly created user instance.

    Example:
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # Additional logic with the created user.

    """

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']

    extra_kwargs = {
        'password': {'write_only': True}
    }

    def save(self):
        """
        Save method for creating a new user.

        This method validates the password confirmation and checks for existing users
        before creating a new user with the provided data.

        Returns:
            User: The newly created user instance.

        Raises:
            serializers.ValidationError: Raised when passwords do not match or the user already exists.

        """
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'Error': 'Passwords do not match'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'Error': 'User already exists'})

        account = User.objects.create_user(
            email=self.validated_data['email'],
            password=self.validated_data['password'],
            is_active = True,
            is_verified=True,
            is_buyer=True,
        )

        return account

    
    
class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Attributes:
        password (str): The user's password.
    """
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'password']


class ChangePasswordSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        """
        Ensure the passwords match.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self, **kwargs):
        """
        Save method for changing the user's password.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['password'])
        user.save()
        return user

