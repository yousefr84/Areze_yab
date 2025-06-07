# tasks.py
import openai
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import get_object_or_404

from .models import *
from .serializers import DomainSerializer


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
        domain = DomainSerializer(questionnaire.domain).data

        # ذخیره نتیجه
        result_data = {
            "overallScore": overallscore,
            "messages": response,
            "domain": domain.name,
            "subdomain_scores": subdomain_scores,
            "summary": "پردازش با موفقیت انجام شد",
            "score": 85
        }
        print(result_data)
        questionnaire.report = result_data
        questionnaire.is_paid = True
        questionnaire.save()
        report_obj.result = result_data
        report_obj.status = 'done'
        report_obj.save()

    except Report.DoesNotExist:

        return


@shared_task
def openEnded(report_id, national_id, questionnaire_id):
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
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
        answers = questionnaire.answers.all()

        if not answers:
            report_obj.status = 'error'
            report_obj.result = {"error": "No answers provided"}
            report_obj.save()

        messages = []
        # محاسبه میانگین کلی برای پاسخ‌های چهارگزینه‌ای
        mc_answers = answers.filter(question__question_type=QuestionType.OPEN_ENDED)
        for answer in mc_answers:
            messages.append(f"{answer.question.text}: {answer.text_answer}")
        response = ''
        prompt = f'''
        تصور کن یک کارشناس مالی هستی و قصد داری بر اساس مدل دوپونت و با توجه به اطلاعات صورت سود و زیان و ترازنامه، یک تحلیل مالی برای شرکت ارائه بدی. اطلاعات مالی به واحد ریال و به شرح زیر است:
{'\n'.join(messages)}
با توجه به اطلاعات مالی ، یک تحلیل عملکرد کلی حوزه مالی شرکت بر اساس مدل دوپونت ارائه. فرمت این گزارش باید به شکل زیر باشد:
برای تحلیل عملکرد مالی بر اساس مدل دوپونت  باید راجب موضوعات زیر در 3 پاراگراف و حداقل 400 کلمه توضیح بدی:
پاراگراف اول: (معرفی مدل دو پونت و توضیح راجب نسبت های آن)
پاراگراف دوم: (انجام محاسبات دو پونت)
پارگراف سوم: (تحلیل عملکرد مالی شرکت بر اساس مدل دوپونت)
*گزارش هر اندازه هم که طولانی شد اما به صورت کامل  و بدون وقفه تحلیل را ارائه بده*

        
    '''
        rule = f'''
        تصور کن یک کارشناس مالی هستی و قصد داری بر اساس مدل دوپونت و با توجه به اطلاعات صورت سود و زیان و ترازنامه، یک تحلیل مالی برای شرکت ارائه بدی.
    '''
        response += openAI(prompt, rule)
        response += 'end first'
        prompt = f'''
تصور کن یک کارشناس مالی هستی و قصد داری بر اساس مدل دوپونت و با توجه به اطلاعات صورت سود و زیان و ترازنامه، یک تحلیل مالی برای شرکت ارائه بدی. اطلاعات مالی به واحد ریال و به شرح زیر است:
{'\n'.join(messages)}
با توجه به اطلاعات مالی، همچنین برای تاثیرگذاری بهتر تحلیل دوپونت در تصمیم گیری ها، راهکارهایی برای بهبود نسبت هایی که محاسبه کردی ارائه بده . برای هر شاخص ، 3 تا 5 پیشنهاد منحصر به فرد برای بهبود عملکرد آن شاخص به گونه ای که برای صاحب کسب و کار که سطح آشنایی اولیه در حوزه مدیریت مالی دارد، به صورت ساده ارائه بده.
 فرمت ارائه راهکارها به شکل زیر باشد:
تحلیل شاخص حاشیه سود خالص در 2 پاراگراف و 120 کلمه
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
تحلیل شاخص گردش دارایی ها در 2 پاراگراف و 120 کلمه
*پیشنهاد اول: (توضیح پیشنهاد بهبود)*
به طور مثال: (توضیح مثال عملیاتی)*
*پیشنهاد دوم: (توضیح پیشنهاد بهبود)*
*به طور مثال: (توضیح مثال عملیاتی)*
*پیشنهاد سوم: (توضیح پیشنهاد بهبود)*
*به طور مثال: (توضیح مثال عملیاتی)*
*پیشنهاد چهارم: (توضیح پیشنهاد بهبود)*
*به طور مثال: (توضیح مثال عملیاتی)*
*پیشنهاد پنجم: (توضیح پیشنهاد بهبود)*
تحلیل شاخص اهرم مالی در 2 پاراگراف و 120 کلمه
*پیشنهاد اول: (توضیح پیشنهاد بهبود)*
به طور مثال: (توضیح مثال عملیاتی)*
*پیشنهاد دوم: (توضیح پیشنهاد بهبود)*
*به طور مثال: (توضیح مثال عملیاتی)*
*پیشنهاد سوم: (توضیح پیشنهاد بهبود)*
*به طور مثال: (توضیح مثال عملیاتی)*
*پیشنهاد چهارم: (توضیح پیشنهاد بهبود)*
*به طور مثال: (توضیح مثال عملیاتی)*
*پیشنهاد پنجم: (توضیح پیشنهاد بهبود)*
*تاکید میکنم زارش هر اندازه هم که طولانی شد اما به صورت کامل و بدون وقفه راهکارها و مثال ها را ارائه بده*

'''
        response += openAI(prompt, rule)
        print(response)
        result_data = response
        questionnaire.report = result_data
        questionnaire.is_paid = True
        questionnaire.save()
        report_obj.result = result_data
        report_obj.status = 'done'
        report_obj.save()

    except Report.DoesNotExist:
        return


@shared_task
def newDomain(report_id, national_id, questionnaire_id):
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
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
        answers = questionnaire.answers.all()

        if not answers:
            report_obj.status = 'error'
            report_obj.result = {"error": "No answers provided"}
            report_obj.save()

        messages = []
        # محاسبه میانگین کلی برای پاسخ‌های چهارگزینه‌ای
        mc_answers = answers.filter(question__question_type=QuestionType.OPEN_ENDED)
        for answer in mc_answers:
            messages.append(f"{answer.question.text}: {answer.text_answer}")
        response = ''
        prompt = f'''
        من می‌خواهم یک گزارش کامل اعتباری از وضعیت مالی شرکت {company.name} تهیه کنم. اطلاعات مالی به شرح زیر است:
برای بخش اطلاعات عمومی با توجه به اطلاعاتی که برات ارسال میشه با فرمتی که بهت میگم اطلاعات رو نمایش بده
در قالب یک جدول با توجه به مثال و اطلاعات داده شده یک جدول کامل بهم ارائه بده
(مثال:نوع شرکت در ستون مورد و سهامی خاص در ستون شرح)برای سایر اطلاعات هم این روند رو ادامه بده,
اطلاعات عمومی در پایین ارسال میشود:
{'\n'.join(messages)}

    '''
        rule = f'''
        تصور کن یک کارشناس مالی هستی و قصد داری بر اساس مدل دوپونت و با توجه به اطلاعات صورت سود و زیان و ترازنامه، یک تحلیل مالی برای شرکت ارائه بدی.
    '''
        response += openAI(prompt, rule)
        response += 'end first'
        prompt = f'''
در بخش تحلیل ترازنامه و ساختار سرمایه الف) ساختار ترازنامه بر اساس اطلاعاتی که بهت میدم با فرمتی که بهت میگم اطلاعات رو نمایش بده
در قالب یک جدول با توجه به مثال و اطلاعات داده شده یک جدول کامل بهم ارائه بده
(مثال: دارایی جاری در ستون عنوان و 8000 در ستون قیمت (ملیون ریال))برای سایر اطلاعات هم این روند رو ادامه بده,
برای بخش ب) تحلیل ساختار سرمایه هم از اطلاعات زیر استفاده کن ولی اطلاعات رو به فرم زیر بهم بده:
در قالب یک جدول با ستون های نسبت، فرمول، مقدار و تفسیر که در هر ستون مانند مثال موارد خواسته شده رو قرار بده:
در ستون نسبت: نسبت بدهی به دارایی، در ستون فرمول: مقدار بدهی رو بر مقدار دارایی تقسیم کن، در بخش مقدار: حاصل تقسیم بدهی تقسیم بر دارایی، تفسیر: یک خط 10 کلمه ای تفسیر بر اساس اعداد بدست آمده) در ادامه برای "نسبت بدهی به حقوق صاحبان سهام" و "نسبت حقوق صاحبان سهام به دارایی" هم همین روند رو انجام بده.
اطلاعات ترازنامه در پایین ارسال میشود:
{'\n'.join(messages)}
'''
        response += openAI(prompt, rule)
        prompt = f'''
در بخش نسبت های مالی کلیدی الف)نسبت‌های نقدینگی بر اساس اطلاعاتی که بهت میدم با فرمتی که بهت میگم اطلاعات رو نمایش بده
در قالب یک جدول با توحه به مثال و اطلاعات داده شده یک جدول کامل بهم ارائه بده
(مثال: در ستون نسبت:جاری, در ستون فرمول: دارایی جاری رو تقسیم بر بدهی جاری کن, در ستون مقدار: حاصل تقسیم دارایی جاری بر بدهی جاری رو بنویس,تفسیر: یک خط 10 کلمه ای تفسیر بر اساس اعداد بدست آمده) در ادامه برای "آنی (سریع)" و "نسبت نقدی" هم همین روند رو انجام بده
برای بخش ب) نسبت های سود آوری بر اساس همین اطلاعات با فرمتی که بهت میگم اطلاعات رو نمایش بده
در قالب یک جدول با توحه به مثال و اطلاعات داده شده یک جدول کامل بهم ارائه بده
(مثال: در ستون نسبت:حاشیه سود ناخالص, در ستون فرمول: مجموع دارایی ها رو تقسیم بر دارایی جاری کن, در ستون مقدار: حاصل تقسیم مجموع دارایی ها بر دارایی جاری رو به درصد بنویس,تفسیر: یک خط 10 کلمه ای تفسیر بر اساس اعداد بدست آمده) در ادامه برای "حاشیه سود خالص" و "بازده دارایی (ROA)" و "بازده حقوق صاحبان سهام (ROE)" هم همین روند رو انجام بده
برای بخش ج) نسبت‌های کارایی  بر اساس همین اطلاعات با فرمتی که بهت میگم اطلاعات رو نمایش بده
در قالب یک جدول با توحه به مثال و اطلاعات داده شده یک جدول کامل بهم ارائه بده
(مثال: در ستون نسبت:گردش موجودی کالا, در ستون فرمول: دارایی غیر جاری رو تقسیم بر موجودی کالا کن, در ستون مقدار: حاصل تقسیم دارایی غیر جاری بر موجودی کالا,تفسیر: یک خط 10 کلمه ای تفسیر بر اساس اعداد بدست آمده) در ادامه برای "گردش حسای های دریافتی" هم همین روند رو انجام بده


اطلاعات ترازنامه در پایین ارسال میشود:
{'\n'.join(messages)}
        
        '''

        response += openAI(prompt, rule)
        prompt = f'''
        برای بخش تحلیل صورت سود و زیان با توجه به اطلاعاتی که برات ارسال میشه با فرمتی که بهت میگم اطلاعات رو نمایش بده
در قالب یک جدول با توجه به مثال و اطلاعات داده شده یک جدول کامل بهم ارائه بده
(مثال:فروش خالص در ستون عنوان و 20000 در ستون قیمت (میلیون ریال))برای سایر اطلاعات هم این روند رو ادامه بده,
همچنین یک تحلیل کلی از وضعیت شرکت، زیر جدولی که تهیه کرده برام با عنوان "تحلیل کلی:"، با 60 کلمه برام بنویس.
اطلاعات عمومی در پایین ارسال میشود:
{'\n'.join(messages)}
'''
        response += openAI(prompt, rule)
        prompt = f'''
        بر اساس اطلاعاتی که برای ارسال میشه بهم مقادیری که میخوام رو در یک جدول نشون بده.
اول جریان نقد عملیاتی، سرمایه گذاری، جریان تامین مالی و مانده پایان دوره رو حساب کن مقادیرشون رو.
بعد در قالب جدول مثل مثال زیر اطلاعات رو نمایش بده:
(مثال: در ستون بخش: "جریان نقد"- در ستون مبلغ: 2000- و در قسمت تقسیر، یک تفسیر در مورد ردیفی که توی جدول تهیه کردی با 15 کلمه)
در پایین جدول با عنوان "تحلیل کلی:" یک تحلیل کلی از جدول در حد 60 کلمه بهم بده.
درنهایت جدول و تحلیل رو فقط بهم نشون بده.
اطلاعات :
{'\n'.join(messages)}

'''
        response += openAI(prompt, rule)
        prompt = f'''
        
برای بخش تحلیل مدل Z آلتمن (Z-Score):
ابتدا عنوان "تحلیل مدل Z آلتمن (Z-Score)" رو بنویس و سپس:
با توجه به اطلاعات، ابتدا مقدار Z رو نمایش بده.
پایین مقدار نهایی z، یک تفسیر 60 کلمه ای برای این مقدار بهم بده.
مقادیر محاسبه X1، X2،  X3، X4، X5  رو اصلا نمایش نده و فقط مقدار نهایی Z رو نشون بده.
فرمول Z-Score برای شرکت‌های غیر بورسی:
Z=0.717X1 +0.847X2 +3.107X3+0.420X4 +0.998X5
اطلاعات:
X1=(داراییجاری−بدهیجاری)/کلدارایی
X2 = سود انباشته/ کل دارایی
X3 = سود عملیاتی / کل دارایی
X4 = ارزشدفتریحقوقصاحبانسهام/بدهی
X5 = فروش / کلدارایی

مقادیر به شکل زیرند:
{'\n'.join(messages)}
'''
        response += openAI(prompt, rule)
        prompt = f'''
        برای بخش ارزیابی کلی اعتباری:
ابتدا عنوان "ارزیابی کلی اعتباری" رو بنویس و سپس:
بر اساس اطلاعاتی که در ادامه بهت میدم یک ارزیابی کلی انجام بده و یک جدول در قالب زیر بهم بده:
(مثال: در ستون معیار: وضعیت نقدینگی, در ستون ارزیابی: نتیجه ارزیابی خود را بر اساس اطلاعات داده شده در حداکثر 5 کلمه بنویس) برای معیار های "سوآوری"و "جریان نقد" و "بدهی و تعهدات" و 
"چک برگشتی و سوابق بانکی" و " تسهیلات فعال" و 
"مدل z آلتمن " نیز انجام بده
در نهایت هم یک نتیجه کلی در حد 250 کلمه بهم بده.

مقادیر به شکل زیر است:
{'\n'.join(messages)}
'''

        response += openAI(prompt, rule)
        print(response)
        result_data = response
        questionnaire.report = result_data
        questionnaire.is_paid = True
        questionnaire.save()
        report_obj.result = result_data
        report_obj.status = 'done'
        report_obj.save()

    except Report.DoesNotExist:
        return
