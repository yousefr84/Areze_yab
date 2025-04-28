from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from areze_yab.serializers import *


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        name = data['name']
        username = data['username']
        password = data['password']
        is_company = data['is_company']
        if not data:
            return Response(data={'No data provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response(data={'No password provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not name:
            return Response({'error': 'name is missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not username:
            return Response({'error': 'username is missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not is_company:
            return Response({'error': 'is_company is missing'}, status=status.HTTP_400_BAD_REQUEST)
        if data['password'] != data['repeatPassword']:
            return Response({'error': 'رمز عبور و تکرار آن با هم برابر نیست'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.create(username=username, password=password, is_company=is_company, name=name)
        serializer = UserSerializer(user)

        if is_company == "true" or is_company == "True":
            try:
                company_domain = data['company_domain']
                if not company_domain:
                    return Response(data={'error': 'company_domain is missing'}, status=status.HTTP_400_BAD_REQUEST)
                registrationNumber = data['registrationNumber']
                if not registrationNumber:
                    return Response(data={'error': 'registrationNumber is missing'}, status=status.HTTP_400_BAD_REQUEST)
                nationalID = username
                size = data['size']
                if not size:
                    return Response(data={'error': 'size is missing'}, status=status.HTTP_400_BAD_REQUEST)
                company = Company.objects.create(company_domain=company_domain, name=name,
                                                 registrationNumber=registrationNumber, nationalID=nationalID, )
                company.size = size
                company.user.add(CustomUser.objects.get(id=serializer.data['id']))
                company.save()
                serializer = CompanySerializer(company)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({'error': _('Company creation failed: {}').format(str(e))},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response(data={"error": "User ID missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(data={"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # اگر کاربر یک شرکت باشد، اطلاعات شرکت را واکشی می‌کنیم
        if user.is_company:
            try:
                company = Company.objects.get(user=user.id)
            except Company.DoesNotExist:
                return Response(data={"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)
            # استفاده از serializer برای شرکت
            company_serializer = CompanySerializer(instance=company)  # استفاده از instance به جای data

            return Response(company_serializer.data, status=status.HTTP_200_OK)

        # در غیر این صورت، از serializer برای کاربر استفاده می‌کنیم
        user_serializer = UserSerializer(instance=user)  # استفاده از instance به جای data

        return Response(user_serializer.data, status=status.HTTP_200_OK)


class CompanyAPIView(APIView):
    def post(self, request):
        userid = request.data['userid']
        company_data = request.data['company']
        name = company_data['name']
        registrationNumber = company_data['registrationNumber']
        nationalID = company_data['nationalID']
        size = company_data['size'],
        company_domain = company_data['company_domain']

        if not userid:
            return Response(data={'user id missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not company_data:
            return Response(data={"error": "Company is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(id=userid)
        if not user.is_company:
            company = Company.objects.create(name=name, company_domain=company_domain,
                                             registrationNumber=registrationNumber, nationalID=nationalID, size=size)
            company.user.add(user)
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)


class DomainsAPIView(APIView):
    def get(self, request):
        domains = Domain.objects.all()
        serializer = DomainSerializer(domains, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StartQuestionnaireView(APIView):
    def post(self, request):
        domain_name = request.data.get('domain')
        nationalId = request.data.get('nationalID')
        if not domain_name:
            return Response(data={'error': 'domain is missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not nationalId:
            return Response(data={'error': 'userid is missing'}, status=status.HTTP_400_BAD_REQUEST)
        company = Company.objects.get(nationalID=nationalId)
        domain = get_object_or_404(Domain, name=domain_name)
        size = company.size
        questionnaire = Questionnaire.objects.create(company=company, domain=domain)
        print(size)
        print(domain)
        questions = Question.objects.filter(
            subdomain__domain=domain,
            size=size,
        ).order_by('id')
        print(questions)
        first_question = questions.first()
        number_of_questions = questions.count()
        if not first_question:
            return Response({"error": "No questions available"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={"number_of_questions": number_of_questions, "questionnaire": questionnaire.id,
                              "question": QuestionSerializer(first_question).data}, status=status.HTTP_200_OK)


class SubmitAnswerView(APIView):
    def post(self, request, questionnaire_id):
        nationalId = request.data.get('nationalID')
        if not nationalId:
            return Response(data={'error': 'nationalID missing'}, status=status.HTTP_400_BAD_REQUEST)
        company = Company.objects.get(nationalID=nationalId)
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, company=company)
        question_name = request.data.get('question')
        if not question_name:
            return Response(data={'error': 'question missing'}, status=status.HTTP_400_BAD_REQUEST)
        option_name = request.data.get('option')
        if not option_name:
            return Response(data={'error': 'option missing'}, status=status.HTTP_400_BAD_REQUEST)
        question = get_object_or_404(Question, name=question_name)
        option = get_object_or_404(Option, name=option_name, question=question)

        Answer.objects.create(
            questionnaire=questionnaire,
            question=question,
            option=option
        )

        next_question = Question.objects.filter(
            subdomain__domain=questionnaire.domain,
            size=company.size,
            id__gt=question.id
        ).order_by('id').first()

        if not next_question:
            questionnaire.is_completed = True
            questionnaire.save()
            return Response({"message": "Questionnaire completed"}, status=status.HTTP_200_OK)

        return Response(QuestionSerializer(next_question).data, status=status.HTTP_200_OK)


class ReportView(APIView):
    def get(self, request, questionnaire_id):
        nationalId = request.query_params.get('nationalID')
        company = Company.objects.get(nationalID=nationalId)
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, company=company)
        answers = questionnaire.answers.all()

        if not answers:
            return Response({"error": "No answers provided"}, status=status.HTTP_400_BAD_REQUEST)

        overallscore = sum(answer.option.value for answer in answers) / len(answers)

        messages = []
        for subdomain in questionnaire.domain.subdomains.all():
            subdomain_answers = answers.filter(question__subdomain=subdomain)
            if subdomain_answers:
                messages.append(f"کاربر در زیرحوزه {subdomain.name} گزینه‌های زیر را انتخاب کرده است:")
                for answer in subdomain_answers:
                    messages.append(f"{answer.question.name}: {answer.option.text}")

        report = {
            "overallscore": overallscore,
            "messages": "\n".join(messages)
        }
        return Response(ReportSerializer(report).data, status=status.HTTP_200_OK)

class QuestionnairesView(APIView):
    def get(self, request):
        nationalId = request.query_params.get('nationalID')
        company = Company.objects.get(nationalID=nationalId)
        questionnaires =Questionnaire.objects.filter(company=company)
        serializer =QuestionnaireSerializer(questionnaires,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class QuestionnaireStatusView(APIView):
    def get(self, request, questionnaire_id):
        nationalID = request.query_params.get('nationalID')
        company = Company.objects.get(nationalID=nationalID)
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, company=company)
        return Response(QuestionnaireStatusSerializer(questionnaire).data, status=status.HTTP_200_OK)
