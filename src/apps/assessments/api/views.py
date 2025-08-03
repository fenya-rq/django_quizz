from datetime import datetime

from django.db.models import Max
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.viewsets import ModelViewSet

from apps.assessments.models import CustomUserQuizz, Quizz
from apps.assessments.api.serializers import (
    CreateCustomUserAnswer,
    QuizzSerializer,
    QuizzWithAnswersSerializer,
)

class QuizzViewSet(ModelViewSet):

    serializer_class = QuizzSerializer
    queryset = Quizz.objects.all()

    @action(detail=True, methods=['get'], url_path='questions')
    def quizz_question_list(self, request, pk=None):
        quizz = self.get_object()
        sr_data = self.get_serializer(quizz).data
        return Response(data=sr_data, status=200)


class CustomUserQuizzViewSet(ModelViewSet):

    serializer_class = QuizzWithAnswersSerializer
    queryset = CustomUserQuizz.objects.all()

    def get_permissions(self):
        if self.action == 'answer_to_question':
            permission_classes = [IsAuthenticated]
        elif self.action == 'resume_quizz':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'answer_to_question':
            return CreateCustomUserAnswer
        return super().get_serializer_class()

    @action(detail=True, methods=['post'], url_path='submit-answer')
    def answer_to_question(self, request, pk=None):
        user = request.user

        if pk is None:
            return Response(data={'detail': 'Choose the Quizz!'}, status=400)

        question_id = request.data.get('question_id')
        if question_id is None:
            return Response(data={'detail': 'Choose the question!'}, status=400)

        last_attempt = CustomUserQuizz.objects.filter(user=user, quizz_id=pk).aggregate(max_attempt=Max('attempt'))['max_attempt'] or 0

        user_progress_obj = (
            self.get_queryset().prefetch_related('quizz__user_answers', 'quizz__questions')
            .filter(user_id=user.id, quizz_id=pk, finished=False)
        ).first()

        if user_progress_obj is None:
            last_attempt += 1
            self.get_queryset().create(user=user, quizz_id=pk, attempt=last_attempt)

        serializer = self.get_serializer(
            data=request.data,
            context={'user': user, 'quizz_id': pk, 'attempt': last_attempt}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    @action(detail=True, methods=['get'], url_path='resume-quizz')
    def resume_quizz(self, request, pk=None):
        user = request.user

        last_attempt = CustomUserQuizz.objects.filter(user=user, quizz_id=pk).aggregate(max_attempt=Max('attempt'))['max_attempt'] or 0
        if last_attempt == 0:
            return Response(data={'detail': 'The quizz does not exists'}, status=HTTP_404_NOT_FOUND)

        progress = self.get_queryset().filter(user_id=user.id, quizz_id=pk, attempt=last_attempt, finished=False).first()
        if progress is None:
            return Response(data={'detail': 'Here are not unfinished quizzes.'}, status=HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(progress.quizz, context={'user': request.user, 'attempt': last_attempt})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='finish-quizz')
    def finish_quizz(self, request, pk=None):
        user = request.user

        last_attempt = CustomUserQuizz.objects.filter(user=user, quizz_id=pk).aggregate(max_attempt=Max('attempt'))['max_attempt'] or 0
        if last_attempt == 0:
            return Response(data={'detail': 'The quizz does not exists'}, status=HTTP_404_NOT_FOUND)

        unfinished_quizz = (
            self.get_queryset().prefetch_related('quizz__user_answers', 'quizz__questions')
            .filter(user_id=user.id, quizz_id=pk, attempt=last_attempt, finished=False)
        ).first()
        if unfinished_quizz is None:
            return Response(data={'detail': 'The quizz already finished!'}, status=HTTP_404_NOT_FOUND)

        correct_answers = unfinished_quizz.quizz.questions.values_list('correct_answer', flat=True)
        user_answers = unfinished_quizz.quizz.user_answers.filter(user_id=user.id).values_list('answer', flat=True)

        cleaned_correct_answer = {ca.lower() for ca in correct_answers}
        cleaned_user_answers = {ua.lower().strip() for ua in user_answers}

        invalid_answers_amount = cleaned_correct_answer - cleaned_user_answers

        total_questions = len(correct_answers)
        correct_count = total_questions - len(invalid_answers_amount)

        score_percent = round((correct_count / total_questions) * 100) if correct_answers else 0

        unfinished_quizz.finished = True
        unfinished_quizz.finished_at = datetime.now()
        unfinished_quizz.save(update_fields=['finished', 'finished_at'])

        return Response(
            data={
                'detail': f'Тест завершён. Результат: {score_percent}%',
                'score': score_percent,
                'correct_answers': correct_count,
                'total_questions': total_questions,
            },
            status=200
        )