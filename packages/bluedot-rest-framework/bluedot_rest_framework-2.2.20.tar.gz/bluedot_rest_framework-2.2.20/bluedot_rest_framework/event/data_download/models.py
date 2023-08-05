from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractEventDataDownload(AbstractRelationTime):
    event_id = models.IntegerField()
    title = models.CharField(max_length=32, default='')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    data = models.JSONField()

    class Meta:
        abstract = True


class EventDataDownload(AbstractEventDataDownload):

    class Meta:
        db_table = 'event_data_download'
