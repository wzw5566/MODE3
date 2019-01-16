from django.db import models
from datetime import datetime
#引入系统用户的分类
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Role(models.Model):
    """
    角色表
    """
    role_name = models.CharField(max_length=30, unique=True, verbose_name="角色名")
    create_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    role_desc = models.TextField(max_length=100, verbose_name="角色描述")
    role_parent_id = models.IntegerField(default=0, verbose_name="父级角色id")
    update_time = models.DateTimeField(default=datetime.now, verbose_name="更新时间")

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.role_name

#userProfile继承AbstractUser分类，进行拓展
class UserProfile(AbstractUser):
    """
    用户类拓展
    """
    name = models.CharField(max_length=30, verbose_name="姓名" )
    avatar = models.CharField(max_length=100, null=True, blank=True, verbose_name="头像")
    role = models.ManyToManyField(Role, verbose_name="角色", related_name='role', )

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    # @property
    # def role(self):
    #     return self.role.role_name
