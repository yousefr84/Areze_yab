import openai
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from areze_yab.serializers import *
from django.core.exceptions import ObjectDoesNotExist


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        # اعتبارسنجی داده‌های ورودی
        try:
            name = data.get('name')
            username = data.get('username')
            password = data.get('password')
            repeat_password = data.get('repeatPassword')
            is_company = data.get('is_company')
        except KeyError as e:
            return Response({'error': f'Missing field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        if not name:
            return Response({'error': 'name is missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not username:
            return Response({'error': 'username is missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': 'password is missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not is_company:
            return Response({'error': 'is_company is missing'}, status=status.HTTP_400_BAD_REQUEST)
        if password != repeat_password:
            return Response({'error': 'رمز عبور و تکرار آن با هم برابر نیست'}, status=status.HTTP_400_BAD_REQUEST)

        # تبدیل is_company به بولین
        is_company = str(is_company).lower()

        # ایجاد کاربر
        try:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                name=name,
                is_company=is_company
            )
            user_serializer = UserSerializer(user)
        except IntegrityError:
            return Response({'error': 'نام کاربری قبلاً استفاده شده است'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'خطا در ایجاد کاربر: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # اگر کاربر شرکت است، شرکت را ایجاد کن
        if is_company:
            try:
                company_domain = data.get('company_domain')
                registration_number = data.get('registrationNumber')
                size = data.get('size')
                national_id = username  # استفاده از username به‌عنوان nationalID

                if not company_domain:
                    return Response({'error': 'company_domain is missing'}, status=status.HTTP_400_BAD_REQUEST)
                if not registration_number:
                    return Response({'error': 'registrationNumber is missing'}, status=status.HTTP_400_BAD_REQUEST)
                if not size:
                    return Response({'error': 'size is missing'}, status=status.HTTP_400_BAD_REQUEST)

                company = Company.objects.create(
                    company_domain=company_domain,
                    name=name,
                    registrationNumber=registration_number,
                    nationalID=national_id,
                    size=size
                )
                # افزودن کاربر به شرکت
                company.user.add(user)  # فرض می‌کنیم مدل Company فیلد user دارد
                company.save()

                return Response(user_serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return Response({'error': f'خطا در ایجاد شرکت: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': f'خطا در ایجاد شرکت: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

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
        questions = Question.objects.filter(
            subdomain__domain=domain,
            size=size,
        ).order_by('id')
        first_question = questions.first()
        if not first_question:
            return Response({"error": "No questions available"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={"questionnaire": questionnaire.id,
                              "question": QuestionSerializer(first_question).data}, status=status.HTTP_200_OK)


class SubmitAnswerView(APIView):
    def post(self, request, questionnaire_id):
        national_id = request.data.get('nationalID')
        if not national_id:
            return Response(data={'error': 'nationalID missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(nationalID=national_id)
        except ObjectDoesNotExist:
            return Response(data={'error': 'Company with this nationalID does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, company=company)

        question_name = request.data.get('question')
        if not question_name:
            return Response(data={'error': 'question missing'}, status=status.HTTP_400_BAD_REQUEST)

        question = get_object_or_404(Question, name=question_name)

        if question.subdomain.domain != questionnaire.domain or question.size != company.size:
            return Response(data={'error': 'Invalid question for this questionnaire'},
                            status=status.HTTP_400_BAD_REQUEST)

        if Answer.objects.filter(questionnaire=questionnaire, question=question).exists():
            return Response(data={'error': 'An answer for this question already exists'},
                            status=status.HTTP_400_BAD_REQUEST)

        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            option_name = request.data.get('option')
            if not option_name:
                return Response(data={'error': 'option missing for multiple choice question'},
                                status=status.HTTP_400_BAD_REQUEST)
            option = get_object_or_404(Option, name=option_name, question=question)
            text_answer = None
        else:
            text_answer = request.data.get('text_answer')
            if not text_answer:
                return Response(data={'error': 'text_answer missing for open-ended question'},
                                status=status.HTTP_400_BAD_REQUEST)
            option = None

        try:
            Answer.objects.create(
                questionnaire=questionnaire,
                question=question,
                option=option,
                text_answer=text_answer
            )
        except Exception as e:
            return Response(data={'error': 'Failed to save answer'}, status=status.HTTP_400_BAD_REQUEST)

        next_question = Question.objects.filter(
            subdomain__domain=questionnaire.domain,
            size=company.size,
            id__gt=question.id
        ).order_by('id').first()

        if not next_question:
            questionnaire.is_completed = True
            questionnaire.save()
            return Response({"message": "Questionnaire completed"}, status=status.HTTP_200_OK)

        return Response(data={'question': QuestionSerializer(next_question).data}, status=status.HTTP_200_OK)


class ReportView(APIView):
    def openAI(self, prompt, rule):
        client = openai.OpenAI(api_key='')
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                temperature=0.3,
                messages=[
                    {"role": "system", "content": rule},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception("Failed to generate report from OpenAI")

    def get(self, request, questionnaire_id):
        national_id = request.query_params.get('nationalID')
        if not national_id:
            return Response(data={'error': 'nationalID missing'}, status=status.HTTP_400_BAD_REQUEST)

        # پیدا کردن شرکت
        try:
            company = Company.objects.get(nationalID=national_id)
        except ObjectDoesNotExist:
            return Response(data={'error': 'Company with this nationalID does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        # پیدا کردن پرسشنامه
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, company=company)
        answers = questionnaire.answers.all()

        if not answers:
            return Response({"error": "No answers provided"}, status=status.HTTP_400_BAD_REQUEST)

        # محاسبه میانگین کلی برای پاسخ‌های چهارگزینه‌ای
        mc_answers = answers.filter(question__question_type=QuestionType.MULTIPLE_CHOICE)
        overallscore = None
        if mc_answers.exists():
            overallscore = sum(answer.option.value for answer in mc_answers) / mc_answers.count()
            overallscore = round(overallscore, 2)

        # محاسبه میانگین برای هر زیرحوزه
        subdomain_scores = {}
        messages = []
        response=''
        for subdomain in questionnaire.domain.subdomains.all():
            subdomain_answers = answers.filter(question__subdomain=subdomain)
            if subdomain_answers:
                # پیام‌ها برای OpenAI
                # پیام‌ها برای OpenAI
                subdomain_name=subdomain.name
                company_domain = questionnaire.company.company_domain
                company_size = questionnaire.company.size

                messages.append(f"کاربر در زیرحوزه {subdomain_name} پاسخ‌های زیر را ارائه کرده است:")
                for answer in subdomain_answers:
                    if answer.question.question_type == QuestionType.MULTIPLE_CHOICE:
                        messages.append(
                            f"{answer.question.name}: {answer.option.text} (توضیح: {answer.option.description})")
                    else:  # OPEN_ENDED
                        messages.append(f"{answer.question.name}: {answer.text_answer}")

                prompt = f'''
                                   تصورکن به عنوان یک کارشناس در حوزه {questionnaire.domain.name} قصد داری {questionnaire.domain.name} یک شرکت با مقیاس {questionnaire.company.size} را که در صنعت {questionnaire.company.company_domain} فعالیت میکند عارضه یابی کنی. برای این کار پرسشنامه عارضه یابی {questionnaire.domain.name} در اختیار تو است. این پرسشنامه شامل حوزه {subdomain.name} است که در {questionnaire.domain.name} شرکت تأثیر گذارند.:
                   در گزارش عارضه‌یابی باید حوزه    {subdomain.name} به صورت مجزا تحلیل شود و توضیحات در دو پاراگراف و 150 کلمه ارائه شود                
                                   همچنین  3 تا 5 پیشنهاد منحصر به فرد برای بهبود عملکرد حوزه {subdomain.name} به گونه ای که برای صاحب کسب و کار با آشنایی اولیه در حوزه {questionnaire.domain} و به صورت ساده ارائه بده و برای هر پیشنهاد به صورت جداگانه  یک مثال عملیاتی و اجرایی در یک پاراگراف جدا که با کلمه "به طور مثال" شروع میشود بزن.
                   فرمت گزارش باید به شکل مثال زیر باشد:               
                                   مثال:
                   حوزه :               {subdomain}
                   *تحلیل                      {subdomain}در 150 کلمه و 2 پاراگراف*
                                       *پیشنهاد اول: (توضیح پیشنهاد بهبود)*
                                       به طور مثال: (توضیح مثال عملیاتی)*
                   *پیشنهاد دوم: (توضیح پیشنهاد بهبود)*                    
                                   *به طور مثال: (توضیح مثال عملیاتی)*
                                       *پیشنهاد سوم: (توضیح پیشنهاد بهبود)*
                   *به طور مثال: (توضیح مثال عملیاتی)*                 
                             *پیشنهاد چهارم: (توضیح پیشنهاد بهبود)*
                   *به طور مثال: (توضیح مثال عملیاتی)*             
                               *پیشنهاد پنجم: (توضیح پیشنهاد بهبود)*
                                       *به طور مثال: (توضیح مثال عملیاتی)*
                   در تحلیل حوزه                        {subdomain} و ارائه راهکارهای پیشنهادی بهبود به نکته زیر توجه کن:
                   این عارضه یابی مخصوص یک شرکت با مقیاس {questionnaire.company.size} است که در صنعت {questionnaire.company.company_domain} فعالیت میکند و تحلیل ها و راهکارهای خود را متناسب با چنین شرکتی ارائه بده           

                                   پرسشنامه عارضه یابی به همراه جواب هایی که بایدآن ها را تحلیل کنی به شرح زیر است
                                   {'\n'.join(messages)}
                                   '''
                rule = f'''
                           .تصورکن به عنوان یک کارشناس در حوزه {questionnaire.domain} قصد داری {questionnaire.domain} یک شرکت با مقیاس {questionnaire.company.size} را که در صنعت {questionnaire.company.company_domain} فعالیت میکند عارضه یابی کنی
                                   '''

                response += self.openAI(prompt, rule)

        report = {
            "overallScore": overallscore,
            "messages": response,
            "subdomain_scores": subdomain_scores
        }
        return Response(ReportSerializer(report).data, status=status.HTTP_200_OK)


class QuestionnairesView(APIView):
    def get(self, request):
        is_company = request.query_params.get('is_company')
        if bool(is_company):
            nationalId = request.query_params.get('nationalID')
            companies = Company.objects.get(nationalID=nationalId)
        else:
            username = request.query_params.get('username')
            companies = Company.objects.filter(username=username)
        for company in companies:
            questionnaires = Questionnaire.objects.filter(company=company)
        serializer = QuestionnaireSerializer(questionnaires, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionnaireStatusView(APIView):
    def get(self, request, questionnaire_id):
        nationalID = request.query_params.get('nationalID')
        company = Company.objects.get(nationalID=nationalID)
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, company=company)
        return Response(QuestionnaireStatusSerializer(questionnaire).data, status=status.HTTP_200_OK)
