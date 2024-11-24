from django.contrib.auth.models import User
from rest_framework import serializers

from ..models.user import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="userprofile.id")
    fullname = serializers.CharField(source="userprofile.fullname", read_only=True)
    position = serializers.CharField(source="userprofile.position", read_only=True)
    avatar = serializers.CharField(source="userprofile.avatar", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "fullname", "position", "avatar"]


class UserRegistrationSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    username = serializers.EmailField()
    fullname = serializers.CharField(max_length=255)
    position = serializers.CharField(max_length=50)
    avatar = serializers.CharField(max_length=100)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )
        UserProfile.objects.create(user=user, fullname=validated_data["fullname"],
                                   position=validated_data["position"],
                                   avatar=validated_data["avatar"])
        return user

    def update(self, instance, validated_data):
        pass


class UserLoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserProfileInfoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.username")

    class Meta:
        model = UserProfile
        fields = ["id", "fullname", "avatar", "position", "email"]
