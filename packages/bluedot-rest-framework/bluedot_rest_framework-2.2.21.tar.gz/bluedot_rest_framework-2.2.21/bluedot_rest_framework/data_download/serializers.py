from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.serializers import CustomSerializer

DataDownload = import_string('data_download.models')
DataDownloadUser = import_string('data_download.user_models')


class DataDownloadSerializer(CustomSerializer):

    class Meta:
        model = DataDownload
        fields = '__all__'


class DataDownloadUserSerializer(CustomSerializer):

    class Meta:
        model = DataDownloadUser
        fields = '__all__'
