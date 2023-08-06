from bluedot_rest_framework.utils.models import models, AbstractRelationUser, AbstractRelationTime


class EventComment(AbstractRelationUser, AbstractRelationTime):

    nick_name = models.CharField(max_length=100)
    avatar_url = models.CharField(max_length=255)
    schedule_id = models.IntegerField()
    event_id = models.IntegerField()
    state = models.IntegerField(default=0)
    data = models.TextField()

    like_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'event_comment'


class EventCommentLike(AbstractRelationUser):

    comment_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'event_comment_like'
