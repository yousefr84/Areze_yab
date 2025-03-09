from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth.hashers import make_password
from django.conf import settings
import requests
import json


# # ? sandbox merchant
# if settings.SANDBOX:
#     sandbox = 'sandbox'
# else:
#     sandbox = 'www'
#
# # variables
# ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
# ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
# ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
#
# amount = 1000  # Rial / Required
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# phone = 'YOUR_PHONE_NUMBER'  # Optional
# # Important: need to edit for realy server.
# CallbackURL = 'http://127.0.0.1:8080/verify/'


class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        if not username or not password:
            return Response(data={"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        serialized_user = UserSerializer(data=request.data)
        if not serialized_user.is_valid():
            return Response(data=serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serialized_user.validated_data
        user = CustomUser.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class GetDataAPIView(APIView):
    permission_classes([IsAuthenticated])
    # def handle_generic(self, serializer_class, company, answers, subdomains):
    #     serializer = serializer_class(data={"company": company.id, **answers})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # results = {}
        # for subdomain, fields in subdomains.items():
        #     values = [answers[field] for field in fields if field in answers]
        #     results[subdomain] = sum(values) / len(values) if values else 0
        #
        # all_scores = list(answers.values())
        # results["OverallScore"] = sum(all_scores) / len(all_scores) if all_scores else 0
        #
        # company_serializer = CompanySerializer(company)
        #
        # return Response({
        #     "company": company_serializer.data,
        #     "results": results
        # }, status=status.HTTP_201_CREATED)
    def post(self, request):
        company_user = request.user
        print(company_user)

        company_data = request.data.get('company')
        # name = company_data.get('name')
        # registrationNumber = company_data.get('registrationNumber')
        # nationalID = company_data.get('nationalID')

        if not company_data:
            return Response({"error": "Company data is required"}, status=status.HTTP_400_BAD_REQUEST)
        company_serializer = CompanySerializer(data=company_data)
        print(f'validation of company serializer: {company_serializer.is_valid()}')
        if not company_serializer.is_valid():
            return Response(data=company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        company = company_serializer.save()
        print('user will be add to company')
        company.user.set(company_user)
        # company.user.add(company_user)
        print(f'user {company_user.username} added to company {company}')

        return Response(company_serializer.data, status=status.HTTP_201_CREATED)



    def patch(self, request):
        answer = request.data.get('answer')
        domain = request.data.get('domain')

        if not answer:
            return Response(data={"error": "Answer is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not domain:
            return Response(data={"error": "Domain is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
            return Response(data={"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        domain_map = {
            'human_resources': (HumanResources, HumanResourcesSerializer),
            'financial_resources': (FinancialResources, FinancialResourcesSerializer),
            'sales_and_marketing': (SalesAndMarketing, SalesAndMarketingSerializer),
            'capital_structure': (CapitalStructure, CapitalStructureSerializer),
            'management_organizational_structure': (
            ManagementOrganizationalStructure, ManagementOrganizationalStructureSerializer),
            'customer_relationship_management': (
            CustomerRelationshipManagement, CustomerRelationshipManagementSerializer),
            'manufacturing_and_production': (ManufacturingAndProduction, ManufacturingAndProductionSerializer),
            'research_and_development': (ResearchAndDevelopment, ResearchAndDevelopmentSerializer),
            'product_competitiveness': (ProductCompetitiveness, ProductCompetitivenessSerializer),
        }

        if domain not in domain_map:
            return Response(data={"error": "Invalid Domain"}, status=status.HTTP_400_BAD_REQUEST)

        model_class, serializer_class = domain_map[domain]

        try:
            table = model_class.objects.get(company=company)
        except model_class.DoesNotExist:
            return Response(data={"error": f"{domain.replace('_', ' ').title()} record not found"},
                            status=status.HTTP_404_NOT_FOUND)

        valid_fields = [field.name for field in model_class._meta.get_fields()]

        for field, value in answer.items():
            if field not in valid_fields:
                return Response(data={"error": f"Invalid field: {field}"}, status=status.HTTP_400_BAD_REQUEST)

            setattr(table, field, value)

        table.save()

        return Response(data=serializer_class(table).data, status=status.HTTP_200_OK)
    # def get(self, request):
    #     user = request.user
    #     domain = request.data.get('domain')
    #     company = Company.objects.get(user=user)
    #
    #     if




# class DiagnosticSurveyView(APIView):
#
#     def post(self, request):
#         company_data = request.data.get("company")
#         if not company_data:
#             return Response({"error": "Company data is required"}, status=status.HTTP_400_BAD_REQUEST)
#
#         company_serializer = CompanySerializer(data=company_data)
#         if company_serializer.is_valid():
#             company, _ = Company.objects.get_or_create(**company_serializer.validated_data)
#         else:
#             return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         domain = request.data.get("domain")
#         answers = request.data.get("answers")
#         if not domain or not answers:
#             return Response({"error": "Domain and answers are required"}, status=status.HTTP_400_BAD_REQUEST)
#
#         domain_handlers = {
#             "human_resources": (self.handle_generic, HumanResourcesSerializer, {
#                 "WorkforceNumbers": ["daily_operations_with_current_workforce", "backlog_of_daily_tasks",
#                                      "available_workforce_for_new_projects"],
#                 "EmployeeRetention": ["employees_with_minimum_5_years_experience", "employee_satisfaction_percentage",
#                                       "employee_requests_for_new_jobs", "employee_requests_for_early_retirement",
#                                       "organizational_support_for_employees",
#                                       "annual_salary_increase_adjusted_for_inflation"],
#                 "EmployeeProductivity": ["management_satisfaction_with_employees",
#                                          "employee_satisfaction_with_management", "revenue_per_employee",
#                                          "employee_responsibility_and_commitment"],
#                 "EmployeePerformanceEvaluationSystem": ["performance_evaluation_system_scheduling",
#                                                         "up_to_date_technology_in_performance_evaluation",
#                                                         "evaluation_criteria_alignment_with_job_description",
#                                                         "practical_model_for_employee_ranking"],
#                 "EmployeeTrainingSystem": ["in_house_training_programs", "support_for_attending_training_programs"],
#                 "CollaborationandTeamwork": ["manager_focus_on_team_processes", "employee_interest_in_group_work",
#                                              "shared_workspaces_availability", "weekly_fixed_meetings",
#                                              "manager_employee_interaction"],
#                 "EthicalValuesAwareness": ["respect_for_employee_privacy", "managers_behavior_towards_men_and_women"]
#             }),
#             "manufacturing_and_production": (self.handle_generic, ManufacturingAndProductionSerializer, {
#                 "MonthlyProduction": ["production_increase_planning", "safety_stock_level", "storage_cost",
#                                       "production_stability", "max_capacity_utilization"],
#                 "ProductionManagementSystem": ["production_process_documentation", "defect_detection_and_resolution",
#                                                "production_process_flexibility"],
#                 "ProductionTechnology": ["production_technology_level", "iot_equipment_in_production_line"],
#                 "Market-DrivenProduction": ["production_sales_marketing_alignment"],
#                 "ProductionEfficiency": ["output_input_ratio", "production_waste_ppm"],
#                 "NationalandInternational Standards": ["required_certifications"],
#                 "Warranty": ["warranty_after_sales", "warranty_commitment"],
#                 "QualityControlSystem": ["quality_control_lab", "quality_control_standards"]
#             }),
#             "financial_resources": (self.handle_generic, FinancialResourcesSerializer, {
#                 "OperatingCashFlow": ["ability_to_maintain_positive_cash_flow"],
#                 "CurrentRatio": ["ability_to_pay_financial_obligations"],
#                 "WorkingCapital": ["assets_for_short_term_financial_obligations"],
#                 "CapitalBurnRate": ["weekly_monthly_annual_expenses"],
#                 "NetProfitMargin": ["profitability_efficiency_comparison"],
#                 "AccountsPayableTurnover": ["ability_to_pay_accounts_payable"],
#                 "TotalFinancialPerformanceCost": ["payment_processing_costs"],
#                 "FinancialActivityCostRatio": ["financial_activity_cost_to_income_ratio"],
#                 "FinancialErrorReporting": ["financial_report_accuracy_and_completeness"],
#                 "BudgetDeviation": ["budget_vs_actual_difference"],
#                 "SalesGrowth": ["sales_change_over_period"]
#             }),
#             "capital_structure": (self.handle_generic, CapitalStructureSerializer, {
#                 "FundingSources": ["shareholder_funding_power", "availability_of_resources_for_new_projects"],
#                 "RiskTolerance": ["startup_investment_risk_tolerance"]
#             }),
#             "management_organizational_structure": (self.handle_generic, ManagementOrganizationalStructureSerializer, {
#                 "OrganizationalChart": ["comprehensive_organizational_chart", "regular_chart_updates"],
#                 "KnowledgeandInformationManagementSystem": ["information_system_for_knowledge_management",
#                                                             "knowledge_management_system_integration"],
#                 "WorkplaceOrganizationSystem": ["workspace_design", "five_s_in_daily_operations"],
#                 "ManagementStrategyandVision": ["vision_and_mission_definition",
#                                                 "employee_awareness_of_long_short_term_plans",
#                                                 "activities_for_increasing_customer_awareness"],
#                 "DelegationofAuthority": ["decision_making_power_for_lower_employees"]
#             }),
#             "customer_relationship_management": (self.handle_generic, CustomerRelationshipManagementSerializer, {
#                 "FeedbackSystem": ["purchase_info_documentation", "customer_feedback_system",
#                                    "customer_feedback_analysis"],
#                 "Facilities": ["special_sales_plan_for_loyal_customers", "loyal_customer_payment_benefits",
#                                "first_purchase_support_plan"],
#                 "CustomerRetention": ["employee_training_for_customer_interaction", "loyal_customer_count"]
#             }),
#             "research_and_development": (self.handle_generic, ResearchAndDevelopmentSerializer, {
#                 "ProductImprovement": ["r_and_d_unit_defined_roles", "r_and_d_production_connection", "r_and_d_budget"],
#                 "Innovation": ["innovation_planning", "innovation_process_guidelines",
#                                "customer_competitor_inspiration", "innovation_culture"]
#             }),
#             "product_competitiveness": (self.handle_generic, ProductCompetitivenessSerializer, {
#                 "CompetitiveEdge": ["unique_feature"]
#             }),
#             "sales_and_marketing": (self.handle_generic, SalesAndMarketingSerializer, {
#                 "Branding": ["brandIdentity", "visualIdentityActivities", "brandReputationManagement",
#                              "brandTrustAndEmotionalConnection"],
#                 "MarketShare": ["marketResearchOpportunities", "salesToIndustryRatio", "marketLeadershipPotential"],
#                 "DistributionandSalesChannels": ["orderDeliveryTimeliness", "salesNetworkCoverage",
#                                                  "salesAgencySupervision", "salesRepProductAwareness",
#                                                  "reliableTransportUsage"],
#                 "MarketingandSalesStrategy": ["digitalMarketingUsage", "marketResearchForMarketing",
#                                               "marketingPlanningAndGuidelines", "marketingAndSalesNetworking",
#                                               "innovativeMarketingUsage", "exhibitionParticipation"],
#                 "SalesHistory": ["salesAmountToCostRatio", "salesGrowthLast3Months", "salesToProductionRatio"],
#                 "TargetMarketKnowledge": ["targetMarketDefinition", "marketRegulationsKnowledge",
#                                           "competitorAwareness"],
#                 "ExportActivities": ["exportActivitiesAndGlobalMarketUse"]
#             })
#         }
#
#         handler, serializer_class, subdomains = domain_handlers.get(domain, (None, None, None))
#         if handler:
#             return handler(serializer_class, company, answers, subdomains)
#         else:
#             return Response({"error": "Invalid domain selected"}, status=status.HTTP_400_BAD_REQUEST)
#
#     def handle_generic(self, serializer_class, company, answers, subdomains):
#         serializer = serializer_class(data={"company": company.id, **answers})
#         if serializer.is_valid():
#             instance = serializer.save()
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         results = {}
#         for subdomain, fields in subdomains.items():
#             values = [answers[field] for field in fields if field in answers]
#             results[subdomain] = sum(values) / len(values) if values else 0
#
#         all_scores = list(answers.values())
#         results["OverallScore"] = sum(all_scores) / len(all_scores) if all_scores else 0
#
#         company_serializer = CompanySerializer(company)
#
#         return Response({
#             "company": company_serializer.data,
#             "results": results
#         }, status=status.HTTP_201_CREATED)

# payment
# def send_request(request):
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": amount,
#         "Description": description,
#         "Phone": phone,
#         "CallbackURL": CallbackURL,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#     try:
#         response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
#
#         if response.status_code == 200:
#             response = response.json()
#             if response['Status'] == 100:
#                 return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
#                         'authority': response['Authority']}
#             else:
#                 return {'status': False, 'code': str(response['Status'])}
#         return response
#
#     except requests.exceptions.Timeout:
#         return {'status': False, 'code': 'timeout'}
#     except requests.exceptions.ConnectionError:
#         return {'status': False, 'code': 'connection error'}
#
#
# def verify(authority):
#     data = {
#         "MerchantID": settings.MERCHANT,
#         "Amount": amount,
#         "Authority": authority,
#     }
#     data = json.dumps(data)
#     # set content length by data
#     headers = {'content-type': 'application/json', 'content-length': str(len(data))}
#     response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
#
#     if response.status_code == 200:
#         response = response.json()
#         if response['Status'] == 100:
#             return {'status': True, 'RefID': response['RefID']}
#         else:
#             return {'status': False, 'code': str(response['Status'])}
#     return response
