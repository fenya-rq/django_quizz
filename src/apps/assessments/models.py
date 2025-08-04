from django.db import models

from apps.user.models import CustomUser


class Quizz(models.Model):

    name = models.CharField(max_length=255, unique=True)


class Question(models.Model):

    class ItemTypes(models.TextChoices):
        TEXT = 'text'
        SINGLE = 'single'
        MULTIPLE = 'multiple'

    quizz = models.ForeignKey(Quizz, blank=True, null=True, on_delete=models.SET_NULL, related_name='questions')
    item = models.CharField(max_length=255)
    item_type = models.CharField(max_length=255, choices=ItemTypes.choices)
    correct_answer = models.TextField(max_length=255)


class CustomUserAnswer(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE, related_name='user_answers')
    answer = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    attempt = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'question', 'quizz', 'attempt'],
                name='unique_answer_per_user_per_question_in_quizz'
            )
        ]


class CustomUserQuizz(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_quizz')
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE, related_name='user_quizz')
    finished = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    attempt = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'quizz', 'attempt'],
                name='unique_user_quizz_attempt'
            )
        ]
