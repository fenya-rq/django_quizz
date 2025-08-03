from django.urls import path, include

from apps.assessments.api.urls import router

urlpatterns = [
    path('', include(router.urls)),
]
