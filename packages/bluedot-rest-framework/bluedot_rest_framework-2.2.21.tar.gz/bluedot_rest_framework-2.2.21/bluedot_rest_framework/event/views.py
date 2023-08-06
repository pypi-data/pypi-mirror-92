
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, AllView
from bluedot_rest_framework.utils.func import get_tree
from bluedot_rest_framework.utils.area import area
from .live.views import LiveView
from .frontend_views import FrontendView

Event = import_string('event.models')
EventSerializer = import_string('event.serializers')
EventRegister = import_string('event.register.models')


class EventView(CustomModelViewSet, FrontendView, LiveView, AllView):
    model_class = Event
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filterset_fields = {
        'event_type': {
            'field_type': 'int',
            'lookup_expr': ''
        },
        'time_state': {
            'start_time': 'start_time',
            'end_time': 'end_time'
        },
        'title': {
            'field_type': 'string',
            'lookup_expr': '__icontains'
        },
        'extend_is_banner': {
            'field_type': 'bool',
            'lookup_expr': ''
        },
        'extend_is_index': {
            'field_type': 'bool',
            'lookup_expr': ''
        },
        'extend_category_id': {
            'field_type': 'int',
            'lookup_expr': ''
        },
    }

    @action(detail=False, methods=['get'], url_path='area', url_name='area')
    def area(self, request, *args, **kwargs):
        return Response(area)
