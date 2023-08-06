from django.db import models
from bluedot_rest_framework.question.abstract_models import AbstractQuestion, AbstractQuestionUser


class EventQuestion(AbstractQuestion):
    event_id = models.CharField(max_length=32)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        db_table = 'event_question'


class EventQuestionUser(AbstractQuestionUser):
    event_id = models.CharField(max_length=32, default='')

    class Meta:
        db_table = 'event_question_user'
