from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractEventSpeaker(AbstractRelationTime):
    event_id = models.IntegerField()
    name = models.CharField(max_length=255)
    jobs = models.CharField(max_length=255)
    description = models.TextField()
    img = models.CharField(max_length=255)
    is_sign_page = models.BooleanField(default=False)
    sort = models.IntegerField(default=1)

    class Meta:
        abstract = True


class EventSpeaker(AbstractEventSpeaker):

    class Meta:
        db_table = 'event_speaker'
