from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class AbstractCategory(AbstractRelationTime):
    category_type = models.IntegerField(default=1)
    title = models.CharField(max_length=100, null=True)
    parent = models.IntegerField(default=0)
    sort = models.IntegerField(default=1)

    class Meta:
        abstract = True


class Category(AbstractCategory):
    class Meta:
        db_table = 'category'
