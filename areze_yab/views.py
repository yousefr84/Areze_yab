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

openai.api_key = "توکن_API_تو"


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        if not data:
            return Response({'error': 'No data provided'}, status=status.HTTP_400_BAD_REQUEST)
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
                                                     nationalID=serializer.data['username'])
                    company.user.add(CustomUser.objects.get(id=serializer.data['id']))
                except IntegrityError as e:
                    return Response({'error': _('Company creation failed: {}').format(str(e))},
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({"error": "user id missing"}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyAPIView(APIView):
    def post(self, request):
        userid = request.data['userid']
        company_data = request.data['company']
        if not company_data:
            return Response(data={"error": "Company is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(id=userid)
        if not user.is_company:
            company = Company.objects.create(name=company_data['name'],
                                             registrationNumber=company_data['registrationNumber'],
                                             nationalID=company_data['nationalID'])
            company.user.add(user)
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)


class HistoryViewSet(ViewSet):
    objects = []

    @action(detail=False, methods=['get'])
    def All(self, request):
        registrationNumber = request.query_params.get('registrationNumber')
        if not registrationNumber:
            return Response(data={"user_id doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        companies = Company.objects.filter(registrationNumber=registrationNumber)
        for company in companies:
            self.objects.append(SalesAndMarketing.objects.filter(company=company))
            self.objects.append(Branding.objects.filter(company=company))
            self.objects.append(ProductCompetitiveness.objects.filter(company=company))
            self.objects.append(ResearchAndDevelopment.objects.filter(company=company))
            self.objects.append(ManufacturingAndProduction.objects.filter(company=company))
        return Response(data=self.objects, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def Companyies(self, request):
        registrationNumber = request.query_params.get('registrationNumber')
        if not registrationNumber:
            return Response(data={"registrationNumber doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        companies = Company.objects.filter(registrationNumber=registrationNumber)
        serializer = CompanySerializer(companies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def DomainFilter(self, request):
        registrationNumber = request.query_params.get('registrationNumber')
        domain = request.query_params.get('domain')
        if not registrationNumber or not domain:
            return Response(data={"registrationNumber or domain doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        companies = Company.objects.filter(registrationNumber=registrationNumber)
        modelclass = apps.get_model('areze_yab', domain)
        for company in companies:
            self.objects.append(modelclass.objects.filter(company=company))
        return Response(data=self.objects, status=status.HTTP_200_OK)


class BaseAPIView(APIView):
    serializer_class = None
    subdomains = None
    domain = None
    finall = None
    model_class = None
    questions = None

    def put(self, request):
        data = request.data
        nationalID = request.data['nationalID']
        if not nationalID:
            return Response(data={"error": "nationalID is required"}, status=status.HTTP_400_BAD_REQUEST)
        user_id = request.data['userid']
        answer = request.data['answer']

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
        request.data['company'] = company.id
        if answer:
            if answer == self.finall:
                data['is_draft'] = False
                serializer = self.serializer_class(data=request.data)
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

        results = {}
        answers = self.model_class.objects.filter(company=company).last()
        fields = [field for fields_list in self.subdomains.values() for field in fields_list]
        text = []
        for field in fields:
            val = getattr(answers, field, None)
            if val is not None and hasattr(val, 'text') and val.text is not None:
                text.append(val.text)

        questions_answers = dict(zip(self.questions, text))

        prompt = f"""
        I want a branding analysis report based on the following questionnaire responses.

        The report must include:
        1. A general analysis of the company’s current branding status considering its size
        2. Strengths and weaknesses of current branding based on the answers and up-to-date research in the field
        3. Five specific and practical suggestions to improve the branding strategy according to the responses

        Go directly into the analysis. Do not include any introductions.

        Company size: Small, with 10 employees
        
        {questions_answers}
        
        Please write the report in Persian, using a professional tone and clear structure.
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional branding consultant. Your task is to analyze questionnaire responses and generate strategic branding reports. Always respond in Persian with a professional tone and clear structure. Do not include any introductions or general explanations — go straight into the analysis."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response = response['choices'][0]['message']['content']
        scores = []
        for field in fields:
            val = getattr(answers, field, None)
        if val is not None and hasattr(val, 'number') and val.number is not None:
            scores.append(val.number)

        # for subdomain, fields in subdomains.items():
        #     values = []
        #     for field in fields:
        #         val = getattr(answers, field, None)
        #         if val is not None and hasattr(val, 'number') and val.number is not None:
        #             values.append(val.number)
        #
        #     results[subdomain] = sum(values) / len(values) if values else 0
        #
        # all_fields = [field for fields_list in subdomains.values() for field in fields_list]
        # all_scores = []
        # for field in all_fields:
        #     val = getattr(answers, field, None)
        #     if val is not None and hasattr(val, 'number') and val.number is not None:
        #         all_scores.append(val.number)

        # results["Overall Score"] = sum(all_scores) / len(all_scores) if all_scores else 0

        overall_score = sum(scores) / len(scores) if scores else 0
        return Response({
            "company": company_serializer.data,
            "domain": self.domain,
            "overallScore": overall_score,
            "response": response,
        }, status=status.HTTP_200_OK)


class SalesAndMarketingAPIView(BaseAPIView):
    serializer_class = SalesAndMarketingSerializer
    model_class = SalesAndMarketing
    subdomains = {
        "برندینگ": ["brandIdentity", "visualIdentityActivities", "brandReputationManagement",
                    "brandTrustAndEmotionalConnection"],
        "سهم بازار": ["marketResearchOpportunities", "salesToIndustryRatio", "marketLeadershipPotential"],
        "کانال های توزیع و فروش": ["orderDeliveryTimeliness", "salesNetworkCoverage",
                                   "salesAgencySupervision", "salesRepProductAwareness",
                                   "reliableTransportUsage"],
        "استراتژی فروش و مارکتینگ": ["digitalMarketingUsage", "marketResearchForMarketing",
                                     "marketingPlanningAndGuidelines", "marketingAndSalesNetworking",
                                     "innovativeMarketingUsage", "exhibitionParticipation"],
        "سوابق فروش": ["salesAmountToCostRatio", "salesGrowthLast3Months", "salesToProductionRatio"],
        "شناخت بازار هدف": ["targetMarketDefinition", "marketRegulationsKnowledge",
                            "competitorAwareness"],
        "فعالیت های صادراتی": ["exportActivitiesAndGlobalMarketUse"]
    }
    domain = "فروش و مارکتینگ"
    finall = 'exportActivitiesAndGlobalMarketUse'


class HumanResourceAPIView(BaseAPIView):
    parser_classes = HumanResourcesSerializer
    model_class = HumanResources
    domain = "منابع انسانی"
    subdomains = {
        "تعداد نیرو": ["daily_operations_with_current_workforce", "backlog_of_daily_tasks",
                       "available_workforce_for_new_projects"],
        "ماندگاری نیروی انسانی": ["employees_with_minimum_5_years_experience", "employee_satisfaction_percentage",
                                  "employee_requests_for_new_jobs", "employee_requests_for_early_retirement",
                                  "organizational_support_for_employees",
                                  "annual_salary_increase_adjusted_for_inflation"],
        "بهره وری پرسنل": ["management_satisfaction_with_employees",
                           "employee_satisfaction_with_management", "revenue_per_employee",
                           "employee_responsibility_and_commitment"],
        "سیستم ارزیابی عملکرد کارکنان": ["performance_evaluation_system_scheduling",
                                         "up_to_date_technology_in_performance_evaluation",
                                         "evaluation_criteria_alignment_with_job_description",
                                         "practical_model_for_employee_ranking"],
        "سیستم آموزش کارکنان": ["in_house_training_programs", "support_for_attending_training_programs"],
        "همکاری و کار گروهی": ["manager_focus_on_team_processes", "employee_interest_in_group_work",
                               "shared_workspaces_availability", "weekly_fixed_meetings",
                               "manager_employee_interaction"],
        "توجه به ارزش های اخلاقی": ["respect_for_employee_privacy", "managers_behavior_towards_men_and_women"]
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
    serializer_class = BrandingSerializer
    model_class = Branding
    domain = 'برندینگ'
    subdomains = {}
    finall = "is_visual_design_of_brand_consistent"
    questions = ["آیا شرکت هویت برند خود را به‌صورت مستند تعریف کرده است؟", "آیا شرکت شخصیت برند خود را مشخص کرده است؟",
                 "چگونه شهرت برند در بازار را رصد و مدیریت می‌کنید؟",
                 "تا چه حد با مشتریان ارتباط عاطفی برقرار کرده‌اید؟",
                 "آیا برای برند خود شعار یا پیامی دارید؟", "چگونه بازخورد مشتریان را جمع‌آوری می‌کنید؟",
                 "آیا برند شما در شبکه‌های اجتماعی فعال است؟", "آیا کارکنان با ارزش‌ها و مأموریت برند آشنا هستند",
                 "آیا طراحی بصری برند (لوگو، رنگ‌ها) یکپارچه است؟",
                 "آیا برنامه‌ای برای بهبود شناخت برند در بازار دارید؟",
                 ]
