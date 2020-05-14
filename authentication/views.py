from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .renderers import UserJSONRenderer
from .serializers import (LoginSerializer, RegistrationSerializer,
                          UserRetriveUpdateSerializer)
from .permission import IsAdminUser, IsLoggedInUserOrAdmin, IsAdminOrAnonymousUser


class RegistrationAPIView(generics.GenericAPIView):
    # permission_classes = [IsAdminOrAnonymousUser]
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.request == 'create':
    #         permission_classes = [IsAdminUser]
    #     elif self.request == 'list':
    #         permission_classes = [IsAdminOrAnonymousUser]
    #     elif self.request == 'retrieve' or self.request == 'update' or self.request == 'partial_update':
    #         permission_classes = [IsLoggedInUserOrAdmin]
    #     elif self.request == 'destroy':
    #         permission_classes = [IsLoggedInUserOrAdmin]
    #     return [permission() for permission in permission_classes]

    def post(self, request):
        """
        Handle user registration
        """
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        data = serializer.data

        return_message = {'message': 'user successfull added'}
        return Response(return_message, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Get a list of all users
        """
        users = User.objects.all().order_by('id')
        serializer = self.serializer_class(
            users,
            many=True
        )
        response = ({
            "users": serializer.data,
            "count": len(serializer.data)
        })
        return Response(response)

    def delete(self, request, id, **kwargs):
        """Delete a specific user"""

        try:
            user = User.objects.get(id=id)
            staff = request.user
            if staff == user:
                return Response({"errors":
                                 "You cannot delete yourself from the system"},
                                status.HTTP_403_FORBIDDEN)
            else:
                user.delete()
            return Response({"message":
                             "User {} deleted successfully".format(user)},
                            status.HTTP_200_OK)

        except:
            return Response({"message": "Could not find that user"},
                            status.HTTP_404_NOT_FOUND)


class LoginAPIView(generics.CreateAPIView):

    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Handle user login
        """
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    Class that handles retrieving and updating user info
    """
    permission_classes = (IsAdminUser,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserRetriveUpdateSerializer

    # def get(self, request, *args, **kwargs):
    #     """
    #     retrieve user details from the token provided
    #     """
    #     serializer = self.serializer_class(request.user)

    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, id, **kwargs):
        """
        Get one user
        """
        user = User.objects.get(id=id)
        serializer = self.serializer_class(user)
        response = ({
            "users": serializer.data
        })
        return Response(response)

    def patch(self, request, id):
        try:
            user = User.objects.get(id=id)
        except Exception:
            return Response({'message': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUserProfile(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    Class that handles retrieving and updating user info
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserRetriveUpdateSerializer

    def get(self, request, *args, **kwargs):
        """
        retrieve user details from the token provided
        """
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
