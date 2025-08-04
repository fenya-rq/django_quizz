from rest_framework.routers import DefaultRouter

from apps.user.api.views import CustomUserViewSet

router = DefaultRouter()
router.register('api/v1/user', CustomUserViewSet)
