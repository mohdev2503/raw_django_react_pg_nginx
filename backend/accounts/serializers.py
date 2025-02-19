# serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers


user_model = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = user_model
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Create the user and hash their password
        user = user_model.objects.create_user(**validated_data)
        return user


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add additional user data to the response
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['full_name'] = f"{self.user.first_name} {self.user.last_name}"

        # Include any other fields you want
        if hasattr(self.user, 'profile'):
            data['profile_image'] = self.user.profile.profile_image.url if self.user.profile.profile_image else None

        return data
