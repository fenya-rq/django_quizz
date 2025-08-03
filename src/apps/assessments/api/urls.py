from rest_framework.routers import DefaultRouter

from apps.assessments.api.views import CustomUserQuizzViewSet, QuizzViewSet

router = DefaultRouter()
router.register('api/v1/quizz', QuizzViewSet)
router.register('api/v1/user_quizz', CustomUserQuizzViewSet)
