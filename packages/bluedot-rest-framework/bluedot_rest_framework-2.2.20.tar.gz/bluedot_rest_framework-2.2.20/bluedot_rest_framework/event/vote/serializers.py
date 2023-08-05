from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string
from rest_framework.serializers import CharField, IntegerField

EventVote = import_string('event.vote.models')
EventVoteUser = import_string('event.vote.user_models')


class EventVoteSerializer(CustomSerializer):

    class Meta:
        model = EventVote
        fields = '__all__'


class EventVoteUserSerializer(CustomSerializer):
    user_id = IntegerField(required=False)
    unionid = CharField(required=False)
    openid = CharField(required=False)
    wechat_id = IntegerField(required=False)

    class Meta:
        model = EventVoteUser
        fields = '__all__'
