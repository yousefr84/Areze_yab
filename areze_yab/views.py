from django.utils.translation import gettext as _

from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from areze_yab.serializers import *


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


class BaseAPIView(APIView):
    serializer_class = None
    subdomains = None
    domain = None

    def put(self, request):
        nationalID = request.data['nationalID']
        if not nationalID:
            return Response(data={"error": "nationalID is required"}, status=status.HTTP_400_BAD_REQUEST)
        user_id = request.data['userid']

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
        subdomains = self.subdomains
        answers = SalesAndMarketing.objects.filter(company=company).last()

        for subdomain, fields in subdomains.items():
            values = [getattr(answers, field, None) for field in fields if
                      getattr(answers, field, None) is not None and isinstance(getattr(answers, field, None),
                                                                               (int, float))]

            results[subdomain] = sum(values) / len(values) if values else 0
        all_fields = [field for fields_list in subdomains.values() for field in fields_list]
        all_scores = [getattr(answers, field, None) for field in all_fields
                      if getattr(answers, field, None) is not None
                      and isinstance(getattr(answers, field, None), (int, float))]

        results["Overall Score"] = sum(all_scores) / len(all_scores) if all_scores else 0

        return Response({
            "company": company_serializer.data,
            "domain": self.domain,
            "results": results
        }, status=status.HTTP_200_OK)


class SalesAndMarketingAPIView(BaseAPIView):
    serializer_class = SalesAndMarketingSerializer
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


class HumanResourceAPIView(BaseAPIView):
    parser_classes = HumanResourcesSerializer
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


class FinancialResourcesAPIView(BaseAPIView):
    serializer_class = FinancialResourcesSerializer
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


class CapitalStructureAPIView(BaseAPIView):
    serializer_class = CapitalStructureSerializer
    domain = "ساختار سرمایه"
    subdomains = {
        "نحوه تامین سرمایه": ["shareholder_funding_power", "availability_of_resources_for_new_projects"],
        "ریسک پذیری": ["startup_investment_risk_tolerance"]
    }


class ManagementOrganizationalStructureAPIView(BaseAPIView):
    serializer_class = ManagementOrganizationalStructureSerializer
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


class CustomerRelationshipManagementAPIView(BaseAPIView):
    serializer_class = CustomerRelationshipManagementSerializer
    domain = 'مدیریت ارتباط با مشتری'
    subdomains = {
        "سیستم بازخورد": ["purchase_info_documentation", "customer_feedback_system",
                          "customer_feedback_analysis"],
        "تسهیلات": ["special_sales_plan_for_loyal_customers", "loyal_customer_payment_benefits",
                    "first_purchase_support_plan"],
        "ماندگاری مشتری": ["employee_training_for_customer_interaction", "loyal_customer_count"]
    }


class ManufacturingAndProductionAPIView(BaseAPIView):
    serializer_class = ManufacturingAndProductionSerializer
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


class ResearchAndDevelopmentAPIView(BaseAPIView):
    serializer_class = ResearchAndDevelopmentSerializer
    subdomains = {
        "بهبود محصول": ["r_and_d_unit_defined_roles", "r_and_d_production_connection", "r_and_d_budget"],
        "نوآوری": ["innovation_planning", "innovation_process_guidelines",
                       "customer_competitor_inspiration", "innovation_culture"]
    }
    domain = 'تحقیق و توسعه'

class ProductCompetitivenessAPIView(BaseAPIView):
    serializer_class = ProductCompetitivenessSerializer
    domain = 'رفابت پذیری محصول'
    subdomains = { "مزیت رفابتی": ["unique_feature"]}