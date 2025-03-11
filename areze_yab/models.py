from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


#
class CustomUser(AbstractUser):
    is_company = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    registrationNumber = models.CharField(max_length=4, blank=True, null=True, unique=True)
    username = models.CharField(max_length=11, blank=True, null=True, unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


class Company(models.Model):
    user = models.ManyToManyField(CustomUser)
    name = models.CharField(max_length=100)
    registrationNumber = models.CharField(max_length=100)
    nationalID = models.CharField(max_length=100)


class SalesAndMarketing(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # <------------Branding------------>
    brandIdentity = models.IntegerField(blank=True, null=True)
    visualIdentityActivities = models.IntegerField(blank=True, null=True)
    brandReputationManagement = models.IntegerField(blank=True, null=True)
    brandTrustAndEmotionalConnection = models.IntegerField(blank=True, null=True)
    # <------------MarketShare------------>
    marketResearchOpportunities = models.IntegerField(blank=True, null=True)
    salesToIndustryRatio = models.IntegerField(blank=True, null=True)
    marketLeadershipPotential = models.IntegerField(blank=True, null=True)
    # <------------DistributionAndSalesChannels------------>
    orderDeliveryTimeliness = models.IntegerField(blank=True, null=True)
    salesNetworkCoverage = models.IntegerField(blank=True, null=True)
    salesAgencySupervision = models.IntegerField(blank=True, null=True)
    salesRepProductAwareness = models.IntegerField(blank=True, null=True)
    reliableTransportUsage = models.IntegerField(blank=True, null=True)

    # <------------MarketingAndSalesStrategy------------>
    digitalMarketingUsage = models.IntegerField(blank=True, null=True)
    marketResearchForMarketing = models.IntegerField(blank=True, null=True)
    marketingPlanningAndGuidelines = models.IntegerField(blank=True, null=True)
    marketingAndSalesNetworking = models.IntegerField(blank=True, null=True)
    innovativeMarketingUsage = models.IntegerField(blank=True, null=True)
    exhibitionParticipation = models.IntegerField(blank=True, null=True)

    # <------------SalesHistory------------>
    salesAmountToCostRatio = models.IntegerField(blank=True, null=True)
    salesGrowthLast3Months = models.IntegerField(blank=True, null=True)
    salesToProductionRatio = models.IntegerField(blank=True, null=True)

    # <------------TargetMarketKnowledge------------>
    targetMarketDefinition = models.IntegerField(blank=True, null=True)
    marketRegulationsKnowledge = models.IntegerField(blank=True, null=True)
    competitorAwareness = models.IntegerField(blank=True, null=True)

    # <------------ExportActivities------------>
    exportActivitiesAndGlobalMarketUse = models.IntegerField(blank=True, null=True)

    date = models.DateField(auto_now=True)


# <------------Human Resources------------>
class HumanResources(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # <------------Workforce Numbers------------>
    daily_operations_with_current_workforce = models.IntegerField(blank=True, null=True)
    backlog_of_daily_tasks = models.IntegerField(blank=True, null=True)
    available_workforce_for_new_projects = models.IntegerField(blank=True, null=True)

    # <------------Employee Retention------------>
    employees_with_minimum_5_years_experience = models.IntegerField(blank=True, null=True)
    employee_satisfaction_percentage = models.IntegerField(blank=True, null=True)
    employee_requests_for_new_jobs = models.IntegerField(blank=True, null=True)
    employee_requests_for_early_retirement = models.IntegerField(blank=True, null=True)
    organizational_support_for_employees = models.IntegerField(blank=True, null=True)
    annual_salary_increase_adjusted_for_inflation = models.IntegerField(blank=True, null=True)

    # <------------Employee Productivity------------>
    management_satisfaction_with_employees = models.IntegerField(blank=True, null=True)
    employee_satisfaction_with_management = models.IntegerField(blank=True, null=True)
    revenue_per_employee = models.IntegerField(blank=True, null=True)
    employee_responsibility_and_commitment = models.IntegerField(blank=True, null=True)

    # <------------Employee Performance Evaluation System------------>
    performance_evaluation_system_scheduling = models.IntegerField(blank=True, null=True)
    up_to_date_technology_in_performance_evaluation = models.IntegerField(blank=True, null=True)
    evaluation_criteria_alignment_with_job_description = models.IntegerField(blank=True, null=True)
    practical_model_for_employee_ranking = models.IntegerField(blank=True, null=True)

    # <------------Employee Training System------------>
    in_house_training_programs = models.IntegerField(blank=True, null=True)
    support_for_attending_training_programs = models.IntegerField(blank=True, null=True)

    # <------------Collaboration and Teamwork------------>
    manager_focus_on_team_processes = models.IntegerField(blank=True, null=True)
    employee_interest_in_group_work = models.IntegerField(blank=True, null=True)
    shared_workspaces_availability = models.IntegerField(blank=True, null=True)
    weekly_fixed_meetings = models.IntegerField(blank=True, null=True)
    manager_employee_interaction = models.IntegerField(blank=True, null=True)

    # <------------Ethical Values Awareness------------>
    respect_for_employee_privacy = models.IntegerField(blank=True, null=True)
    managers_behavior_towards_men_and_women = models.IntegerField(blank=True, null=True)

    date = models.DateField(auto_now=True)


# <------------Financial Resources------------>
class FinancialResources(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # <------------Operating Cash Flow------------>
    ability_to_maintain_positive_cash_flow = models.IntegerField(blank=True, null=True)

    # <------------Current Ratio------------>
    ability_to_pay_financial_obligations = models.IntegerField(blank=True, null=True)

    # <------------Working Capital------------>
    assets_for_short_term_financial_obligations = models.IntegerField(blank=True, null=True)

    # <------------Capital Burn Rate------------>
    weekly_monthly_annual_expenses = models.IntegerField(blank=True, null=True)

    # <------------Net Profit Margin------------>
    profitability_efficiency_comparison = models.IntegerField(blank=True, null=True)

    # <------------Accounts Payable Turnover------------>
    ability_to_pay_accounts_payable = models.IntegerField(blank=True, null=True)

    # <------------Total Financial Performance Cost------------>
    payment_processing_costs = models.IntegerField(blank=True, null=True)

    # <------------Financial Activity Cost Ratio------------>
    financial_activity_cost_to_income_ratio = models.IntegerField(blank=True, null=True)

    # <------------Financial Error Reporting------------>
    financial_report_accuracy_and_completeness = models.IntegerField(blank=True, null=True)

    # <------------Budget Deviation------------>
    budget_vs_actual_difference = models.IntegerField(blank=True, null=True)

    # <------------Sales Growth------------>
    sales_change_over_period = models.IntegerField(blank=True, null=True)

    date = models.DateField(auto_now=True)


# <------------Capital Structure------------>
class CapitalStructure(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # <------------Funding Sources------------>
    shareholder_funding_power = models.IntegerField(blank=True, null=True)
    availability_of_resources_for_new_projects = models.IntegerField(blank=True, null=True)

    # <------------Risk Tolerance------------>
    startup_investment_risk_tolerance = models.IntegerField(blank=True, null=True)

    date = models.DateField(auto_now=True)


# <------------Management & Organizational Structure------------>
class ManagementOrganizationalStructure(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # <------------Organizational Chart------------>
    comprehensive_organizational_chart = models.IntegerField(blank=True, null=True)
    regular_chart_updates = models.IntegerField(blank=True, null=True)

    # <------------Knowledge and Information Management System------------>
    information_system_for_knowledge_management = models.IntegerField(blank=True, null=True)
    knowledge_management_system_integration = models.IntegerField(blank=True, null=True)

    # <------------Workplace Organization System------------>
    workspace_design = models.IntegerField(blank=True, null=True)
    five_s_in_daily_operations = models.IntegerField(blank=True, null=True)

    # <------------Management Strategy and Vision------------>
    vision_and_mission_definition = models.IntegerField(blank=True, null=True)
    employee_awareness_of_long_short_term_plans = models.IntegerField(blank=True, null=True)
    activities_for_increasing_customer_awareness = models.IntegerField(blank=True, null=True)

    # <------------Delegation of Authority------------>
    decision_making_power_for_lower_employees = models.IntegerField(blank=True, null=True)

    date = models.DateField(auto_now=True)


# <------------Customer Relationship Management------------>
class CustomerRelationshipManagement(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # <------------Feedback System------------>
    purchase_info_documentation = models.IntegerField(blank=True, null=True)
    customer_feedback_system = models.IntegerField(blank=True, null=True)
    customer_feedback_analysis = models.IntegerField(blank=True, null=True)

    # <------------Facilities------------>
    special_sales_plan_for_loyal_customers = models.IntegerField(blank=True, null=True)
    loyal_customer_payment_benefits = models.IntegerField(blank=True, null=True)
    first_purchase_support_plan = models.IntegerField(blank=True, null=True)

    # <------------Customer Retention------------>
    employee_training_for_customer_interaction = models.IntegerField(blank=True, null=True)
    loyal_customer_count = models.IntegerField(blank=True, null=True)

    date = models.DateField(auto_now=True)


class ManufacturingAndProduction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # <------------Monthly Production------------>
    production_increase_planning = models.IntegerField(blank=True, null=True)
    safety_stock_level = models.IntegerField(blank=True, null=True)
    storage_cost = models.IntegerField(blank=True, null=True)
    production_stability = models.IntegerField(blank=True, null=True)
    max_capacity_utilization = models.IntegerField(blank=True, null=True)

    # <------------Production Management System------------>
    production_process_documentation = models.IntegerField(blank=True, null=True)
    defect_detection_and_resolution = models.IntegerField(blank=True, null=True)
    production_process_flexibility = models.IntegerField(blank=True, null=True)

    # <------------Production Technology------------>
    production_technology_level = models.IntegerField(blank=True, null=True)
    iot_equipment_in_production_line = models.IntegerField(blank=True, null=True)

    # <------------Market-Driven Production------------>
    production_sales_marketing_alignment = models.IntegerField(blank=True, null=True)

    # <------------Production Efficiency------------>
    output_input_ratio = models.IntegerField(blank=True, null=True)
    production_waste_ppm = models.IntegerField(blank=True, null=True)

    # <------------National and International Standards------------>
    required_certifications = models.IntegerField(blank=True, null=True)

    # <------------Warranty------------>
    warranty_after_sales = models.IntegerField(blank=True, null=True)
    warranty_commitment = models.IntegerField(blank=True, null=True)

    # <------------Quality Control System------------>
    quality_control_lab = models.IntegerField(blank=True, null=True)
    z = models.IntegerField(blank=True, null=True)

    date = models.DateField(auto_now=True)


# <------------Research & Development------------>
class ResearchAndDevelopment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # <------------Product Improvement------------>
    r_and_d_unit_defined_roles = models.IntegerField(blank=True, null=True)
    r_and_d_production_connection = models.IntegerField(blank=True, null=True)
    r_and_d_budget = models.IntegerField(blank=True, null=True)

    # <------------Innovation------------>
    innovation_planning = models.IntegerField(blank=True, null=True)
    innovation_process_guidelines = models.IntegerField(blank=True, null=True)
    customer_competitor_inspiration = models.IntegerField(blank=True, null=True)
    innovation_culture = models.IntegerField(blank=True, null=True)
    date = models.DateField(auto_now=True)


# <------------Product Competitiveness------------>
class ProductCompetitiveness(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    unique_feature = models.IntegerField(blank=True, null=True)
    date = models.DateField(auto_now=True)
