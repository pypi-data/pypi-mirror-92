from bluedot_rest_framework.utils.models import models, AbstractRelationTime
from .abstract_models import AbstractEventExtend, AbstractEventLive, AbstractEventAddress


class AbstractEvent(AbstractEventExtend, AbstractEventLive, AbstractEventAddress, AbstractRelationTime):
    event_type = models.IntegerField(default=1)
    is_show = models.IntegerField(default=0)

    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255, null=True)
    description = models.TextField(verbose_name='介绍')

    banner = models.CharField(max_length=255, verbose_name='封面图片')
    qr_code = models.CharField(max_length=255, verbose_name='二维码', null=True)
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    module_list = models.JSONField(verbose_name='模块列表')

    class Meta:
        abstract = True


class Event(AbstractEvent):
    class Meta:
        db_table = 'event'
