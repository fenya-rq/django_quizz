from django.urls import path

from apps.assessments.api.views import CustomUserQuizzViewSet, QuizzViewSet

urlpatterns = [
    path('api/v1/quizz/<int:pk>/questions', QuizzViewSet.as_view({'get': 'quizz_question_list'})),
    path(
        'api/v1/quizz/<int:pk>/submit-answer',
        CustomUserQuizzViewSet.as_view({'post': 'answer_to_question'})
    ),
    path(
        'api/v1/quizz/<int:pk>/resume-quizz',
        CustomUserQuizzViewSet.as_view({'get': 'resume_quizz'})
    ),
    path(
        'api/v1/quizz/<int:pk>/finish-quizz',
        CustomUserQuizzViewSet.as_view({'get': 'finish_quizz'})
    ),
]
