from django.contrib.auth import authenticate, login, logout

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import get_object_or_404, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Profile, User


from .serializers import (UserLoginSerializer,
                          UserCreateSerializer,
                          ProfileSerializer,
                          UserPasswordChangeSerializer)
from .permissions import IsSelf


class UserLoginAPIView(APIView):

    def get(self, request):
        serializer = UserLoginSerializer()
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            username = request.data['username']
            password = request.data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                user_token = get_object_or_404(Token.objects.all(), user=user)
                response_data = serializer.data

                # send authentication token in response
                response_data['token'] = user_token.key

                # send user profile id in response.
                response_data['id'] = user.profile.id

                return Response(data=response_data,
                                status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserPasswordChangeAPIView(APIView):
    permission_classes = (IsAuthenticated, IsSelf)

    def post(self, request):
        serializer = UserPasswordChangeSerializer(data=request.data,
                                                  context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
