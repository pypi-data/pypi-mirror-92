from bluedot_rest_framework.utils.models import models, AbstractRelationUser, AbstractRelationTime


class AbstractEventChat(AbstractRelationUser, AbstractRelationTime):
    event_id = models.IntegerField()

    nick_name = models.CharField(max_length=100)
    avatar_url = models.CharField(max_length=255)

    state = models.IntegerField(default=0)
    data = models.TextField()

    class Meta:
        abstract = True


class EventChat(AbstractEventChat):
    class Meta:
        db_table = 'event_chat'
