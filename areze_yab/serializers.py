from rest_framework import serializers
from areze_yab.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_company=validated_data.get('is_company', False),
            name=validated_data.get('name')
        )
        return user

    def update(self, instance, validated_data):
        # به‌روزرسانی فیلدها
        instance.username = validated_data.get('username', instance.username)
        instance.is_company = validated_data.get('is_company', instance.is_company)
        instance.name = validated_data.get('name', instance.name)

        # مدیریت رمز عبور
        password = validated_data.get('password')
        if password:
            instance.set_password(password)  # رمز عبور را به صورت ایمن به‌روزرسانی می‌کند

        instance.save()
        return instance


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
    def update(self, instance, validated_data):
        # به‌روزرسانی فیلدها
        instance.is_company = validated_data.get('is_company', instance.is_company)
        instance.name = validated_data.get('name', instance.name)
        instance.nationalID = validated_data.get('nationalID', instance.nationalID)
        instance.size = validated_data.get('size', instance.size)
        instance.company_domain = validated_data.get('company_domain', instance.company_domain)

        instance.save()
        return instance


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['name', 'text','description']


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    question_type = serializers.CharField()

    class Meta:
        model = Question
        fields = ['name', 'text', 'size', 'question_type', 'options','link','num_of_question','all_questions']

    def get_options(self, obj):
        if obj.question_type == QuestionType.MULTIPLE_CHOICE:
            return OptionSerializer(obj.options.all(), many=True).data
        return []

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['name','icon']


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    option = OptionSerializer(allow_null=True)
    text_answer = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = Answer
        fields = ['question', 'option', 'text_answer']


class ReportSerializer(serializers.Serializer):
    overallscore = serializers.FloatField(allow_null=True)
    subdomain_scores = serializers.DictField(child=serializers.FloatField(allow_null=True))
    messages = serializers.CharField()


class QuestionnaireStatusSerializer(serializers.ModelSerializer):
    next_question = serializers.SerializerMethodField()

    class Meta:
        model = Questionnaire
        fields = ['id', 'is_completed', 'next_question','is_paid','domain']

    def get_next_question(self, obj):
        unanswered = obj.answers.order_by('question__id').last()
        if not unanswered:
            return QuestionSerializer(
                Question.objects.filter(
                    subdomain__domain=obj.domain,
                    size=obj.company.size
                ).order_by('id').first()
            ).data
        next_question = Question.objects.filter(
            subdomain__domain=obj.domain,
            size=obj.company.size,
            id__gt=unanswered.question.id
        ).order_by('id').first()
        return QuestionSerializer(next_question).data if next_question else None



class QuestionnaireSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    domain = serializers.StringRelatedField()

    class Meta:
        model = Questionnaire
        fields = ['id', 'company', 'domain', 'created_at', 'is_completed']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["price"]


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['percent','usage']