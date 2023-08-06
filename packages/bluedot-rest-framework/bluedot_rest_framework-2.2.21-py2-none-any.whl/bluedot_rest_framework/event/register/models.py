from bluedot_rest_framework.utils.models import models, AbstractRelationUser, AbstractRelationTime


class AbstractEventRegister(AbstractRelationUser, AbstractRelationTime):

    event_id = models.CharField(max_length=32)
    event_type = models.IntegerField(default=1)
    source = models.IntegerField(default=0)
    state = models.IntegerField(default=0)

    tel_region = models.CharField(max_length=32, null=True, default='')
    industry = models.CharField(max_length=100, null=True, default='')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        abstract = True


class EventRegister(AbstractEventRegister):
    class Meta:
        db_table = 'event_register'


class EventRegisterConfig(AbstractRelationTime):
    event_id = models.CharField(max_length=32)
    over_time = models.DateTimeField()

    field_list = models.JSONField()

    class Meta:
        db_table = 'event_register_config'
