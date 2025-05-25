import openai
from asgiref.sync import sync_to_async, async_to_sync
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from openai import AsyncOpenAI
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from areze_yab.serializers import *
from django.core.exceptions import ObjectDoesNotExist
import logging
from celery.result import AsyncResult
from .tasks import report as report_task, openEnded
from areze_yab.models import *


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

        # ایجاد کاربر

        try:
            if CustomUser.objects.filter(username=username).exists():
                return Response({'error': 'نام کاربری قبلاً استفاده شده است'}, status=status.HTTP_400_BAD_REQUEST)

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
        is_company = str(is_company).lower()

        if is_company == 'true':
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
                print(f"size of company: {company.size}")

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
        company_domain = company_data['company_domain']
        print(f"nationalID: {nationalID}")
        print(f"registrationNumber: {registrationNumber}")
        if not userid:
            return Response(data={'user id missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not company_data:
            return Response(data={"error": "Company is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(id=userid)
        if not company_data['size']:
            return Response(data={'size is missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not registrationNumber:
            return Response(data={'registrationNumber is missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not nationalID:
            return Response(data={'nationalID is missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not company_domain:
            return Response(data={'company_domain is missing'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_company:
            try:
                company = Company.objects.get(nationalID=nationalID)
            except:
                company = Company.objects.create(
                    company_domain=company_domain,
                    name=name,
                    registrationNumber=registrationNumber,
                    nationalID=nationalID,
                    size = company_data['size']
                )
                print(f'company: {company}')
                print(f'size of company: {company.size}')
                # افزودن کاربر به شرکت
                company.user.add(user)  # فرض می‌کنیم مدل Company فیلد user دارد
                company.save()
                print(f'company: {company}')
                print(f'size of company: {company.size}')
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
            # questionnaire.is_completed = True
            # questionnaire.save()
            return Response({"message": "Questionnaire completed"}, status=status.HTTP_202_ACCEPTED)

        return Response(data={'question': QuestionSerializer(next_question).data}, status=status.HTTP_200_OK)


logger = logging.getLogger(__name__)


# class ReportView(APIView):
#     def openAI(self, prompt, rule):
#         print('i going too send request to openAI')
#         client = openai.OpenAI(api_key='')
#         try:
#             response = client.chat.completions.create(
#                 model="gpt-4",
#                 temperature=0.3,
#                 messages=[
#                     {"role": "system", "content": rule},
#                     {"role": "user", "content": prompt}
#                 ]
#             )
#             print("i got the response")
#             return response.choices[0].message.content
#         except Exception as e:
#             raise Exception("Failed to generate report from OpenAI")
#
#     def get(self, request, questionnaire_id):
#         national_id = request.query_params.get('nationalID')
#         if not national_id:
#             return Response(data={'error': 'nationalID missing'}, status=status.HTTP_400_BAD_REQUEST)
#
#         # پیدا کردن شرکت
#         try:
#             company = Company.objects.get(nationalID=national_id)
#         except ObjectDoesNotExist:
#             return Response(data={'error': 'Company with this nationalID does not exist'},
#                             status=status.HTTP_404_NOT_FOUND)
#
#         # پیدا کردن پرسشنامه
#         questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, company=company)
#         answers = questionnaire.answers.all()
#
#         if not answers:
#             return Response({"error": "No answers provided"}, status=status.HTTP_400_BAD_REQUEST)
#
#         # محاسبه میانگین کلی برای پاسخ‌های چهارگزینه‌ای
#         mc_answers = answers.filter(question__question_type=QuestionType.MULTIPLE_CHOICE)
#         print(f"mc_answers: {mc_answers}")
#         overallscore = None
#         if mc_answers.exists():
#             overallscore = sum(answer.option.value for answer in mc_answers) / mc_answers.count()
#             print(f"overallscore: {overallscore}")
#             overallscore = round(overallscore, 2)
#             print(f"overallscore: {overallscore}")
#
#         # محاسبه میانگین برای هر زیرحوزه
#         subdomain_scores = {}
#         messages = []
#         text_answer = []
#         subdomains_list = []
#         num =0
#         response = ''
#         for subdomain in questionnaire.domain.subdomains.all():
#             subdomain_answers = answers.filter(question__subdomain=subdomain)
#             num +=1
#             subdomains_list.append(subdomain.name)
#             if subdomain_answers:
#                 # پیام‌ها برای OpenAI
#                 # پیام‌ها برای OpenAI
#                 subdomain_name = subdomain.name
#                 company_domain = questionnaire.company.company_domain
#                 company_size = questionnaire.company.size
#                 domain = questionnaire.domain
#                 sum_of_answers = 0
#                 num_of_answers = 0
#                 print(f'before loop sum_of_answers: {sum_of_answers} and num_of_answers: {num_of_answers}')
#                 messages.append(f"کاربر در زیرحوزه {subdomain_name} پاسخ‌های زیر را ارائه کرده است:")
#                 for answer in subdomain_answers:
#                     if answer.question.question_type == QuestionType.MULTIPLE_CHOICE:
#                         messages.append(
#                             f"{answer.question.text}: {answer.option.text}  ")
#                         text_answer.append(
#                             f"{answer.question.text}: {answer.option.text}  ")
#                         sum_of_answers += answer.option.value
#                         print(f"sum_of_answers: {sum_of_answers}")
#                         num_of_answers += 1
#                     else:  # OPEN_ENDED
#                         messages.append(f"{answer.question.name}: {answer.text_answer}")
#                         text_answer.append(f"{answer.question.name}: {answer.text_answer}")
#                 subdomain_scores.update({subdomain_name: sum_of_answers / num_of_answers})
#                 print(f'subdomain_score: {subdomain_scores}')
#                 if num == 5:
#                     prompt = f'''
#                                                    تصورکن به عنوان یک کارشناس در حوزه {domain} قصد داری {domain} یک شرکت با مقیاس {company_size} را که در صنعت {company_domain} فعالیت میکند عارضه یابی کنی. برای این کار پرسشنامه عارضه یابی {domain} در اختیار تو است. این پرسشنامه شامل حوزه های مختلفی است که در {domain} شرکت تأثیر گذارند..
# با توجه به سوالات و پاسخ های پرسشنامه، یک تحلیل عملکرد کلی از {domain} شرکت ارائه بده. فرمت این گزارش باید به شکل زیر است:
# برای تحلیل عملکرد {domain} باید راجب موضوعات زیر در 3 پاراگراف و حداقل 300 کلمه توضیح بدی:
# پاراگراف اول: (اهمیت عارضه یابی {domain} شرکت با توجه به صنعت {company_size})
# پارگراف دوم: (تحلیل عملکرد {domain} شرکت با توجه به پاسخ های هر حوزه)
# پاراگراف سوم: (توضیح نقاط قوت و ضعف {domain} شرکت)
# این توضیحات باید درباره ی حوزه های {domain} که شامل موارد زیر است باشد:
# حوزه ها: {subdomains_list}
# گزارش هر اندازه هم که طولانی شد اما به صورت کامل و برای همه حوزه ها، تحلیل ها، توضیحات لازم و پیشنهادات بهود را ارائه بده
# :پرسشنامه عارضه یابی به همراه جواب هایی که بایدآن ها را تحلیل کنی به شرح زیر است
#                                                        {'\n'.join(text_answer)}
#                                                        '''
#
#                     rule = f'''
#                                .تصورکن به عنوان یک کارشناس در حوزه {questionnaire.domain} قصد داری {questionnaire.domain} یک شرکت با مقیاس {questionnaire.company.size} را که در صنعت {questionnaire.company.company_domain} فعالیت میکند عارضه یابی کنی
#                                        '''
#                     response += 'start this subdomain'
#                     response += self.openAI(prompt, rule)
#                     response += 'end this subdomain'
#
#                     subdomains_list.clear()
#                     text_answer.clear()
#                     num =0
#
#         prompt = f'''
#                 تصورکن به عنوان یک کارشناس در حوزه {questionnaire.domain} قصد داری {questionnaire.domain} یک شرکت با مقیاس {questionnaire.company.size} را که در صنعت {questionnaire.company.company_domain} فعالیت میکند عارضه یابی کنی.
# . برای این کار پرسشنامه عارضه یابی {questionnaire.domain} در اختیار تو است. این پرسشنامه شامل حوزه های مختلفی است که در {questionnaire.domain} شرکت تأثیر گذارند..
# با توجه به سوالات و پاسخ های پرسشنامه، یک تحلیل عملکرد کلی از {questionnaire.domain} شرکت ارائه بده. فرمت این گزارش باید به شکل زیر است:
# برای تحلیل عملکرد {questionnaire.domain} باید راجب موضوعات زیر در 3 پاراگراف و حداقل 300 کلمه توضیح بدی:
# پاراگراف اول: (اهمیت عارضه یابی {questionnaire.domain} شرکت با توجه به صنعت {questionnaire.company.company_domain})
# پارگراف دوم: (تحلیل عملکرد {questionnaire.domain} شرکت با توجه به پاسخ های هر حوزه)
# پاراگراف سوم: (توضیح نقاط قوت و ضعف {questionnaire.domain} شرکت)
# این توضیحات باید درباره ی حوزه های {questionnaire.domain} که شامل موارد زیر است باشد:
#
# *گزارش هر اندازه هم که طولانی شد اما به صورت کامل و برای همه حوزه ها، تحلیل ها، توضیحات لازم و پیشنهادات بهود را ارائه بده*
#     {'\n'.join(messages)}'
#
# '''
#
#         rule = f'''
#         تصورکن به عنوان یک کارشناس در حوزه {questionnaire.domain} قصد داری {questionnaire.domain} یک شرکت با مقیاس {questionnaire.company.size} را که در صنعت {questionnaire.company.company_domain} فعالیت میکند عارضه یابی کنی.
# '''
#         response += 'start first'
#         response += self.openAI(prompt, rule)
#         response += 'end first'
#         print(f"overallscore: {overallscore}")
#         report = {
#             "overallScore": overallscore,
#             "messages": response,
#             "subdomain_scores": subdomain_scores
#         }
#         print("report going to save")
#         questionnaire.report = report
#         print("its saved")
#         return Response(ReportSerializer(report).data, status=status.HTTP_200_OK)


class StartReportView(APIView):
    def post(self, request):
        questionnaire_id = request.data.get('questionnaire_id')
        national_id = request.data.get('nationaID')
        if not national_id:
            return Response(data={'error': 'nationalID missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not questionnaire_id:
            return Response(data={'error': 'questionnaireID missing'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            questionnaire = Questionnaire.objects.get(id=questionnaire_id)
        except Questionnaire.DoesNotExist:
            return Response({'error': 'Questionnaire not found'}, status=status.HTTP_404_NOT_FOUND)

        # ساختن Report جدید
        report = Report.objects.create(
            questionnaire=questionnaire,
            status='pending'
        )
        print("object created")

        # اجرای تسک celery
        if questionnaire.domain.name != 'تحلیل صورت های مالی':
            print('its molti type domain')
            report_task.delay(report_id=report.id, national_id=national_id, questionnaire_id=questionnaire_id)
        else:
            print(" its open ended domain")
            openEnded.delay(report_id=report.id, national_id=national_id)
        print("task started")

        return Response({'report_id': report.id, 'status': 'pending'}, status=status.HTTP_202_ACCEPTED)


class GetReportAPIView(APIView):
    def get(self, request, report_id):
        report = get_object_or_404(Report, id=report_id)

        # اگر گزارش هنوز آماده نشده بود
        if report.status == 'error':
            return Response({
                'status': report.status,
                'message': report.result,
            },status.HTTP_404_NOT_FOUND)
        if report.status != 'done':
            return Response({
                'status': report.status,
                'message': 'گزارش هنوز کامل نشده است. لطفاً بعداً دوباره امتحان کنید.'
            }, status=status.HTTP_404_NOT_FOUND)

        # اگر گزارش آماده بود
        return Response({
            'status': report.status,
            'result': report.result
        }, status=status.HTTP_200_OK)


class QuestionnairesView(APIView):
    def get(self, request):
        # Extract query parameters
        is_company = request.query_params.get('is_company')
        national_id = request.query_params.get('nationalID')
        username = request.query_params.get('username')

        # Validate required query parameters
        if is_company is None:
            return Response(
                {"error": "Missing 'is_company' query parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )
        print(f"is_company befor: {is_company}")
        # Convert is_company to boolean
        is_company = is_company.lower()
        print(f"is_company after: {is_company}")

        try:
            if is_company == 'true':
                print(f"is_company is True")
                # Validate nationalID is provided and not empty
                if not national_id or not national_id.strip():
                    return Response(
                        {"error": "Missing or invalid 'nationalID' query parameter"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                # Get company by nationalID (single object)
                try:
                    company = Company.objects.get(nationalID=national_id.strip())
                    # Filter questionnaires for this company
                    questionnaires = Questionnaire.objects.filter(company=company)
                except Company.DoesNotExist:
                    return Response(
                        {"error": f"No company found with nationalID: {national_id}"},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                print(f"is_company is False")
                # Validate username is provided and not empty
                if not username or not username.strip():
                    return Response(
                        {"error": "Missing or invalid 'username' query parameter"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                print("we have username")
                # Get companies by username (queryset)
                companies = Company.objects.filter(user__username=username.strip())
                print(f"we have {len(companies)} companies")
                if not companies.exists():
                    return Response(
                        {"error": f"No companies found for username: {username}"},
                        status=status.HTTP_404_NOT_FOUND
                    )
                # Aggregate questionnaires for all matching companies
                questionnaires = Questionnaire.objects.filter(company__in=companies)
                print(f"we have {len(questionnaires)} questionnaires")
            # Serialize the questionnaires
            serializer = QuestionnaireSerializer(questionnaires, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class QuestionnaireStatusView(APIView):
    def get(self, request, questionnaire_id):
        nationalID = request.query_params.get('nationalID')
        company = Company.objects.get(nationalID=nationalID)
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, company=company)

        return Response(QuestionnaireStatusSerializer(questionnaire).data, status=status.HTTP_200_OK)
