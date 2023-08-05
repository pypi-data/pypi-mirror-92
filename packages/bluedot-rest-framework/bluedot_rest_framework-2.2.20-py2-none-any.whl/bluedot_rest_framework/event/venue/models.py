from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class EventVenue(AbstractRelationTime):
    event_id = models.IntegerField()
    image_list = models.JSONField()

    class Meta:
        db_table = 'event_venue'
