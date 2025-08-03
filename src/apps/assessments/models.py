from django.db import models


class Quizz(models.Model):

    name = models.CharField(max_length=255)


class Question(models.Model):

    class ItemTypes(models.TextChoices):
        TEXT = 'text'
        SINGLE = 'single'
        MULTIPLE = 'multiple'

    quizz = models.ForeignKey(Quizz, blank=True, null=True, on_delete=models.SET_NULL, related_name='questions')
    item = models.CharField(max_length=255)
    item_type = models.CharField(max_length=255, choices=ItemTypes.choices)
    correct_answer = models.TextField(max_length=255, blank=True, null=True)


