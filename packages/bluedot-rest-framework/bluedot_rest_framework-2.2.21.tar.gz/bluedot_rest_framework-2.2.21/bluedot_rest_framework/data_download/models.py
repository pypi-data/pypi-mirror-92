from bluedot_rest_framework.utils.models import models, AbstractRelationTime, AbstractRelationUser


class AbstractDataDownload(AbstractRelationTime):
    data_download_type = models.IntegerField(default=1)
    category_id = models.IntegerField()
    title = models.CharField(max_length=255, default='')
    data = models.JSONField()
    view_count = models.IntegerField()

    class Meta:
        abstract = True


class DataDownload(AbstractDataDownload):
    class Meta:
        db_table = 'data_download'


class AbstractDataDownloadUser(AbstractRelationUser, AbstractRelationTime):
    data_download_id = models.IntegerField()

    class Meta:
        abstract = True


class DataDownloadUser(AbstractDataDownloadUser):
    class Meta:
        db_table = 'data_download_user'
