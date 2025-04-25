from django.db import IntegrityError
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from django.apps import apps
from areze_yab.serializers import *
import openai
from django.db.models import Avg

openai.api_key = "توکن_API_تو"


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        company_domain = data['company_domain']
        if not data:
            return Response(data={'No data provided'}, status=status.HTTP_400_BAD_REQUEST)
        if data['password'] != data['repeatPassword']:
            return Response({'error': 'رمز عبور و تکرار آن با هم برابر نیست'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            if serializer.data['is_company']:
                try:
                    user = CustomUser.objects.get(id=serializer.data['id'])
                    company = Company.objects.create(name=serializer.data['name'],
                                                     registrationNumber=serializer.data['registrationNumber'],
                                                     nationalID=serializer.data['username'], size=request.data['size'],
                                                     company_domain=company_domain)
                    company.user.add(CustomUser.objects.get(id=serializer.data['id']))
                except IntegrityError as e:
                    return Response({'error': _('Company creation failed: {}').format(str(e))},
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response(data={"user id missing"}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyAPIView(APIView):
    def post(self, request):
        userid = request.data['userid']
        company_data = request.data['company']

        if not userid:
            return Response(data={'user id missing'}, status=status.HTTP_400_BAD_REQUEST)
        if not company_data:
            return Response(data={"error": "Company is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(id=userid)
        if not user.is_company:
            company = Company.objects.create(name=company_data['name'],
                                             registrationNumber=company_data['registrationNumber'],
                                             nationalID=company_data['nationalID'], size=company_data['size'],
                                             company_domain=company_data['company_domain'])
            company.user.add(user)
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)


class HistoryViewSet(ViewSet):

    def Mentor(self, request, nationalID):
        try:
            user = CustomUser.objects.get(nationalID=nationalID)
        except:
            return Response(data={'user id missing'}, status=status.HTTP_400_BAD_REQUEST)
        return UserSerializer(user).data

    @action(detail=False, methods=['get'])
    def All(self, request):
        objects = []
        nationalID = request.query_params.get('nationalID')
        is_company = request.query_params.get('is_Company')
        if not nationalID:
            return Response(data={"user_id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(username=nationalID)
        except CustomUser.DoesNotExist:
            return Response({"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)
        companies = CompanySerializer(Company.objects.filter(user=user), many=True).data
        for company in companies:
            companyID = company['id']
            objects.append(
                SalesAndMarketingSSerializer(SalesAndMarketingS.objects.filter(company_id=companyID), many=True).data)
            objects.append(
                SalesAndMarketingMSerializer(SalesAndMarketingM.objects.filter(company_id=companyID), many=True).data)
            objects.append(
                SalesAndMarketingLSerializer(SalesAndMarketingL.objects.filter(company_id=companyID), many=True).data)
            objects.append(BrandingSSerializer(BrandingS.objects.filter(company_id=companyID), many=True).data)
            objects.append(BrandingMSerializer(BrandingM.objects.filter(company_id=companyID), many=True).data)
            objects.append(BrandingLSerializer(BrandingL.objects.filter(company_id=companyID), many=True).data)
            objects.append(HumanResourcesSSerializer(HumanResourcesS.objects.filter(company_id=companyID),
                                                     many=True).data)
            objects.append(HumanResourcesLSerializer(HumanResourcesL.objects.filter(company_id=companyID),
                                                     many=True).data)
            objects.append(HumanResourcesMSerializer(HumanResourcesM.objects.filter(company_id=companyID),
                                                     many=True).data)
        if not bool(is_company):
            mentor = dict(self.Mentor(request, nationalID))
            return Response(data={
                "History": objects,
                "Companies": companies,
                "mentors": mentor
            }, status=status.HTTP_200_OK)
        return Response(data={
            "History": objects,
            "Companies": companies,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def Companyies(self, request):
        registrationNumber = request.query_params.get('nationalID')
        if not registrationNumber:
            return Response(data={"nationalID doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        companies = Company.objects.filter(nationalID=registrationNumber)
        serializer = CompanySerializer(companies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def DomainFilter(self, request):
        objects = []
        registrationNumber = request.query_params.get('nationalID')
        domain = request.query_params.get('domain')
        if not registrationNumber or not domain:
            return Response(data={"nationalID or domain doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        companies = Company.objects.filter(nationalID=registrationNumber)
        modelclass = apps.get_model('areze_yab', domain)
        for company in companies:
            objects.append(modelclass.objects.filter(company=company))
        return Response(data=objects, status=status.HTTP_200_OK)


class BaseAPIView(APIView):
    small_serializer_class = None
    medium_serializer_class = None
    large_serializer_class = None
    small_subdomains = None
    medium_subdomains = None
    large_subdomains = None
    domain = None
    finall = None
    small_model_class = None
    medium_model_class = None
    large_model_class = None
    small_questions = None
    medium_questions = None
    large_questions = None
    small_numeric_fields = None
    medium_numeric_fields = None
    large_numeric_fields = None

    def put(self, request):
        data = request.data
        nationalID = request.data['nationalID']
        if not nationalID:
            return Response(data={"error": "nationalID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.data['userid']
        answer = request.data['answer']
        size = request.data['size']
        if size == 'کوچک':
            serializer_class = self.small_serializer_class
        elif size == 'متوسط':
            serializer_class = self.medium_serializer_class
        elif size == 'یزرگ':
            serializer_class = self.large_serializer_class
        else:
            return Response(data={"error": "some error with size"}, status=status.HTTP_400_BAD_REQUEST)
        if not user_id:
            return Response(data={"error": "userid is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(data={"error": "userid does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(user=user, nationalID=nationalID)
        except Company.DoesNotExist:
            return Response(data={"error": "Company does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if answer is valid (you can add more validation here if needed)
        if not isinstance(answer, dict):
            return Response(data={"error": "answer must be a dictionary"}, status=status.HTTP_400_BAD_REQUEST)

        # Set company ID
        request.data['company'] = {
            "id": company.id,
            "name": company.name,
            "company_domain": company.company_domain,
            "nationalID": company.nationalID,
            "registrationNumber": company.registrationNumber,
            "size": company.size,
            "user": user.id
        }

        first_key = list(answer.keys())[0]  # گرفتن اولین کلید دیکشنری

        # بررسی اینکه آیا اولین کلید برابر با final است
        if first_key == self.finall:
            # انجام کاری که می‌خواهید وقتی اولین کلید برابر با final باشد
            data['is_draft'] = False

        serializer = serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        nationalID = request.query_params.get('nationalID')
        if not nationalID:
            return Response(data={"error": "nationalID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.query_params.get('userid')
        if not user_id:
            return Response(data={"error": "userid is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(data={"error": "userid does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(user=user, nationalID=nationalID)
            company_serializer = CompanySerializer(company)
        except Company.DoesNotExist:
            return Response(data={"error": "Company does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        size = request.data['size']
        if size == 'کوچک':
            serializer_class = self.small_serializer_class
            model_class = self.small_model_class
            subdomains = self.small_subdomains
            questions = self.small_questions
            numeric_fields = self.small_numeric_fields
        elif size == 'متوسط':
            serializer_class = self.medium_serializer_class
            model_class = self.medium_model_class
            subdomains = self.medium_subdomains
            questions = self.medium_questions
            numeric_fields = self.medium_numeric_fields
        elif size == 'یزرگ':
            serializer_class = self.large_serializer_class
            model_class = self.large_model_class
            subdomains = self.large_subdomains
            questions = self.large_questions
            numeric_fields = self.large_numeric_fields
        else:
            return Response(data={"error": "some error with size"}, status=status.HTTP_400_BAD_REQUEST)
        results = {}
        answers = model_class.objects.filter(company=company).last()

        results = {}

        for subdomain, fields in subdomains.items():
            values = [getattr(answers, field, None) for field in fields]

            subdomain_results = {}
            for question, value in zip(questions[subdomain], values):
                subdomain_results[question] = value

            results[subdomain] = subdomain_results

        prompt = ''

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"تصور کن به عنوان یک کارشناس در حوزه {self.domain} قصد داری {self.domain} یک شرکت با مقیاس {company.size} را عارضه یابی کنی"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response = response['choices'][0]['message']['content']

        avg_values = {}

        # محاسبه میانگین برای هر فیلد
        for field in numeric_fields:
            avg_value = model_class.objects.aggregate(avg_value=Avg(field))
            avg_values[field] = avg_value['avg_value']

        return Response({
            "company": company_serializer.data,
            "domain": self.domain,
            "overallScore": avg_values,
            "response": response,
        }, status=status.HTTP_200_OK)


class SalesAndMarketingAPIView(BaseAPIView):
    small_serializer_class = SalesAndMarketingSSerializer
    medium_serializer_class = SalesAndMarketingMSerializer
    large_serializer_class = SalesAndMarketingLSerializer
    small_model_class = SalesAndMarketingS
    medium_model_class = SalesAndMarketingM
    large_model_class = SalesAndMarketingL
    small_questions = {
        "استراتژی فروش": [
            "13.\tآیا کارکنان شما در انجام وظایف خود به اخلاق حرفه\u200Cای پایبند هستند؟  \n(اخلاق حرفه\u200Cای: رعایت استانداردهای شغلی، تعهد، درستکاری و مسئولیت\u200Cپذیری در محیط کار)\n",
            "1. آیا استراتژی فروش مشخص و مستندی برای شرکت شما وجود دارد؟(استراتژی فروش: برنامه مکتوب و دقیق برای هدایت فعالیت\u200Cهای فروش با هدف دستیابی به بازار و افزایش درآمد)"],
        "فرآیند فروش": ["2. آیا استراتژی فروش شما با اهداف شرکت هم\u200Cراستا است؟",
                        "3. آیا فرایند فروش شما به صورت شفاف و مستند تعریف شده است؟(فرایند فروش: مراحلی که از جذب مشتری تا نهایی کردن فروش طی می\u200Cشود)"],
        "تیم فروش": ["4. آیا مراحل پیگیری مشتریان پس از فروش به\u200Cطور منظم انجام می\u200Cشود؟",
                     "5. آیا تیم فروش شما از نظر تعداد و تخصص مناسب است؟(تخصص تیم فروش: مهارت و دانش لازم برای ارتباط مؤثر با مشتری و بستن قرارداد فروش)"],
        "تحلیل بازار": [
            "6. آیا برنامه آموزشی برای تیم فروش وجود دارد؟(آموزش تیم فروش: دوره\u200Cهای آموزشی تخصصی برای افزایش مهارت و به\u200Cروز بودن اطلاعات تیم فروش)",
            "7. آیا تحلیل بازار به\u200Cطور منظم برای تعیین فرصت\u200Cها و تهدیدهای جدید انجام می\u200Cشود؟(تحلیل بازار: بررسی تغییرات نیازهای مشتری، رقبا و روندهای بازار به صورت سیستماتیک)"],
        'مدیریت ارتباط با مشتری': [
            "8. آیا شما در انتخاب بازار هدف، اطلاعات دقیق و به\u200Cروز دارید؟(بازار هدف: گروه مشخصی از مشتریان که محصولات یا خدمات شرکت برای آن\u200Cها طراحی شده است)",
            "9. آیا شما از نرم\u200Cافزار یا سیستمی برای مدیریت ارتباطات با مشتریان استفاده می\u200Cکنید؟(CRM: ابزار یا فرآیندی برای ثبت، پیگیری و مدیریت ارتباطات با مشتریان)"],
        "بازار یابی دیجیتال": [
            "10. آیا شما به\u200Cطور منظم اطلاعات مشتریان و تجربیات آن\u200Cها را بررسی و تجزیه\u200Cوتحلیل می\u200Cکنید؟(تحلیل داده\u200Cهای مشتری: تحلیل رفتار خرید، بازخوردها و رضایت مشتری برای بهبود فروش)",
            "11. آیا شما از ابزارهای بازاریابی دیجیتال مانند شبکه\u200Cهای اجتماعی، ایمیل مارکتینگ و تبلیغات آنلاین استفاده می\u200Cکنید؟(بازاریابی دیجیتال: استفاده از بسترهای آنلاین برای معرفی محصولات، جذب مشتری و افزایش فروش)"],
        "نبلیغ و ترویج فروش": [
            "12. آیا فعالیت\u200Cهای بازاریابی دیجیتال شما با استراتژی کلی فروش هم\u200Cراستا است؟(هم\u200Cراستایی بازاریابی دیجیتال: تطابق بین محتوای آنلاین، تبلیغات و اهداف فروش شرکت)"]
    }
    medium_questions = {
        "استراتژی فروش": [
            "1.آیا استراتژی فروش شما به\u200Cطور منظم بروزرسانی می\u200Cشود؟ (استراتژی فروش: برنامه\u200Cریزی منسجم برای هدایت تیم فروش به سوی اهداف مشخص در بازار هدف)",
            "2.آیا استراتژی فروش شما برای تمام بخش\u200Cهای بازار هدف مناسب است؟",
            "3.آیا استراتژی فروش شما شامل تعیین اهداف کوتاه\u200Cمدت و بلندمدت است؟",
            "4.آیا فرایند فروش شما به\u200Cطور مستند و شفاف برای تمام اعضای تیم فروش تدوین شده است؟"],
        "فرآیند فروش": ["5.آیا از نرم\u200Cافزارهای خاص برای مدیریت و پیگیری فرایند فروش استفاده می\u200Cکنید؟",
                        "6.آیا فرایند فروش شما قابلیت انعطاف\u200Cپذیری در مواجهه با تغییرات بازار را دارد؟",
                        "7.آیا شما از تحلیل\u200Cهای داده\u200Cای برای بهبود فرایند فروش استفاده می\u200Cکنید؟",
                        "8.آیا اعضای تیم فروش شما بر اساس عملکرد خود به\u200Cطور مرتب ارزیابی می\u200Cشوند؟(ارزیابی عملکرد: بررسی منظم عملکرد فروشندگان بر اساس اهداف و شاخص\u200Cهای مشخص)"],
        "تیم فروش": [
            "9.آیا اعضای تیم فروش شما به\u200Cطور مستمر برای بهبود مهارت\u200Cهای فروش خود آموزش می\u200Cبینند؟",
            "10.آیا اهداف فروش تیم شما با اهداف کلی شرکت هم\u200Cراستا است؟",
            "11.آیا تیم فروش شما به\u200Cطور منظم بازخورد و مشاوره از مدیران دریافت می\u200Cکند؟",
            "12.آیا شما تحلیل\u200Cهای بازار را به\u200Cطور منظم انجام می\u200Cدهید؟"],
        "تحلیل بازار": [
            "13.آیا شما رقبا را به\u200Cطور دقیق تحلیل کرده و از اطلاعات آن\u200Cها برای استراتژی فروش خود استفاده می\u200Cکنید؟",
            "14.آیا در تحلیل\u200Cهای بازار خود به نیازهای جدید و تغییرات تقاضا توجه می\u200Cکنید؟",
            "15.آیا شما از یک سیستم CRM پیشرفته برای مدیریت ارتباط با مشتریان استفاده می\u200Cکنید؟"],
        'مدیریت ارتباط با مشتری': ["16.آیا سیستم CRM شما قابلیت تحلیل داده\u200Cهای مشتری و رفتار آن\u200Cها را دارد؟",
                                   "17.آیا شما از ابزارهای تحلیل دیجیتال برای ارزیابی کمپین\u200Cهای بازاریابی دیجیتال خود استفاده می\u200Cکنید؟"],
        "بازار یابی دیجیتال": [
            "18.آیا فعالیت\u200Cهای بازاریابی دیجیتال شما بر اساس داده\u200Cهای به\u200Cدست\u200Cآمده از تحلیل\u200Cهای دیجیتال بهینه\u200Cسازی می\u200Cشود؟",
            "19.آیا شما به\u200Cطور منظم تبلیغات هدفمند برای جذب مشتریان جدید انجام می\u200Cدهید؟"],
        "نبلیغ و ترویج فروش": ["20.آیا شما از تخفیف\u200Cها و پیشنهادات ویژه برای ترویج فروش استفاده می\u200Cکنید؟"]
    }
    large_questions = {
        "استراتژی فروش": [
            "1. آیا استراتژی فروش شما شامل کانال\u200Cهای مختلف (آنلاین، آفلاین، شرکاء) است؟(استراتژی کانال: بهره\u200Cبرداری همزمان و هدفمند از چند کانال توزیع و فروش برای پوشش کامل بازار)",
            "2. آیا استراتژی فروش شما در هر بازار هدف به طور خاص تنظیم شده است؟(بازار هدف: بخش خاصی از مشتریان که با ویژگی\u200Cهای جمعیت\u200Cشناختی یا رفتاری مشخص تعریف شده\u200Cاند)",
            "3. آیا استراتژی فروش شما شامل برنامه\u200Cهای خاص برای توسعه بازارهای جدید است؟(توسعه بازار: ورود به مناطق جغرافیایی جدید یا جذب مشتریان با ویژگی\u200Cهای متفاوت از بازار فعلی)",
            "4. آیا فرآیند فروش شما به\u200Cطور خودکار برای بهبود کارایی و کاهش خطاها طراحی شده است؟(خودکارسازی فروش: استفاده از نرم\u200Cافزار و ابزارهای دیجیتال برای تسهیل مراحل فروش)"],
        "فرآیند فروش": [
            "5. آیا برای هر مرحله از فرآیند فروش شاخص\u200Cهای عملکرد (KPIs) تعریف شده است؟(KPI: معیارهای سنجش موفقیت در هر مرحله از فرآیند فروش مانند نرخ تبدیل، مدت زمان چرخه فروش، میزان فروش فردی و غیره)",
            "6. آیا فرآیند فروش شما به\u200Cطور منظم مورد ارزیابی و بهبود قرار می\u200Cگیرد؟(ارزیابی فروش: بازنگری ساختاری در روندهای فروش بر اساس داده\u200Cها و بازخوردها)",
            "7. آیا اعضای تیم فروش شما به\u200Cطور مرتب از تجربیات بازار و بازخوردهای مشتریان برای بهبود استراتژی فروش استفاده می\u200Cکنند؟(یادگیری از بازار: استفاده عملی از بازخورد مشتریان برای تنظیم و اصلاح فرآیندها و رویکردهای فروش)"],
        "تیم فروش": [
            "8. آیا برنامه\u200Cهای انگیزشی متناسب با عملکرد فروش برای تیم وجود دارد؟(برنامه انگیزشی: سیستم\u200Cهای پاداش\u200Cدهی مالی یا غیرمالی مرتبط با اهداف فروش)",
            "9. آیا آموزش\u200Cهای تخصصی فروش برای تیم به\u200Cطور مستمر ارائه می\u200Cشود؟(آموزش فروش: دوره\u200Cهای مهارت\u200Cافزایی در حوزه محصول، بازار، تکنیک\u200Cهای فروش، نرم\u200Cافزارهای CRM و مدیریت ارتباط با مشتری)",
            "10. آیا در تحلیل بازار از ابزارهای پیشرفته مانند تحلیل رقابتی، داده\u200Cهای کلان و مدل\u200Cهای پیش\u200Cبینی استفاده می\u200Cکنید؟(تحلیل بازار پیشرفته: استفاده از نرم\u200Cافزارهای تحلیلی، پایگاه\u200Cهای داده و مدل\u200Cهای پیش\u200Cبینی رفتار مشتریان)"],
        "تحلیل بازار": [
            "11. آیا بازارهای جدید با داده\u200Cهای جدید و تحلیل\u200Cهای به\u200Cروز شناسایی می\u200Cشوند؟(تحلیل بازار جدید: کشف فرصت\u200Cهای فروش جدید با استفاده از تحلیل مستمر داده\u200Cهای به\u200Cروز و اطلاعات رقابتی)",
            "12. آیا سیستم CRM شما به\u200Cطور یکپارچه با دیگر سیستم\u200Cهای سازمانی مانند حسابداری، پشتیبانی و فروش در ارتباط است؟(یکپارچگی سیستم\u200Cها: قابلیت تبادل خودکار اطلاعات میان سیستم\u200Cهای مختلف سازمان برای افزایش بهره\u200Cوری و کاهش خطا) "],
        'مدیریت ارتباط با مشتری': [
            "13. آیا سیستم CRM به\u200Cطور فعال اطلاعات مشتری را در زمان واقعی به\u200Cروزرسانی می\u200Cکند؟(به\u200Cروزرسانی در زمان واقعی: تغییرات اطلاعات مشتری بلافاصله در دسترس همه بخش\u200Cها قرار می\u200Cگیرد)",
            "14. آیا شما از ابزارهای پیشرفته بازاریابی دیجیتال (مانند A/B تست، بازاریابی مبتنی بر داده) استفاده می\u200Cکنید؟(بازاریابی دیجیتال پیشرفته: بهره\u200Cگیری از ابزارهای علمی و تحلیلی برای طراحی و بهینه\u200Cسازی کمپین\u200Cهای دیجیتال)"],
        "بازار یابی دیجیتال": [
            "15. آیا شما کمپین\u200Cهای دیجیتال خود را به\u200Cطور مستمر برای بهینه\u200Cسازی بر اساس تجزیه\u200Cوتحلیل داده\u200Cها تنظیم می\u200Cکنید؟(بهینه\u200Cسازی کمپین: تنظیم مستمر تبلیغات، محتوا و هدف\u200Cگذاری براساس نتایج و داده\u200Cهای واقعی بازار)",
            "16. آیا کمپین\u200Cهای تبلیغاتی شما به\u200Cطور مؤثر با مشتریان هدف شما هم\u200Cراستا است؟(هم\u200Cراستایی تبلیغات با مخاطب هدف: تطابق پیام، زبان، تصویر و رسانه با پرسونای دقیق مشتریان)"],
        "نبلیغ و ترویج فروش": [
            "17. آیا شما تبلیغات خود را بر اساس تغییرات نیازهای مشتریان به\u200Cطور مداوم تطبیق می\u200Cدهید؟(تطبیق تبلیغات: تنظیم پیام و محتوا بر اساس تغییرات بازار و نیازهای به\u200Cروز مشتریان)"]
    }
    small_subdomains = {
        "استراتژی فروش": ["staffing_sufficiency",
                          "recruitment_planning"],
        "فرآیند فروش": ["employee_turnover_rate"
            , "employee_turnover_reasons_attention"],
        "تیم فروش": ["employee_performance_evaluation",
                     "employee_productivity_tool"],
        "تحلیل بازار": ["performance_evaluation_impact",
                        "employee_training_programs"],
        'مدیریت ارتباط با مشتری': ["training_impact_on_performance",
                                   "employee_collaboration_effectiveness"],
        "بازار یابی دیجیتال": ["teamwork_culture_exists",
                               "ethical_standards_attention"],
        "نبلیغ و ترویج فروش": ["employee_professional_ethics"]

    }

    medium_subdomains = {
        "استراتژی فروش": ["regular_sales_strategy_updates",
                          "sales_strategy_suitability_for_target_segments",
                          "sales_strategy_with_short_long_term_goals",
                          "automated_sales_process_for_efficiency_and_error_reduction"],
        "فرآیند فروش": ["documented_transparent_sales_process_for_team",
                        "using_specialized_software_for_sales_process_management"
                        "sales_process_flexibility_for_market_changes ",
                        "using_data_analytics_to_improve_sales_process"],

        "تیم فروش": ["regular_evaluation_of_sales_team_based_on_performance",
                     "continuous_training_for_sales_team_skills",
                     "sales_team_goals_alignment_with_company_goals",
                     "regular_feedback_and_coaching_for_sales_team"],
        "تحلیل بازار": ["regular_market_analysis",
                        "competitor_analysis_and_using_data_for_sales_strategy",
                        "market_analysis_attention_to_new_needs_and_demand_changes", ],
        'مدیریت ارتباط با مشتری': [
            "advanced_crm_system_for_customer_relationship_management",
            "crm_system_ability_to_analyze_customer_data_and_behavior",
        ],
        "بازار یابی دیجیتال": ["digital_analytics_tools_for_evaluating_marketing_campaigns",
                               "optimizing_digital_marketing_based_on_analytics_data", ],
        "نبلیغ و ترویج فروش": [
            "regular_targeted_advertising_for_new_customers",
            "using_discounts_and_special_offers_for_sales_promotion", ]

    }
    large_subdomains = {
        "استراتژی فروش": ["sales_strategy_including_multiple_channels_online_offline_partners",
                          "sales_strategy_tailored_for_each_target_market",
                          "sales_strategy_with_plans_for_new_market_development",
                          "automated_sales_process_for_efficiency_and_error_reduction"],
        "فرآیند فروش": ["kpis_defined_for_each_stage_of_sales_process",
                        "regular_evaluation_and_improvement_of_sales_process",
                        "using_market_experiences_and_customer_feedback_for_sales_strategy_improvement"],
        "تیم فروش": ["performance_based_motivational_programs_for_sales_team",
                     "continuous_sales_training_for_team",
                     "advanced_market_analysis_tools"],
        "تحلیل بازار": ["identifying_new_markets_with_updated_data",
                        "crm_integrated_with_other_systems"],
        'مدیریت ارتباط با مشتری': ["crm_real_time_customer_data_update",
                                   "advanced_digital_marketing_tools_usage", ],
        "بازار یابی دیجیتال": [
            "digital_campaign_optimization_based_on_data_analysis",
            "advertising_campaign_alignment_with_target_customers", ],
        "نبلیغ و ترویج فروش": [
            "advertising_adjustment_based_on_customer_needs", ]
    }
    domain = "فروش و مارکتینگ"
    finall = 'exportActivitiesAndGlobalMarketUse'


class HumanResourceAPIView(BaseAPIView):
    small_serializer_class = HumanResourcesSSerializer
    medium_serializer_class = HumanResourcesMSerializer
    small_model_class = HumanResourcesS
    medium_model_class = HumanResourcesM
    domain = "منابع انسانی"
    small_questions = {
        "تعداد نیروی انسانی": [
            "1.\tآیا تعداد نیروی انسانی شما برای انجام وظایف روزمره کافی است؟  \n(منظور: نسبت تعداد نیروی انسانی به حجم کار، بدون ایجاد فشار شغلی یا کندی در انجام وظایف)\n",
            "2.\tآیا شما برای جذب نیروی انسانی جدید برنامه\u200Cریزی می\u200Cکنید؟  \n(برنامه\u200Cریزی جذب نیرو: پیش\u200Cبینی نیازهای منابع انسانی با توجه به توسعه کسب\u200Cوکار و برنامه\u200Cهای استخدامی)\n"],
        "ماندگاری نیروی انسانی": [
            "3.\tآیا شما نرخ بالای ترک خدمت کارکنان را تجربه می\u200Cکنید؟  \n(نرخ ماندگاری: نسبت کارکنان فعلی به مجموع افراد جذب\u200Cشده طی یک دوره مشخص)\n",
            "4.\tآیا به\u200Cطور منظم به دلایل ترک خدمت کارکنان توجه می\u200Cکنید؟  \n(تحلیل ترک خدمت: بررسی دلایل خروج افراد برای کاهش ریسک از دست دادن منابع انسانی)\n"],
        "سیستم و ارزیابی عملکرد کارکنان": [
            "5.\tآیا شما سیستم ارزیابی عملکرد منظم برای کارکنان دارید؟  \n(سیستم ارزیابی عملکرد: فرآیند سازمان\u200Cیافته برای بررسی و تحلیل کیفیت و میزان دستاوردهای کارکنان نسبت به اهداف شغلی)\n",
            "6.آیا بهره\u200Cوری کارکنان شما به طور منظم ارزیابی می\u200Cشود؟\n(ارزیابی منظم بهره\u200Cوری: برنامه\u200Cریزی دوره\u200Cای برای بررسی عملکرد کارکنان و تعیین نقاط قوت و ضعف)",
            "7.\tآیا ارزیابی عملکرد کارکنان بر تصمیمات مدیریتی تأثیر دارد؟  \n(ارزیابی عملکرد: بررسی منظم و ساختارمند میزان تحقق اهداف، مهارت\u200Cها و رفتارهای کارکنان و استفاده از نتایج آن در تصمیم\u200Cگیری مدیریتی)\n"],
        "سیستم و آموزش کارکنان": [
            "8.\tآیا شما برنامه\u200Cهای آموزشی برای کارکنان خود دارید؟  \n(برنامه\u200Cهای آموزشی: مجموعه دوره\u200Cهای مهارتی و دانشی که به\u200Cمنظور ارتقاء کیفیت کار و توسعه حرفه\u200Cای کارکنان برگزار می\u200Cشود)\n",
            "9.\tآیا برنامه\u200Cهای آموزشی شما بر بهبود عملکرد کارکنان تأثیرگذار بوده است؟  \n(تأثیر آموزش: سنجش میزان تغییر در رفتار کاری، مهارت و بهره\u200Cوری کارکنان پس از دوره\u200Cهای آموزشی)\n"],
        "همکاری و کار گروهی": [
            "10.\tآیا کارکنان شما به\u200Cطور مؤثر با یکدیگر همکاری می\u200Cکنند؟  \n(همکاری مؤثر: تعامل سازنده میان اعضای تیم برای دستیابی به اهداف مشترک)\n",
            "11.\tآیا در شرکت شما فرهنگ کار تیمی وجود دارد؟  \n(فرهنگ کار تیمی: باور و رفتارهای سازمانی که موجب تشویق به همکاری، همدلی و تلاش جمعی در محیط کار می\u200Cشود)\n"],
        "توجه به ارزش ها اخلاقی": [
            "12.\tآیا در شرکت شما به اصول اخلاقی توجه ویژه\u200Cای می\u200Cشود؟  \n(اصول اخلاقی: رعایت رفتار منصفانه، شفافیت، صداقت و مسئولیت\u200Cپذیری در تمام سطوح سازمانی)\n",
            "13.\tآیا کارکنان شما در انجام وظایف خود به اخلاق حرفه\u200Cای پایبند هستند؟  \n(اخلاق حرفه\u200Cای: رعایت استانداردهای شغلی، تعهد، درستکاری و مسئولیت\u200Cپذیری در محیط کار)\n"],
    }
    medium_questions = {
        "تعداد نیرو": [
            "1.آیا تعداد کارکنان شما با حجم کاری شرکت تناسب دارد؟(منظور: تطابق تعداد نیروی انسانی با نیازهای عملیاتی شرکت)",
            "2.برنامه شما برای جذب نیروی جدید چگونه است؟(منظور: میزان برنامه\u200Cریزی و پیش\u200Cبینی در فرآیند استخدام)"],
        "ماندگاری نیروی انسانی": [
            "3.میزان تمایل کارکنان به ماندگاری در شرکت چگونه است؟(منظور: میزان رضایت و انگیزه کارکنان برای ماندن در شرکت)",
            "4.آیا دلایل خروج کارکنان بررسی می\u200Cشود؟(منظور: شناسایی علل ترک خدمت برای بهبود شرایط سازمانی)",
            "5.آیا برای نگهداشت نیروهای کلیدی برنامه دارید؟(منظور: برنامه\u200Cریزی برای حفظ کارکنان با ارزش و حیاتی)"],
        "بهره وری پرسنل‌": [
            "7.چه کسی بهره\u200Cوری کارکنان را بررسی می\u200Cکند؟(منظور: مسئولیت پایش و سنجش عملکرد کارکنان)",
            "9.آیا سیستم ارزیابی عملکرد ساختار یافته دارید؟(منظور: وجود یک فرآیند منظم، مستند و دوره\u200Cای برای ارزیابی عملکرد)",
            "10.آیا ارزیابی عملکرد بر تصمیمات حقوق و ارتقا تأثیر دارد؟(منظور: میزان ارتباط مستقیم نتایج ارزیابی با تصمیمات منابع انسانی)"],
        "سیستم ارزیابی عملکرد": [
            "11.آیا بازخورد عملکرد به کارکنان داده می\u200Cشود؟(منظور: ارائه بازخورد منظم و سازنده به کارکنان برای اصلاح یا بهبود عملکرد)",
            "12.آیا برنامه آموزشی مستمر برای کارکنان وجود دارد؟(منظور: آموزش\u200Cهای مهارت\u200Cافزایی بر اساس نیازهای شغلی و توسعه فردی)",
            "13.آیا اثر آموزش\u200Cها بررسی می\u200Cشود؟(منظور: سنجش اثربخشی دوره\u200Cهای آموزشی در بهبود عملکرد افراد)"],
        "سیستم آموزش کارکنان": [
            "14.آیا بودجه و منابع آموزشی در نظر گرفته شده است؟(منظور: برنامه\u200Cریزی سازمان برای سرمایه\u200Cگذاری روی آموزش)",
            "15.همکاری میان واحدهای مختلف شرکت چگونه است؟(منظور: میزان هماهنگی و تعامل واحدها برای انجام فعالیت\u200Cهای سازمانی)",
            "16.آیا جلسات یا برنامه\u200Cهایی برای تقویت همکاری دارید؟(منظور: وجود فرآیند رسمی برای افزایش هماهنگی و همکاری بین کارکنان و تیم\u200Cها)"],
        "همکاری و کار تیمی": [
            "17.آیا فرهنگ کار گروهی در شرکت وجود دارد؟(منظور: میزان تمایل سازمان و کارکنان به همکاری و روحیه تیمی)",
            "18.آیا اصول اخلاقی در رفتار کارکنان مشهود است؟(منظور: رعایت استانداردهای اخلاقی مانند احترام، صداقت، انصاف در ارتباطات و تصمیم\u200Cگیری\u200Cها)",
            "19.آیا مدیران الگوی رعایت اخلاق حرفه\u200Cای هستند؟(منظور: میزان مسئولیت\u200Cپذیری و رفتار اخلاقی مدیران در محیط کار)"],
        "ارزش های اخلاقی": [
            "20.آیا کد اخلاق حرفه\u200Cای یا دستورالعمل رفتاری دارید؟(منظور: وجود یک سند رسمی که انتظارات رفتاری سازمان از کارکنان را شفاف و مکتوب بیان کند)"],
    }
    large_questions = {
        "تعداد نیرو": [
            "1. آیا تعداد فعلی نیروهای شرکت با حجم کاری متناسب است؟(تناسب تعداد نیرو: میزان هماهنگی تعداد کارکنان با حجم وظایف جاری شرکت)",
            "2. آیا ساختار سازمانی شما متناسب با رشد شرکت به\u200Cروزرسانی شده است؟(ساختار سازمانی: چارت سازمانی، شرح شغل\u200Cها و روابط رسمی بین بخش\u200Cها)"],
        "ماندگاری نیروی انسانی": [
            "3. نرخ خروج نیروها از شرکت در سال گذشته چگونه بوده است؟(نرخ خروج: درصد کارکنانی که شرکت را ترک کرده\u200Cاند نسبت به کل کارکنان)",
            "4. آیا برنامه مشخصی برای افزایش رضایت و وفاداری کارکنان دارید؟(برنامه وفادارسازی: استراتژی\u200Cهای ساختاریافته برای نگهداشت نیروی انسانی)"],
        "بهره وری پرسنل‌": [
            "5. سطح بهره\u200Cوری پرسنل در بخش\u200Cهای کلیدی چگونه ارزیابی می\u200Cشود؟(بهره\u200Cوری: نسبت خروجی مؤثر به منابع و زمان مصرف\u200Cشده توسط کارکنان)",
            "6. آیا منابع و ابزار کافی برای افزایش بهره\u200Cوری در اختیار نیروها قرار گرفته است؟(منابع: ابزارهای فیزیکی، نرم\u200Cافزارها و اطلاعات مورد نیاز برای انجام کار)"],
        "سیستم ارزیابی عملکرد": [
            "7. آیا سیستم ارزیابی عملکرد کارکنان به صورت رسمی و منظم اجرا می\u200Cشود؟ (ارزیابی عملکرد: فرآیند سنجش و بررسی دوره\u200Cای عملکرد کارکنان در راستای اهداف سازمانی)",
            "8. آیا بازخورد حاصل از ارزیابی به بهبود عملکرد کارکنان منجر می\u200Cشود؟ (بازخورد مؤثر: اطلاعات کاربردی که پس از ارزیابی برای بهبود عملکرد به کارکنان داده می\u200Cشود)"],
        "سیستم آموزش کارکنان": [
            "9. آیا برنامه آموزشی ساختاریافته و دوره\u200Cای برای کارکنان وجود دارد؟ (برنامه آموزشی ساختاریافته: آموزش\u200Cهای برنامه\u200Cریزی\u200Cشده و هدفمند برای توسعه مهارت\u200Cهای کارکنان)",
            "10. آیا آموزش\u200Cها به بهبود مهارت و عملکرد کارکنان منجر شده\u200Cاند؟ (اثربخشی آموزش: تاثیر دوره\u200Cهای آموزشی در رشد و بهبود عملکرد شغلی)"],
        "همکاری و کار تیمی": [
            "11. سطح همکاری بین تیم\u200Cها و بخش\u200Cها در شرکت چگونه است؟ (همکاری بین تیمی: میزان هماهنگی و تعامل اثربخش بین بخش\u200Cهای مختلف سازمان)",
            "12. آیا اختلافات تیمی در شرکت به\u200Cدرستی مدیریت می\u200Cشود؟ (مدیریت تعارض: فرایندهای پیشگیری و حل اختلاف در سازمان)"],
        "ارزش های اخلاقی": [
            "13. ارزش\u200Cهای اخلاقی در رفتار روزمره کارکنان رعایت می\u200Cشود؟ (ارزش\u200Cهای اخلاقی: اصول اخلاقی شامل صداقت، مسئولیت\u200Cپذیری و رفتار حرفه\u200Cای در محیط کار)",
            "14. آیا در فرآیند استخدام، ارزش\u200Cهای اخلاقی سنجیده می\u200Cشود؟ (اخلاق در استخدام: ارزیابی اصول رفتاری و تعهد اخلاقی داوطلبان در کنار مهارت فنی)"],
    }
    finall = "managers_behavior_towards_men_and_women"


class FinancialResourcesAPIView(BaseAPIView):
    serializer_class = FinancialResourcesSerializer
    model_class = FinancialResources
    domain = "منابع مالی"
    subdomains = {
        "جریان نقد عملیاتی": ["ability_to_maintain_positive_cash_flow"],
        "نسبت جاری": ["ability_to_pay_financial_obligations"],
        "سرمایه در گردش": ["assets_for_short_term_financial_obligations"],
        "نرخ سوختن سرمایه": ["weekly_monthly_annual_expenses"],
        "حاشیه سود خالص": ["profitability_efficiency_comparison"],
        "بازده حساب های پرداختی": ["ability_to_pay_accounts_payable"],
        "مجموع هزینه کل عملکرد مالی": ["payment_processing_costs"],
        "نسبت هزینه کل عملکرد مالی": ["financial_activity_cost_to_income_ratio"],
        "گزارش خطلای مالی": ["financial_report_accuracy_and_completeness"],
        "انحراف بودجه": ["budget_vs_actual_difference"],
        "رشد فروش": ["sales_change_over_period"]

    }
    finall = 'sales_change_over_period'


class CapitalStructureAPIView(BaseAPIView):
    serializer_class = CapitalStructureSerializer
    model_class = CapitalStructure
    domain = "ساختار سرمایه"
    subdomains = {
        "نحوه تامین سرمایه": ["shareholder_funding_power", "availability_of_resources_for_new_projects"],
        "ریسک پذیری": ["startup_investment_risk_tolerance"]
    }
    finall = 'startup_investment_risk_tolerance'


class ManagementOrganizationalStructureAPIView(BaseAPIView):
    serializer_class = ManagementOrganizationalStructureSerializer
    model_class = ManagementOrganizationalStructure
    domain = 'ساختار مدیریتی و سازمانی'
    subdomains = {
        "چارت سازمانی": ["comprehensive_organizational_chart", "regular_chart_updates"],
        "سبستم مدیریت دانش و اطلاعات": ["information_system_for_knowledge_management",
                                        "knowledge_management_system_integration"],
        "نظام آراستگی محیط": ["workspace_design", "five_s_in_daily_operations"],
        "استراتژی و دیدگاه مدیریت": ["vision_and_mission_definition",
                                     "employee_awareness_of_long_short_term_plans",
                                     "activities_for_increasing_customer_awareness"],
        "میزان تفویض اختیار": ["decision_making_power_for_lower_employees"]
    }
    finall = 'decision_making_power_for_lower_employees'


class CustomerRelationshipManagementAPIView(BaseAPIView):
    serializer_class = CustomerRelationshipManagementSerializer
    model_class = CustomerRelationshipManagement
    domain = 'مدیریت ارتباط با مشتری'
    subdomains = {
        "سیستم بازخورد": ["purchase_info_documentation", "customer_feedback_system",
                          "customer_feedback_analysis"],
        "تسهیلات": ["special_sales_plan_for_loyal_customers", "loyal_customer_payment_benefits",
                    "first_purchase_support_plan"],
        "ماندگاری مشتری": ["employee_training_for_customer_interaction", "loyal_customer_count"]
    }
    finall = 'loyal_customer_count'


class ManufacturingAndProductionAPIView(BaseAPIView):
    serializer_class = ManufacturingAndProductionSerializer
    model_class = ManagementOrganizationalStructure
    domain = 'ساخت و تولید'
    subdomains = {
        "میزان تولید ماهیانه": ["production_increase_planning", "safety_stock_level", "storage_cost",
                                "production_stability", "max_capacity_utilization"],
        "سیستم مدیریت و تولید": ["production_process_documentation", "defect_detection_and_resolution",
                                 "production_process_flexibility"],
        "تکنولوژی تولید": ["production_technology_level", "iot_equipment_in_production_line"],
        "تولید بر اساس نیاز بازار": ["production_sales_marketing_alignment"],
        "راندمان تولید": ["output_input_ratio", "production_waste_ppm"],
        "استاندارد های ملی و بین المللی": ["required_certifications"],
        "گارانتی": ["warranty_after_sales", "warranty_commitment"],
        "سیستم کنترل کیفیت": ["quality_control_lab", "quality_control_standards"]
    }
    finall = 'quality_control_standards'


class ResearchAndDevelopmentAPIView(BaseAPIView):
    serializer_class = ResearchAndDevelopmentSerializer
    model_class = ResearchAndDevelopment
    subdomains = {
        "بهبود محصول": ["r_and_d_unit_defined_roles", "r_and_d_production_connection", "r_and_d_budget"],
        "نوآوری": ["innovation_planning", "innovation_process_guidelines",
                   "customer_competitor_inspiration", "innovation_culture"]
    }
    domain = 'تحقیق و توسعه'
    finall = 'innovation_culture'


class ProductCompetitivenessAPIView(BaseAPIView):
    serializer_class = ProductCompetitivenessSerializer
    model_class = ProductCompetitiveness
    domain = 'رفابت پذیری محصول'
    subdomains = {"مزیت رفابتی": ["unique_feature"]}
    finall = 'unique_feature'


class BrandingAPIView(BaseAPIView):
    small_serializer_class = BrandingSSerializer
    medium_serializer_class = BrandingMSerializer
    small_model_class = BrandingS
    medium_model_class = BrandingM
    domain = 'برندینگ'
    finall = "is_visual_design_of_brand_consistent"
    small_questions = {
        "هویت برند": [
            "1.\tآیا شما هویت برند واضح و مشخصی برای کسب\u200Cوکار خود تعریف کرده\u200Cاید؟ (هویت برند: اجزای قابل رویت برند از قبیل رنگ، طراحی و لوگو که با ماهیت کسب\u200Cوکار به خوبی همخوانی دارد)",
            "2.\tآیا کارکنان شما به\u200Cطور کامل با هویت برند آشنا هستند؟ (دلیل انتخاب رنگ، طرح لوگو و ماهیت مرتبط با برند را می\u200Cدانند؟)  "],
        "آگاهی از برند": ["3. آیا مشتریان شما برند شما را به\u200Cخوبی می\u200Cشناسند و به خاطر می\u200Cآورند؟",
                          "4.آیا شما در شبکه\u200Cهای اجتماعی حضور فعالی دارید؟"],
        "تجربه مشتری": ["5.آیا مشتریان احساس خوبی از ارتباط با شما و خرید محصولتان دارند؟",
                        "6.آیا شما از بازخورد مشتریان برای بهبود تجربه برند استفاده می\u200Cکنید؟"],
        "وفاداری برند": ["7.آیا شما برنامه\u200Cهایی برای افزایش وفاداری مشتریان به برند دارید؟",
                         "8.مشتریان چند بار خرید مجدد می\u200Cکنند؟",
                         "9.مشتریان حاضرند برای محصولات/خدمات شما نسبت به رقبا هزینه بیشتری پرداخت کنند؟"],
        "ارزیابی برند": ["10. آیا شما ارزیابی دوره\u200Cای از عملکرد برند خود انجام می\u200Cدهید؟",
                         "11. آیا شما از داده\u200Cهای مشتریان برای سنجش عملکرد برند استفاده می\u200Cکنید؟"],
        "استراتزی برند": ["12. آیا استراتژی برند شما مشخص و مستند است؟",
                          "13. آیا شما بر روی برند خود به\u200Cطور مستمر سرمایه\u200Cگذاری می\u200Cکنید؟"],
        "نوآوری در برندینگ": ["14. آیا شما در حال حاضر در حال نوآوری در برند خود هستید؟"],
    }
    medium_questions = {
        "هویت برند": [
            "1. آیا شما هویت برند واضح و مشخصی برای کسب\u200Cوکار خود تعریف کرده\u200Cاید؟(هویت برند: اجزای قابل رویت برند از قبیل رنگ، طراحی، لحن ارتباطی و لوگو که با ماهیت کسب\u200Cوکار همخوانی دارد)",
            "2. آیا هویت برند شما با استراتژی کلی کسب\u200Cوکار هماهنگ است؟ (منظور: همسویی هویت برند با چشم\u200Cانداز، مأموریت و ارزش\u200Cهای سازمان)",
            "3. آیا از هویت برند برای شفاف\u200Cسازی فرهنگ سازمانی استفاده می\u200Cکنید؟ (منظور: استفاده از عناصر هویتی برند در تقویت فرهنگ و رفتارهای سازمانی داخلی)"],
        "آگاهی از برند": [". آیا برند شما در بازار هدف به\u200Cخوبی شناخته\u200Cشده است؟",
                          "5. آیا شما از تبلیغات دیجیتال برای افزایش آگاهی از برند استفاده می\u200Cکنید؟",
                          "6. آیا شما از کمپین\u200Cهای تبلیغاتی برای تقویت آگاهی از برند استفاده می\u200Cکنید؟",
                          "7. آیا مشتریان برند شما را با کیفیت محصولات یا خدماتتان ارتباط می\u200Cدهند؟"],
        "تجربه مشتری": ["8. آیا شما برای بهبود تجربه مشتری خود، تحقیقات بازار انجام می\u200Cدهید؟",
                        "9. آیا شما از بازخورد مشتریان برای بهبود تجربه برند استفاده می\u200Cکنید؟",
                        "10. آیا شما فرآیندهایی برای اندازه\u200Cگیری و ارزیابی تجربه مشتری در نظر گرفته\u200Cاید؟",
                        "11. آیا شما از نظرات مشتریان برای ارتقاء خدمات و محصولات خود استفاده می\u200Cکنید؟"],
        "وفاداری برند": ["12. آیا شما برنامه\u200Cهای ویژه\u200Cای برای افزایش وفاداری مشتریان دارید؟",
                         "13. آیا شما از مشتریان وفادار خود برای تبلیغ برند استفاده می\u200Cکنید؟",
                         "14. آیا شما به مشتریان خود پاداش\u200Cهایی برای وفاداری می\u200Cدهید؟"],
        "ارزیابی برند": ["15. آیا شما به\u200Cطور منظم ارزیابی از عملکرد برند خود انجام می\u200Cدهید؟"],

    }
    large_questions = {
        "هویت برند": [
            "1. آیا هویت برند شما به\u200Cطور دقیق با فرهنگ سازمانی هم\u200Cراستا است؟(هویت برند: ارزش\u200Cها، پیام\u200Cها، لحن و ظاهر برند که باید با رفتار و باورهای سازمانی همخوان باشد.)",
            "2. آیا شما از تمامی کارکنان در فرآیند ایجاد هویت برند مشارکت می\u200Cدهید؟(مشارکت کارکنان: حضور، همفکری و بازخورد کارکنان در تدوین و توسعه هویت برند.)",
            "3. آیا هویت برند شما به\u200Cطور کامل در تمامی نقاط تماس با مشتری پیاده\u200Cسازی شده است؟(نقاط تماس: تمامی لحظات و کانال\u200Cهایی که مشتری با برند در تعامل است — آنلاین، آفلاین، تلفنی و حضوری.)"],
        "آگاهی از برند": [
            "4. آیا شما از کمپین\u200Cهای تبلیغاتی مختلف برای ارتقاء آگاهی از برند استفاده می\u200Cکنید؟(کمپین تبلیغاتی: برنامه\u200Cریزی شده و هدفمند برای افزایش دیده\u200Cشدن برند.)",
            "5. آیا شما از کانال\u200Cهای مختلف برای تبلیغات و شناساندن برند خود استفاده می\u200Cکنید؟(کانال\u200Cهای تبلیغاتی: رسانه\u200Cهای دیجیتال، شبکه\u200Cهای اجتماعی، تبلیغات محیطی، رویدادها و رسانه\u200Cهای سنتی.)",
            "6. آیا شما در ارزیابی تأثیر کمپین\u200Cهای تبلیغاتی خود از داده\u200Cها و تجزیه\u200Cو\u200Cتحلیل\u200Cها استفاده می\u200Cکنید؟(تحلیل داده: بررسی دقیق نتایج تبلیغات برای ارزیابی اثربخشی.)",
            "7. آیا شما به\u200Cطور مداوم وضعیت آگاهی از برند خود را ارزیابی می\u200Cکنید؟(آگاهی از برند: میزان شناخت مخاطبان نسبت به برند.)"],
        "تجربه مشتری": [
            "8. آیا شما از تحقیقات بازار برای بهبود تجربه برند خود استفاده می\u200Cکنید؟(تحقیقات بازار: جمع\u200Cآوری و تحلیل داده\u200Cهای رفتاری، نگرشی و تجربی مشتریان.)",
            "9. آیا شما از داده\u200Cهای مشتریان برای شخصی\u200Cسازی تجربه برند استفاده می\u200Cکنید؟(شخصی\u200Cسازی تجربه: استفاده از اطلاعات مشتریان برای ارائه پیشنهادها یا خدمات متناسب با نیازهای هر فرد.)",
            "10. آیا شما به\u200Cطور مداوم تجربه مشتریان خود را ارزیابی می\u200Cکنید؟(ارزیابی تجربه مشتری: سنجش رضایت، انتظارات و نقاط قوت یا ضعف تعامل با برند.)",
            "11. آیا شما از نظرات مشتریان برای بهبود تجربه برند استفاده می\u200Cکنید؟(بازخورد مشتریان: نظرات، پیشنهادات و انتقادات آن\u200Cها درباره محصولات، خدمات یا برند.)"],
        "وفاداری برند": [
            "12. آیا شما برنامه\u200Cهای وفاداری ویژه\u200Cای برای مشتریان خود دارید؟(برنامه وفاداری: مشوق\u200Cها و پیشنهاداتی برای حفظ و افزایش رضایت و خرید مجدد مشتریان.)",
            "مثال: مشتریان در صورت تکرار خرید مزیت خاصی دریافت نمی\u200Cکنند.\n13. آیا شما از مشتریان وفادار خود برای افزایش آگاهی از برند استفاده می\u200Cکنید؟(تبلیغ از طریق مشتریان وفادار: استفاده از رضایت مشتریان برای جذب مشتریان جدید.)",
            "14. آیا شما به\u200Cطور مداوم میزان وفاداری مشتریان را ارزیابی می\u200Cکنید؟(اندازه\u200Cگیری وفاداری: بررسی خرید مجدد، توصیه برند توسط مشتریان، میزان ریزش مشتری.)"]
    }
