from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractEventConfiguration(AbstractRelationTime):

    event_id = models.IntegerField()
    value = models.JSONField()

    class Meta:
        abstract = True


class EventConfiguration(AbstractEventConfiguration):

    class Meta:
        db_table = 'event_configuration'
