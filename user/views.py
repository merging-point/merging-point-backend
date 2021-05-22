from django.http.request import HttpRequest
from user.serializers import UserSerializer
from rest_framework import permissions, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializerDocument
from drf_yasg.utils import swagger_auto_schema


class UserView(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserSerializer
    lookup_field = 'username'

    @swagger_auto_schema(responses={
        201: UserSerializerDocument,
        400: "Bad Request",
    })
    @action(detail=False, methods=['post'])
    def register(self, request: HttpRequest, *args, **kwargs):
        serializer: UserSerializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={
        200: UserSerializerDocument,
        401: "Unauthorized"
    })
    @action(detail=False, methods=['get'])
    def me(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer: UserSerializer = self.get_serializer(request.user)
        return Response(serializer.data)