from django.contrib.auth import authenticate, login
from rest_framework import generics, status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models.user import UserProfile
from app.serializers.user_serializer import UserProfileSerializer, UserRegistrationSerializer, \
    UserLoginSerializer, UserSerializer
from app.utility import error_detail_to_error_list


class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"detail": "Registration not allowed for authenticated users."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRegistrationSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        except serializers.ValidationError as validation_error:

            return Response({"detail": error_detail_to_error_list(validation_error)},
                            status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(user)
        token, created = Token.objects.get_or_create(user=user)
        data = user_serializer.data
        data["token"] = token.key

        return Response(data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                user_serializer = UserSerializer(user)
                token, created = Token.objects.get_or_create(user=user)
                data = user_serializer.data
                data["token"] = token.key

                return Response(data, status=status.HTTP_200_OK)

            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
