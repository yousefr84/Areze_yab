from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from areze_yab.serializers import *
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import logging
from .tasks import report as report_task, openEnded, newDomain
from areze_yab.models import *
import requests
import json


class PaymentAPIView(APIView):
    sandbox = 'www'
    MERCHANT = settings.MERCHANT  # باید تو settings.py تعریف شده باشه
    ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
    ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
    ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
    CallbackURL = 'http://91.107.185.130:8080/api/payment/verify/'  # اصلاح شده برای مطابقت با URL

    def post(self, request):
        try:
            payment = Payment.objects.get(id=1)
            amount = int(PaymentSerializer(payment).data['price'])  # فرض می‌کنیم فیلد price تو سریالایزر وجود داره
            print(f'Payment amount {amount} with type {type(amount)}')
        except Payment.DoesNotExist:
            return Response({'status': False, 'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({'status': False, 'error': 'Invalid payment data'}, status=status.HTTP_400_BAD_REQUEST)

        description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
        phone = '09120478082'

        data = {
            "MerchantID": self.MERCHANT,
            "Amount": amount,
            "Description": description,
            "Phone": phone,
            "CallbackURL": self.CallbackURL,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        try:
            response = requests.post(self.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response_data = response.json()
                if response_data['Status'] == 100:
                    return Response({
                        'status': True,
                        'url': self.ZP_API_STARTPAY + str(response_data['Authority']),
                        'authority': response_data['Authority']
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'status': False, 'code': str(response_data['Status'])},
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': False, 'code': str(response.status_code)}, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.Timeout:
            return Response({'status': False, 'code': 'timeout'}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except requests.exceptions.ConnectionError:
            return Response({'status': False, 'code': 'connection error'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def get(self, request):
        authority = request.GET.get('Authority')
        status_param = request.GET.get('Status')

        if not authority or status_param != 'OK':
            return Response({'status': False, 'error': 'Invalid payment attempt'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment.objects.get(id=1)
            amount = PaymentSerializer(payment).data['price']
        except Payment.DoesNotExist:
            return Response({'status': False, 'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({'status': False, 'error': 'Invalid payment data'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "MerchantID": self.MERCHANT,
            "Amount": amount,
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        try:
            response = requests.post(self.ZP_API_VERIFY, data=data, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                if response_data['Status'] == 100:
                    return HttpResponseRedirect('https://' + authority + '/' + response_data['Authority'])
                else:
                    return Response({'status': False, 'code': str(response_data['Status'])},
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response({'status': False, 'code': str(response.status_code)}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException:
            return Response({'status': False, 'code': 'request error'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


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
                size = data.get('size')
                national_id = username  # استفاده از username به‌عنوان nationalID
                if not company_domain:
                    return Response({'error': 'company_domain is missing'}, status=status.HTTP_400_BAD_REQUEST)

                if not size:
                    return Response({'error': 'size is missing'}, status=status.HTTP_400_BAD_REQUEST)
                company = Company.objects.create(
                    company_domain=company_domain,
                    name=name,
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

    def put(self, request):
        user_id = request.data.get('id')
        username = request.data.get('username')
        name = request.data.get('name')

        if not user_id:
            return Response(data={"error": "User ID missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(data={"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.is_company:
            try:
                national_id = username
                size = str(request.data.get('size'))
                company_domain = str(request.data.get('company_domain'))
                company = Company.objects.get(user=user)
                serializer = CompanySerializer(company, data={'name': name, 'national_id': national_id,
                                                              'size': size,
                                                              'company_domain': company_domain}, partial=True)
                if serializer.is_valid():
                    print('serializer validated1')
                    serializer.save()
                else:
                    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Company.DoesNotExist:
                return Response(data={"error": "Company not found for this user"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data={'username': username, 'name': name}, partial=True)

        if serializer.is_valid():
            print('serializer validated2')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyAPIView(APIView):
    def post(self, request):
        userid = request.data['userid']
        company_data = request.data['company']
        name = company_data['name']
        nationalID = company_data['nationalID']
        company_domain = company_data['company_domain']
        print(f"nationalID: {nationalID}")
        if not userid:
            return Response(data={'user id missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not company_data:
            return Response(data={"error": "Company is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(id=userid)
        if not company_data['size']:
            return Response(data={'size is missing'}, status=status.HTTP_400_BAD_REQUEST)

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
                    nationalID=nationalID,
                    size=company_data['size']
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

    def get(self, request):
        nationalID = request.query_params.get('nationalID')
        try:
            company = Company.objects.get(nationalID=nationalID)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
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

        # مدیریت نوع سوال
        option = None
        text_answer = None
        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            option_name = request.data.get('option')
            if not option_name:
                return Response(data={'error': 'option missing for multiple choice question'},
                                status=status.HTTP_400_BAD_REQUEST)
            option = get_object_or_404(Option, name=option_name, question=question)
        else:  # OPEN_ENDED
            text_answer = request.data.get('text_answer')
            if not text_answer:
                return Response(data={'error': 'text_answer missing for open-ended question'},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            answer = Answer(
                questionnaire=questionnaire,
                question=question,
                option=option,
                text_answer=text_answer  # استفاده از text_answer به جای txt_answer
            )
            answer.save()  # اعتبارسنجی در متد save مدل انجام می‌شود
        except ValidationError as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error saving answer: {str(e)}")  # لاگ برای دیباگ
            return Response(data={'error': f'Failed to save answer: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی سوال بعدی
        next_question = Question.objects.filter(
            subdomain__domain=questionnaire.domain,
            size=company.size,
            id__gt=question.id
        ).order_by('id').first()

        if not next_question:
            questionnaire.is_completed = True
            questionnaire.save()
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
        national_id = request.data.get('nationalID')
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
        if questionnaire.domain.name == 'بررسی اعتبار مالی شرکت':
            print('its new type domain')
            newDomain.delay(report_id=report.id, national_id=national_id, questionnaire_id=questionnaire_id)
        elif questionnaire.domain.name != 'تحلیل صورت های مالی':
            print("its open ended domain")
            openEnded.delay(report_id=report.id, national_id=national_id,
                            questionnaire_id=questionnaire_id)  # اصلاح پارامترها
        else:
            print('its multi type domain')
            report_task.delay(report_id=report.id, national_id=national_id, questionnaire_id=questionnaire_id)
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
            }, status.HTTP_404_NOT_FOUND)
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
        username = request.query_params.get('username')

        # Validate required query parameters

        try:

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
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
        serializer = QuestionnaireSerializer(questionnaire)
        try:
            report_id = Report.objects.get(questionnaire=questionnaire).id
        except Report.DoesNotExist:
            report_id = None
        return Response(data={"status": serializer.data, "report_id": report_id}, status=status.HTTP_200_OK)
