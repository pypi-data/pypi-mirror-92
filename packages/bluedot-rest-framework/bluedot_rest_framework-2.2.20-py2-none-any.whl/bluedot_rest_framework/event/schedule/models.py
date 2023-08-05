from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractEventSchedule(AbstractRelationTime):
    event_id = models.IntegerField()

    project_title = models.CharField(max_length=255, verbose_name='项目名称')
    topic_title = models.CharField(max_length=255, verbose_name='互动话题名称')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    sort = models.IntegerField(default=0)

    speaker_ids = models.JSONField(null=True)

    class Meta:
        abstract = True


class EventSchedule(AbstractEventSchedule):

    class Meta:
        db_table = 'event_schedule'
