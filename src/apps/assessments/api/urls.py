from rest_framework.routers import DefaultRouter

from apps.assessments.api.views import QuizzViewSet

router = DefaultRouter()
router.register('api/v1/quizz', QuizzViewSet)
