from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractConfig(AbstractRelationTime):

    config_type = models.IntegerField()
    title = models.CharField(max_length=255)
    value = models.JSONField()

    class Meta:
        abstract = True


class Config(AbstractConfig):

    class Meta:
        db_table = 'config'
