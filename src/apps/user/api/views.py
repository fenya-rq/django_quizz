from rest_framework.viewsets import ModelViewSet

from apps.user.models import CustomUser
from apps.user.api.serializers import CustomUserSerializer


class CustomUserViewSet(ModelViewSet):

    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
