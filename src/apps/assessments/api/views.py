from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.assessments.models import Quizz
from apps.assessments.api.serializers import QuizzSerializer


class QuizzViewSet(ModelViewSet):

    serializer_class = QuizzSerializer
    queryset = Quizz.objects.all()

    @action(detail=True, methods=['get'], url_path='questions')
    def quizz_question_list(self, request, pk=None):
        quizz = self.get_object()
        sr_data = self.get_serializer(quizz).data
        return Response(data=sr_data, status=200)