from bluedot_rest_framework.utils.serializers import CustomSerializer
from rest_framework.serializers import SerializerMethodField, CharField
from bluedot_rest_framework import import_string

User = import_string('user.models')


class UserSerializer(CustomSerializer):
    country = CharField(required=False, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
