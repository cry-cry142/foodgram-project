from django.contrib.auth.hashers import make_password, check_password
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import User
from .serializers import (
    UserSerializer, AuthenticationUserSerializer, ChangePasswordSerializer
)


class UserViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        password = make_password(
            serializer.validated_data['password']
        )
        serializer.save(
            password=password
        )

    def get_permissions(self):
        if self.detail:
            self.permission_classes = (permissions.IsAuthenticated,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return AuthenticationUserSerializer
        return self.serializer_class

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        serializer = AuthenticationUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['POST'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def set_password(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data
        )
        user = request.user
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(
            serializer.validated_data['current_password'],
            user.password
        ):
            return Response(
                {'current_password': 'Пароль не верен.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.password = make_password(
            serializer.validated_data['new_password']
        )
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
