from django.contrib.auth import get_user_model
from rest_framework import serializers
from bluedot_rest_framework.api_auth.models import AuthMenu, AuthGroup


class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def create(self, validated_data):
        return get_user_model().create_user(**validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('password', None):
            instance.set_password(validated_data.get(
                'password'))

        instance.group_ids = validated_data.get(
            'group_ids', instance.group_ids)
        instance.email = validated_data.get(
            'email', instance.email)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.save()
        return instance


class AuthMenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthMenu
        fields = '__all__'


class AuthGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthGroup
        fields = '__all__'
