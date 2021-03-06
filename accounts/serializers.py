from rest_framework import serializers

from accounts.models import User


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'email', 'username', 'is_staff', 'is_active', 'date_joined', 'last_login']
