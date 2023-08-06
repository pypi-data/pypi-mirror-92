from bluedot_rest_framework.utils.models import models, AbstractRelationUser, AbstractRelationTime


class AbstractQuestion(AbstractRelationTime):
    title = models.CharField(max_length=100, null=True, default='')
    qa = models.JSONField()

    class Meta:
        abstract = True


class AbstractQuestionUser(AbstractRelationUser, AbstractRelationTime):
    qa_id = models.IntegerField(null=True)
    title = models.CharField(max_length=100, null=True)
    integral = models.IntegerField(default=0)
    qa = models.JSONField(null=True)

    class Meta:
        abstract = True
