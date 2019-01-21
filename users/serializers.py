# -*- coding: UTF-8 -*-
from django.contrib.auth import get_user_model
from users.models import Role
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.validators import UniqueValidator

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ("role_name", "role_desc")

class UserRegisterSerializer(serializers.ModelSerializer):

    # role = serializers.CharField(source="role.role_name", read_only=True)
    role = serializers.StringRelatedField(many=True)


    # 利用drf中的validators验证username是否唯一
    username = serializers.CharField(required=True, allow_blank=False, validators=[UniqueValidator(queryset=User.objects.all(),
                                                                                        message='用户已经存在')])
    print(username)
    password = serializers.CharField(
         style={"input_type": "password"},help_text="密码", label="密码", write_only=True,
     )
    print(password, "password")

    @staticmethod
    def addrole(roles, user):
        """
        为传入的 post 添加 tag ,如果 tag 已经存在,添加的关系是库中已经存在的 tag,
        如果 tag 不存在,则将 tag 添加到 Tag,添加的关系是新入库的 tag
        :param tags: validated_data 中的 tag
        :param post: Post类实例
        """
        for role in roles:
            try:
                r = Role.objects.get(name=role['role_name'])
                user.role.add(r)
                flag = True
            except ObjectDoesNotExist:
                flag = False
            if not flag:
                r = Role.objects.create(name=role['role_name'])
                user.role.add(r)
    def create(self, validated_data):
         print(validated_data)
         roles = validated_data["role"]
         user = super(UserRegisterSerializer, self).create(validated_data= validated_data)
         user.set_password(validated_data["password"])
         print(roles)
         if roles is not None:
             self.addtag(roles, user)
         user.save()
         return user
    class Meta:
         model = User
         fields = ( "username", "password", "role", "avatar")
         depth = 1


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列表类
    """
    # role = serializers.CharField(source="role.role_name", read_only=True)
    # role = serializers.StringRelatedField(many=True)
    role = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='role_name'
     )
    class Meta:
        model = User
        fields = ("id", "username", "name", "role", "avatar")