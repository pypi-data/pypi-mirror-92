from django.db import models
from bluedot_rest_framework.question.abstract_models import AbstractQuestion, AbstractQuestionUser


class EventVote(AbstractQuestion):
    event_id = models.IntegerField(verbose_name='活动id')
    schedule_id = models.IntegerField(verbose_name='日程id')
    state = models.IntegerField(default=0, verbose_name='状态')

    class Meta:
        db_table = 'event_vote'


class EventVoteUser(AbstractQuestionUser):
    schedule_id = models.IntegerField(default=0, verbose_name='日程id')

    class Meta:
        db_table = 'event_vote_user'
