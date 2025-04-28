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
        questions = Question.objects.filter(
            subdomain__domain=domain,
            size=size,
        ).order_by('id')
        first_question = questions.first()
        number_of_questions = questions.count()
        if not first_question:
            return Response({"error": "No questions available"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={"number_of_questions": number_of_questions, "questionnaire": questionnaire.id,
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

        return Response(QuestionSerializer(next_question).data, status=status.HTTP_200_OK)


class ReportView(APIView):
    def openAI(self, prompt, rule):
        client = openai.OpenAI(api_key='')
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
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

        try:
            company = Company.objects.get(nationalID=national_id)
        except ObjectDoesNotExist:
            return Response(data={'error': 'Company with this nationalID does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, company=company)
        answers = questionnaire.answers.all()

        if not answers:
            return Response({"error": "No answers provided"}, status=status.HTTP_400_BAD_REQUEST)

        mc_answers = answers.filter(question__question_type=QuestionType.MULTIPLE_CHOICE)
        overallscore = None
        if mc_answers.exists():
            overallscore = sum(answer.option.value for answer in mc_answers) / mc_answers.count()
            overallscore = round(overallscore, 2)

        messages = []
        for subdomain in questionnaire.domain.subdomains.all():
            subdomain_answers = answers.filter(question__subdomain=subdomain)
            if subdomain_answers:
                messages.append(f"کاربر در زیرحوزه {subdomain.name} پاسخ‌های زیر را ارائه کرده است:")
                for answer in subdomain_answers:
                    if answer.question.question_type == QuestionType.MULTIPLE_CHOICE:
                        messages.append(f"{answer.question.name}: {answer.option.text} (امتیاز: {answer.option.value})")
                    else:  # OPEN_ENDED
                        messages.append(f"{answer.question.name}: {answer.text_answer}")
        if questionnaire.domain == 'Financial':
            prompt = f'''
            تصور کن یک کارشناس مالی هستی و قصد داری بر اساس مدل دوپونت و با توجه به اطلاعات صورت سود و زیان و ترازنامه، یک تحلیل مالی برای شرکت ارائه بدی. اطلاعات مالی به شرح زیر است:
                        {chr(10).join(messages)}

            با توجه به این اطلاعات، تحلیل دوپونت را ارائه بده.
            در ابتدای گزارش تحلیلی خود، در 4 پارگراف و حداقل 300 کلمه در باره ی ضرورت تحلیل صورت های مالی، توضیح مدل دوپونت و استفاده از این مدل برای تحلیل اطلاعات وارد شده توضیح بده.
            
            هر یک از شاخص های حاشیه سود خالص، گردش دارایی ها و اهرم مالی را به صورت منحصر به فرد در 2 پاراگراف و 120 کلمه تحلیل کن
             همچنین برای تاثیرگذاری بهتر تحلیل در تصمیم گیری ها، راهکارهایی برای بهبود نسبت هایی که محاسبه کردی ارائه بده . فرمت ارائه راهکارها به شکل زیر باشد:
              برای هر شاخص ، 3 تا 5 پیشنهاد منحصر به فرد برای بهبود عملکرد آن شاخص به گونه ای که برای صاحب کسب و کار که سطح آشنایی اولیه در حوزه مدیریت مالی دارد، به صورت ساده ارائه بده
            یک بخش از گزارش که با بعد از توضیحات مقدماتی و قبل از تحلیل ها باشد را به محاسبات دوپونت اختصاص بده

            
            '''
            rule = "تصور کن یک کارشناس مالی هستی و قصد داری بر اساس مدل دوپونت و با توجه به اطلاعات صورت سود و زیان و ترازنامه، یک تحلیل مالی برای شرکت ارائه بدی"
        else:

            prompt = f'''
                    تصور کن به عنوان یک کارشناس در حوزه {questionnaire.domain} قصد داری {questionnaire.domain} یک شرکت با مقیاس {questionnaire.company.size} را عارضه یابی کنی. برای این کار پرسشنامه عارضه یابی {questionnaire.domain} در اختیار تو است. این پرسشنامه از حوزه های مختلف تشکیل شده و هر حوزه سوالات مربوط به خود که نشان دهنده ی شاخص های عملکردی حوزه {questionnaire.domain} است را   شامل می‌شود. هر حوزه را با توجه به پاسخ های داده شده ی مربوط به آن در 120 کلمه و 2 پاراگراف تحلیل کن. این تحلیل باید شامل گزارشی از وضعیت فعلی حوزه {questionnaire.domain}، نقاط قوت و ضعف و فرصت‌های بهبود باشد.  
            همچنین برای هر حوزه، 3 تا 5 پیشنهاد منحصر به فرد برای بهبود عملکرد آن حوزه به گونه ای که برای صاحب کسب و کار با آشنایی اولیه در حوزه {questionnaire.domain} و به صورت ساده ارائه بده و برای هر پیشنهاد به صورت 
            جداگانه  یک مثال عملیاتی و اجرایی در یک پاراگراف جدا که با کلمه "به طور مثال" شروع میشود بزن.
            مثال:
            پیشنهادات بهبود:
            راه‌اندازی برنامه‌های ارجاع برای تشویق مشتریان وفادار به معرفی برند.
            به طور مثال: (مثال عملیاتی)
            برای هر حوزه از این مثال سمپل استفاده کن.
             برای تاثیر بیشتر در عملکرد شرکت، دلیل پیشنهاد ارائه شده و لزوم اجرای آن را به صورت دقیق توضیح بده.        
            پرسشنامه عارضه یابی {questionnaire.domain} به شرح زیر است:
            {chr(10).join(messages)}
            با توجه به پاسخ‌ها، در ابتدای گزارش عارضه یابی عملکرد شرکت را در حوزه {questionnaire.domain} که در سطح {questionnaire.company.size} قرار دارد را با در نظر گرفتن همه ی حوزه‌ها تحلیل کن و توضیحات را در 300 کلمه و 3 پاراگراف ارائه بده. در نظر داشته باش که این شرکت در زمینه {questionnaire.company.company_domain} فعالیت میکند. در تحلیل ها و راهکارهای پیشنهادی خود، زمینه {questionnaire.company.company_domain} را در نظر داشته باش.
            متنی از خودت اضافه نکن و فقط گزارش را ارائه بده.
                    '''
            rule = f' تصور کن به عنوان یک کارشناس در حوزه {questionnaire.domain} قصد داری {questionnaire.domain} یک شرکت با مقیاس {questionnaire.company.size} را عارضه یابی کنی'

        try:
            response = self.openAI(prompt=prompt, rule=rule)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        report = {
            "overallscore": overallscore,
            "messages": response
        }
        return Response(ReportSerializer(report).data, status=status.HTTP_200_OK)


class QuestionnairesView(APIView):
    def get(self, request):
        nationalId = request.query_params.get('nationalID')
        company = Company.objects.get(nationalID=nationalId)
        questionnaires = Questionnaire.objects.filter(company=company)
        serializer = QuestionnaireSerializer(questionnaires, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionnaireStatusView(APIView):
    def get(self, request, questionnaire_id):
        nationalID = request.query_params.get('nationalID')
        company = Company.objects.get(nationalID=nationalID)
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, company=company)
        return Response(QuestionnaireStatusSerializer(questionnaire).data, status=status.HTTP_200_OK)
