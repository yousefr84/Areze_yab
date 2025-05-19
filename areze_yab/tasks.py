# tasks.py
import openai
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import get_object_or_404

from .models import *


def openAI(prompt, rule):
    client = openai.OpenAI(api_key='YOUR_API_KEY')
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
        print(e)
        raise Exception("Failed to generate report from OpenAI")


@shared_task
def report(report_id, national_id, questionnaire_id):
    try:
        report_obj = Report.objects.get(id=report_id)
        report_obj.status = 'processing'
        report_obj.save()

        # شبیه‌سازی یک عملیات سنگین

        # پیدا کردن شرکت
        try:
            company = Company.objects.get(nationalID=national_id)
        except ObjectDoesNotExist:
            report_obj.status = 'error'
            report_obj.result = {'error': 'Company with this nationalID does not exist'}
            report_obj.save()

            # پیدا کردن پرسشنامه
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id, company=company)
        answers = questionnaire.answers.all()

        if not answers:
            report_obj.status = 'error'
            report_obj.result = {"error": "No answers provided"}
            report_obj.save()

            # محاسبه میانگین کلی برای پاسخ‌های چهارگزینه‌ای
        mc_answers = answers.filter(question__question_type=QuestionType.MULTIPLE_CHOICE)
        print(f"mc_answers: {mc_answers}")
        overallscore = None
        if mc_answers.exists():
            overallscore = sum(answer.option.value for answer in mc_answers) / mc_answers.count()
            print(f"overallscore: {overallscore}")
            overallscore = round(overallscore, 2)
            print(f"overallscore: {overallscore}")

            # محاسبه میانگین برای هر زیرحوزه
        subdomain_scores = {}
        messages = []
        text_answer = []

        response = ''
        for subdomain in questionnaire.domain.subdomains.all():
            subdomain_answers = answers.filter(question__subdomain=subdomain)
            if subdomain_answers:
                # پیام‌ها برای OpenAI
                # پیام‌ها برای OpenAI
                subdomain_name = subdomain.name
                company_domain = questionnaire.company.company_domain
                company_size = questionnaire.company.size
                domain = questionnaire.domain
                sum_of_answers = 0
                num_of_answers = 0
                print(f'before loop sum_of_answers: {sum_of_answers} and num_of_answers: {num_of_answers}')
                messages.append(f"کاربر در زیرحوزه {subdomain_name} پاسخ‌های زیر را ارائه کرده است:")
                for answer in subdomain_answers:
                    if answer.question.question_type == QuestionType.MULTIPLE_CHOICE:
                        messages.append(
                            f"{answer.question.text}: {answer.option.text}  ")
                        text_answer.append(
                            f"{answer.question.text}: {answer.option.text}  ")
                        sum_of_answers += answer.option.value
                        print(f"sum_of_answers: {sum_of_answers}")
                        num_of_answers += 1
                    else:  # OPEN_ENDED
                        messages.append(f"{answer.question.name}: {answer.text_answer}")
                        text_answer.append(f"{answer.question.name}: {answer.text_answer}")
                subdomain_scores.update({subdomain_name: sum_of_answers / num_of_answers})
                print(f'subdomain_score: {subdomain_scores}')
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
                response += 'start this subdomain'
                response += openAI(prompt, rule)
                response += 'end this subdomain'

        prompt = f'''
                                        تصورکن به عنوان یک کارشناس در حوزه {questionnaire.domain} قصد داری {questionnaire.domain} یک شرکت با مقیاس {questionnaire.company.size} را که در صنعت {questionnaire.company.company_domain} فعالیت میکند عارضه یابی کنی.
                        . برای این کار پرسشنامه عارضه یابی {questionnaire.domain} در اختیار تو است. این پرسشنامه شامل حوزه های مختلفی است که در {questionnaire.domain} شرکت تأثیر گذارند..
                        با توجه به سوالات و پاسخ های پرسشنامه، یک تحلیل عملکرد کلی از {questionnaire.domain} شرکت ارائه بده. فرمت این گزارش باید به شکل زیر است:
                        برای تحلیل عملکرد {questionnaire.domain} باید راجب موضوعات زیر در 3 پاراگراف و حداقل 300 کلمه توضیح بدی:
                        پاراگراف اول: (اهمیت عارضه یابی {questionnaire.domain} شرکت با توجه به صنعت {questionnaire.company.company_domain})
                        پارگراف دوم: (تحلیل عملکرد {questionnaire.domain} شرکت با توجه به پاسخ های هر حوزه)
                        پاراگراف سوم: (توضیح نقاط قوت و ضعف {questionnaire.domain} شرکت)
                        این توضیحات باید درباره ی حوزه های {questionnaire.domain} که شامل موارد زیر است باشد:

                        *گزارش هر اندازه هم که طولانی شد اما به صورت کامل و برای همه حوزه ها، تحلیل ها، توضیحات لازم و پیشنهادات بهود را ارائه بده*
                            {'\n'.join(messages)}'

                        '''

        rule = f'''
                                تصورکن به عنوان یک کارشناس در حوزه {questionnaire.domain} قصد داری {questionnaire.domain} یک شرکت با مقیاس {questionnaire.company.size} را که در صنعت {questionnaire.company.company_domain} فعالیت میکند عارضه یابی کنی.
                        '''
        response += 'start first'
        response += openAI(prompt, rule)
        response += 'end first'
        print(f"overallscore: {overallscore}")

        # ذخیره نتیجه
        result_data = {
            "overallScore": overallscore,
            "messages": response,
            "subdomain_scores": subdomain_scores,
            "summary": "پردازش با موفقیت انجام شد",
            "score": 85
        }
        report_obj.result = result_data
        report_obj.status = 'done'
        report_obj.save()

    except Report.DoesNotExist:

        return
