from rest_framework import serializers

from apps.assessments.models import Question, Quizz, CustomUserAnswer


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


class CustomUserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUserAnswer
        fields = ['answer']

class CreateCustomUserAnswer(CustomUserAnswerSerializer):
    question_id = serializers.IntegerField()

    class Meta(CustomUserAnswerSerializer.Meta):
        fields = CustomUserAnswerSerializer.Meta.fields + ['question_id']

    def validate(self, attrs):
        quizz_id = self.context['quizz_id']
        question_id = attrs['question_id']

        if not Question.objects.filter(id=question_id, quizz_id=quizz_id).exists():
            raise serializers.ValidationError('The question does not belong to this quiz.')

        if CustomUserAnswer.objects.filter(
                user=self.context['user'],
                attempt=self.context['attempt'],
                question_id=question_id,
                quizz_id=quizz_id,
        ).exists():
            raise serializers.ValidationError('The answer to this question already exists.')

        return attrs

    def create(self, validated_data):
        return CustomUserAnswer.objects.create(
            user_id=self.context['user'].id,
            quizz_id=self.context['quizz_id'],
            attempt=self.context['attempt'],
            question_id=validated_data['question_id'],
            answer=validated_data['answer'],
        )


class QuestionWithUserAnswerSerializer(serializers.ModelSerializer):
    user_answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'item', 'item_type', 'user_answer']

    def get_user_answer(self, obj):
        user = self.context['user']
        attempt = self.context['attempt']
        answer = CustomUserAnswer.objects.filter(user=user, question=obj, attempt=attempt).first()
        if answer is None:
            return None
        return CustomUserAnswerSerializer(answer).data


class QuizzWithAnswersSerializer(serializers.ModelSerializer):
    questions = QuestionWithUserAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Quizz
        fields = ['id', 'name', 'questions']
