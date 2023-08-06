from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractEventConfiguration(AbstractRelationTime):

    event_id = models.IntegerField(verbose_name='活动id')
    value = models.JSONField(verbose_name='内容')

    class Meta:
        abstract = True


class EventConfiguration(AbstractEventConfiguration):

    class Meta:
        db_table = 'event_configuration'
