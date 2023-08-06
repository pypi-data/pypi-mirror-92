from bluedot_rest_framework.utils.models import models
from bluedot_rest_framework.question.abstract_models import AbstractQuestionUser


class AbstractMaterial(AbstractQuestionUser):
    material_type = models.IntegerField()
    category_id = models.JSONField()
    title = models.CharField(max_length=100)
    banner = models.CharField(max_length=255)
    state = models.IntegerField(default=1)
    is_new = models.IntegerField(default=0)
    average_grade = models.FloatField(default=0)
    data = models.TextField(null=True)
    tags_id = models.JSONField(null=True)
    extend = models.JSONField(null=True)
    article = models.JSONField(null=True)
    recommend = models.JSONField(null=True)

    class Meta:
        abstract = True
