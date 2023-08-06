import requests
from rest_framework import status
from django.conf import settings
from rest_framework.response import Response
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from rest_framework.decorators import action
from bluedot_rest_framework import import_string
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet
from bluedot_rest_framework.utils.crypto import AESEncrypt
from bluedot_rest_framework.utils.jwt_token import jwt_get_wechatid_handler
from bluedot_rest_framework.event.frontend_views import FrontendView


EventRegister = import_string('event.register.models')
EventDataDownload = import_string('event.data_download.models')
EventDataDownloadSerializer = import_string('event.data_download.serializers')


class EventDataDownloadView(CustomModelViewSet, FrontendView):
    model_class = EventDataDownload
    serializer_class = EventDataDownloadSerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id', None)
        queryset = self.model_class.objects.filter(event_id=event_id).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        queryset = self.model_class.objects.filter(
            event_id=request.data.get('event_id', None)).first()
        if queryset:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(
                queryset, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], url_path='send-email', url_name='send-email')
    def send_email(self, request, *args, **kwargs):
        data_list = request.data["data"]
        wechat_id = jwt_get_wechatid_handler(request.auth)
        email = EventRegister.objects.get(wechat_id=wechat_id).email
        email = AESEncrypt.decrypt(email)
        email = EmailMessage(subject='【下载资料】' + 'title',
                             from_email=settings.EMAIL_HOST_USER, to=[email])
        url_list = [data['url'] for data in data_list]
        # pdf = [requests.get(url).content for url in url_list]

        return Response({"code": "200"})
