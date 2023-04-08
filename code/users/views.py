from rest_framework import viewsets, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from . import serializers, services
from utils import mixins
from drf_yasg.utils import swagger_auto_schema


class UserViewSet(viewsets.ViewSet, mixins.ActionPermissionMixin):
    user_services: services.UserServicesInterface = services.UserServicesV1()

    @swagger_auto_schema(request_body=serializers.CreateUserSerializer)
    def create_user(self, request, *args, **kwargs):
        serializer = serializers.CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session_id = self.user_services.create_user(serializer.validated_data)
        return Response(session_id)

    @swagger_auto_schema(request_body=serializers.VerifyUserSerializer)
    def verify_user(self, request, *args, **kwargs):
        serializer = serializers.VerifyUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.user_services.verify_user(data=serializer.validated_data)
        return Response({'message': 'User has been created successfully'}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=serializers.CreateTokenSerializer)
    def create_token(self, request, *args, **kwargs):
        serializer = serializers.CreateTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = self.user_services.create_token(data=serializer.validated_data)
        return Response(tokens)

    @swagger_auto_schema(request_body=serializers.UpdatePasswordSerializer)
    def update_password(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        serializer = serializers.UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['phone_number'] = request.user.phone_number

        session_id = self.user_services.update_password(data=serializer.validated_data)
        return Response(session_id)

    @swagger_auto_schema(request_body=serializers.VerifyUserSerializer)
    def verify_update_password(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise NotAuthenticated()

        serializer = serializers.VerifyUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.user_services.verify_update_password(data=serializer.validated_data)
        return Response({'message': 'Password has been successfully changed'}, status=status.HTTP_200_OK)

    def get_user_info(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise NotAuthenticated()

        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=serializers.UpdatePersonalInfoSerializer)
    def update_personal_info(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise NotAuthenticated()

        serializer = serializers.UpdatePersonalInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['phone_number'] = request.user.phone_number

        self.user_services.update_personal_info(serializer.validated_data)
        return Response({'message': 'Personal information has been successfully updated'}, status=status.HTTP_200_OK)
