from django.db import models
from django.contrib.auth.models import AbstractUser


class AuthUser(AbstractUser):
    _type = models.IntegerField(default=0)
    avatar_url = models.TextField(null=True)
    group_ids = models.JSONField(null=True)

    class Meta:
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'


class AuthMenu(models.Model):
    path = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    icon = models.CharField(max_length=150)
    parent = models.IntegerField(default=0)
    is_menu = models.IntegerField(default=0)
    sort = models.IntegerField(default=0)

    class Meta:
        db_table = 'auth_menu'


class AuthGroup(models.Model):
    name = models.CharField(max_length=150)
    menu_ids = models.JSONField()

    class Meta:
        db_table = 'auth_group_menu'
