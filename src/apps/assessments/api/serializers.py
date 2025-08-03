from rest_framework import serializers

from apps.assessments.models import Question, Quizz


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['item']


class QuizzSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quizz
        fields = ['id', 'name', 'questions']
        read_only_fields = ['id']


