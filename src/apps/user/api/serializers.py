from rest_framework import serializers

from apps.user.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']
