from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create, AllView
from bluedot_rest_framework.utils.jwt_token import jwt_create_token_wechat, jwt_get_userinfo_handler


User = import_string('user.models')
UserSerializer = import_string('user.serializers')


class UserView(CustomModelViewSet):
    model_class = User
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        wechat_id, unionid = jwt_get_userinfo_handler(
            self.request.auth)
        serializer.save(unionid=unionid, wechat_id=wechat_id)
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)
