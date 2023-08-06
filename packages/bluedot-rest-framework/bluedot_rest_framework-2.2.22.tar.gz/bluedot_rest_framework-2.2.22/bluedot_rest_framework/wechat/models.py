from bluedot_rest_framework.utils.models import models, AbstractRelationTime


class WeChatUser(AbstractRelationTime):
    unionid = models.CharField(max_length=32)
    nick_name = models.CharField(max_length=100)
    gender = models.IntegerField()
    language = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    province = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    avatar_url = models.TextField()

    class Meta:
        db_table = 'wechat_user'


class WeChatUserOpenid(AbstractRelationTime):
    wechat = models.ForeignKey(WeChatUser, on_delete=models.CASCADE)
    appid = models.CharField(max_length=32)
    openid = models.CharField(max_length=32)
    subscribe = models.IntegerField(default=0)

    class Meta:
        db_table = 'wechat_user_openid'
