from rest_framework import serializers

from accounts.models import User


class UserDetailSerializer(serializers.ModelSerializer):
    is_readonly = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['pk', 'email', 'username', 'is_staff', 'is_active', 'date_joined', 'last_login', 'profile',
                  'is_readonly']

    def get_is_readonly(self, obj):
        return obj.groups.filter(name='read_only').exists()
