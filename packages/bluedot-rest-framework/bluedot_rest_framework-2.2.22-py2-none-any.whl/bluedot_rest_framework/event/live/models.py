from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractEventLivePPT(AbstractRelationTime):
    event_id = models.IntegerField()

    class Meta:
        abstract = True


class EventLivePPT(AbstractEventLivePPT):
    image_list = models.JSONField(null=True)

    class Meta:
        db_table = 'event_live_ppt'
