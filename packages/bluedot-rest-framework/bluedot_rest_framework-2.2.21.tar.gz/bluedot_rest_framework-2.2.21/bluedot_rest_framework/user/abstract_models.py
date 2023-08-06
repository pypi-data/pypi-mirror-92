from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractUser(AbstractRelationTime):
    wechat_id = models.IntegerField(null=True)
    unionid = models.CharField(max_length=100, null=True)
    tel_region = models.CharField(max_length=32, null=True, default='')
    industry = models.CharField(max_length=100, null=True, default='')

    user_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    tel = models.CharField(max_length=100, null=True)
    company = models.CharField(max_length=100, null=True)
    job = models.CharField(max_length=100, null=True)

    country = models.CharField(max_length=100, null=True)
    source_type = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True
