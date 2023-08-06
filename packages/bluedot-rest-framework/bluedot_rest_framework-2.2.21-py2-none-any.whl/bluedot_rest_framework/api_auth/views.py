from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, TreeAPIView, AllView
from .serializers import AuthUserSerializer, AuthMenuSerializer, AuthGroupSerializer
from .models import AuthGroup, AuthMenu, AuthUser
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from bluedot_rest_framework.utils.func import get_tree, get_tree_menu


class AuthUserViewSet(CustomModelViewSet):
    model_class = AuthUser
    serializer_class = AuthUserSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        return self.model_class.objects.create_user(**request.data)

    @action(detail=False, methods=['get'], url_path='current', url_name='current')
    def current(self, request, *args, **kwargs):
        user = AuthUserSerializer(request.user, context={
            'request': request}).data
        return Response(user)


class AuthGroupViewSet(CustomModelViewSet, AllView):
    model_class = AuthGroup
    serializer_class = AuthGroupSerializer

    permission_classes = [IsAdminUser]


class MenuViewSet(CustomModelViewSet, TreeAPIView):
    model_class = AuthMenu
    serializer_class = AuthMenuSerializer

    @action(detail=False, methods=['get'], url_path='current', url_name='current')
    def current(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.model_class.objects.filter(
                is_menu=1).order_by('-sort')
        else:
            user = AuthUserSerializer(request.user, context={
                                      'request': request}).data
            queryset = AuthGroup.objects.filter(
                pk__in=user['group_ids']).distinct('menu_ids')

        serializer = self.get_serializer(queryset, many=True)

        before_menu = serializer.data
        data = []
        for item in before_menu:
            data.append(item)
            if item['parent'] and get_tree_menu(data, item['parent']):
                queryset = self.model_class.objects.get(pk=item['parent'])
                data.append(self.get_serializer(queryset).data)
        data = get_tree(data, None)
        return Response(data)
