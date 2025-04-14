import re
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CharIntegerField(models.Field):
    description = "A custom field that stores both string and integer values separately"

    def __init__(self, *args, **kwargs):
        self.max_length = kwargs.get('max_length', 255)
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self._parse_value(value)

    def to_python(self, value):
        if isinstance(value, CharInteger):
            return value
        if value is None:
            return value
        return self._parse_value(value)

    def get_prep_value(self, value):
        if isinstance(value, CharInteger):
            return value.raw
        return str(value)

    def _parse_value(self, raw_value):
        return CharInteger(raw_value)

    def db_type(self, connection):
        # نوع داده پایگاه داده که باید برای این فیلد استفاده شود (برای مثال: VARCHAR)
        return f"VARCHAR({self.max_length})"

class CharInteger:
    def __init__(self, raw_value):
        self.raw = raw_value
        self.number = None
        self.text = None
        self._parse_value()

    def _parse_value(self):
        # جدا کردن قسمت عددی و متنی
        match = re.match(r'(\d+)([a-zA-Z]*)', self.raw)
        if match:
            self.number = int(match.group(1))
            self.text = match.group(2)
        else:
            self.number = None
            self.text = self.raw

    def __str__(self):
        return self.raw

    def __repr__(self):
        return f"<CharInteger number={self.number}, text='{self.text}'>"


class CustomUser(AbstractUser):
    is_company = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
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


class BaseDomain(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=True)
    date = models.DateField(auto_now=True)


class SalesAndMarketing(BaseDomain):
    # <------------Branding------------>
    brandIdentity = CharIntegerField(default=0,max_length=100)
    visualIdentityActivities = CharIntegerField(default=0,max_length=100)
    brandReputationManagement = CharIntegerField(default=0,max_length=100)
    brandTrustAndEmotionalConnection = CharIntegerField(default=0,max_length=100)
    # <------------MarketShare------------>
    marketResearchOpportunities = CharIntegerField(default=0,max_length=100)
    salesToIndustryRatio = CharIntegerField(default=0,max_length=100)
    marketLeadershipPotential = CharIntegerField(default=0,max_length=100)
    # <------------DistributionAndSalesChannels------------>
    orderDeliveryTimeliness = CharIntegerField(default=0,max_length=100)
    salesNetworkCoverage = CharIntegerField(default=0,max_length=100)
    salesAgencySupervision = CharIntegerField(default=0,max_length=100)
    salesRepProductAwareness = CharIntegerField(default=0,max_length=100)
    reliableTransportUsage = CharIntegerField(default=0,max_length=100)

    # <------------MarketingAndSalesStrategy------------>
    digitalMarketingUsage = CharIntegerField(default=0,max_length=100)
    marketResearchForMarketing = CharIntegerField(default=0,max_length=100)
    marketingPlanningAndGuidelines = CharIntegerField(default=0,max_length=100)
    marketingAndSalesNetworking = CharIntegerField(default=0,max_length=100)
    innovativeMarketingUsage = CharIntegerField(default=0,max_length=100)
    exhibitionParticipation = CharIntegerField(default=0,max_length=100)

    # <------------SalesHistory------------>
    salesAmountToCostRatio = CharIntegerField(max_length=100, default=0)
    salesGrowthLast3Months = CharIntegerField(max_length=100, default=0)
    salesToProductionRatio = CharIntegerField(max_length=100, default=0)

    # <------------TargetMarketKnowledge------------>
    targetMarketDefinition = CharIntegerField(max_length=100, default=0)
    marketRegulationsKnowledge = CharIntegerField(max_length=100, default=0)
    competitorAwareness = CharIntegerField(max_length=100, default=0)

    # <------------ExportActivities------------>
    exportActivitiesAndGlobalMarketUse = CharIntegerField(max_length=100, default=0)


# <------------Human Resources------------>
class HumanResources(BaseDomain):
    # <------------Workforce Numbers------------>
    daily_operations_with_current_workforce = CharIntegerField(max_length=100, blank=True)
    backlog_of_daily_tasks = CharIntegerField(max_length=100, blank=True)
    available_workforce_for_new_projects = CharIntegerField(max_length=100, blank=True)

    # <------------Employee Retention------------>
    employees_with_minimum_5_years_experience = CharIntegerField(max_length=100, blank=True)
    employee_satisfaction_percentage = CharIntegerField(max_length=100, blank=True)
    employee_requests_for_new_jobs = CharIntegerField(max_length=100, blank=True)
    employee_requests_for_early_retirement = CharIntegerField(max_length=100, blank=True)
    organizational_support_for_employees = CharIntegerField(max_length=100, blank=True)
    annual_salary_increase_adjusted_for_inflation = CharIntegerField(max_length=100, blank=True)

    # <------------Employee Productivity------------>
    management_satisfaction_with_employees = CharIntegerField(max_length=100, blank=True)
    employee_satisfaction_with_management = CharIntegerField(max_length=100, blank=True)
    revenue_per_employee = CharIntegerField(max_length=100, blank=True)
    employee_responsibility_and_commitment = CharIntegerField(max_length=100, blank=True)

    # <------------Employee Performance Evaluation System------------>
    performance_evaluation_system_scheduling = CharIntegerField(max_length=100, blank=True)
    up_to_date_technology_in_performance_evaluation = CharIntegerField(max_length=100, blank=True)
    evaluation_criteria_alignment_with_job_description = CharIntegerField(max_length=100, blank=True)
    practical_model_for_employee_ranking = CharIntegerField(max_length=100, blank=True)

    # <------------Employee Training System------------>
    in_house_training_programs = CharIntegerField(max_length=100, blank=True)
    support_for_attending_training_programs = CharIntegerField(max_length=100, blank=True)

    # <------------Collaboration and Teamwork------------>
    manager_focus_on_team_processes = CharIntegerField(max_length=100, blank=True)
    employee_interest_in_group_work = CharIntegerField(max_length=100, blank=True)
    shared_workspaces_availability = CharIntegerField(max_length=100, blank=True)
    weekly_fixed_meetings = CharIntegerField(max_length=100, blank=True)
    manager_employee_interaction = CharIntegerField(max_length=100, blank=True)

    # <------------Ethical Values Awareness------------>
    respect_for_employee_privacy = CharIntegerField(max_length=100, blank=True)
    managers_behavior_towards_men_and_women = CharIntegerField(max_length=100, blank=True)


# <------------Financial Resources------------>
class FinancialResources(BaseDomain):
    # <------------Operating Cash Flow------------>
    ability_to_maintain_positive_cash_flow = CharIntegerField(max_length=100, blank=True)

    # <------------Current Ratio------------>
    ability_to_pay_financial_obligations = CharIntegerField(max_length=100, blank=True)

    # <------------Working Capital------------>
    assets_for_short_term_financial_obligations = CharIntegerField(max_length=100, blank=True)

    # <------------Capital Burn Rate------------>
    weekly_monthly_annual_expenses = CharIntegerField(max_length=100, blank=True)

    # <------------Net Profit Margin------------>
    profitability_efficiency_comparison = CharIntegerField(max_length=100, blank=True)

    # <------------Accounts Payable Turnover------------>
    ability_to_pay_accounts_payable = CharIntegerField(max_length=100, blank=True)

    # <------------Total Financial Performance Cost------------>
    payment_processing_costs = CharIntegerField(max_length=100, blank=True)

    # <------------Financial Activity Cost Ratio------------>
    financial_activity_cost_to_income_ratio = CharIntegerField(max_length=100, blank=True)

    # <------------Financial Error Reporting------------>
    financial_report_accuracy_and_completeness = CharIntegerField(max_length=100, blank=True)

    # <------------Budget Deviation------------>
    budget_vs_actual_difference = CharIntegerField(max_length=100, blank=True)

    # <------------Sales Growth------------>
    sales_change_over_period = CharIntegerField(max_length=100, blank=True)


# <------------Capital Structure------------>
class CapitalStructure(BaseDomain):
    # <------------Funding Sources------------>
    shareholder_funding_power = CharIntegerField(max_length=100, blank=True)
    availability_of_resources_for_new_projects = CharIntegerField(max_length=100, blank=True)

    # <------------Risk Tolerance------------>
    startup_investment_risk_tolerance = CharIntegerField(max_length=100, blank=True)


# <------------Management & Organizational Structure------------>
class ManagementOrganizationalStructure(BaseDomain):
    # <------------Organizational Chart------------>
    comprehensive_organizational_chart = CharIntegerField(max_length=100, blank=True)
    regular_chart_updates = CharIntegerField(max_length=100, blank=True)

    # <------------Knowledge and Information Management System------------>
    information_system_for_knowledge_management = CharIntegerField(max_length=100, blank=True)
    knowledge_management_system_integration = CharIntegerField(max_length=100, blank=True)

    # <------------Workplace Organization System------------>
    workspace_design = CharIntegerField(max_length=100, blank=True)
    five_s_in_daily_operations = CharIntegerField(max_length=100, blank=True)

    # <------------Management Strategy and Vision------------>
    vision_and_mission_definition = CharIntegerField(max_length=100, blank=True)
    employee_awareness_of_long_short_term_plans = CharIntegerField(max_length=100, blank=True)
    activities_for_increasing_customer_awareness = CharIntegerField(max_length=100, blank=True)

    # <------------Delegation of Authority------------>
    decision_making_power_for_lower_employees = CharIntegerField(max_length=100, blank=True)


# <------------Customer Relationship Management------------>
class CustomerRelationshipManagement(BaseDomain):
    # <------------Feedback System------------>
    purchase_info_documentation = CharIntegerField(max_length=100, blank=True)
    customer_feedback_system = CharIntegerField(max_length=100, blank=True)
    customer_feedback_analysis = CharIntegerField(max_length=100, blank=True)

    # <------------Facilities------------>
    special_sales_plan_for_loyal_customers = CharIntegerField(max_length=100, blank=True)
    loyal_customer_payment_benefits = CharIntegerField(max_length=100, blank=True)
    first_purchase_support_plan = CharIntegerField(max_length=100, blank=True)

    # <------------Customer Retention------------>
    employee_training_for_customer_interaction = CharIntegerField(max_length=100, blank=True)
    loyal_customer_count = CharIntegerField(max_length=100, blank=True)


class ManufacturingAndProduction(BaseDomain):
    # <------------Monthly Production------------>
    production_increase_planning = CharIntegerField(max_length=100, blank=True)
    safety_stock_level = CharIntegerField(max_length=100, blank=True)
    storage_cost = CharIntegerField(max_length=100, blank=True)
    production_stability = CharIntegerField(max_length=100, blank=True)
    max_capacity_utilization = CharIntegerField(max_length=100, blank=True)

    # <------------Production Management System------------>
    production_process_documentation = CharIntegerField(max_length=100, blank=True)
    defect_detection_and_resolution = CharIntegerField(max_length=100, blank=True)
    production_process_flexibility = CharIntegerField(max_length=100, blank=True)

    # <------------Production Technology------------>
    production_technology_level = CharIntegerField(max_length=100, blank=True)
    iot_equipment_in_production_line = CharIntegerField(max_length=100, blank=True)

    # <------------Market-Driven Production------------>
    production_sales_marketing_alignment = CharIntegerField(max_length=100, blank=True)

    # <------------Production Efficiency------------>
    output_input_ratio = CharIntegerField(max_length=100, blank=True)
    production_waste_ppm = CharIntegerField(max_length=100, blank=True)

    # <------------National and International Standards------------>
    required_certifications = CharIntegerField(max_length=100, blank=True)

    # <------------Warranty------------>
    warranty_after_sales = CharIntegerField(max_length=100, blank=True)
    warranty_commitment = CharIntegerField(max_length=100, blank=True)

    # <------------Quality Control System------------>
    quality_control_lab = CharIntegerField(max_length=100, blank=True)
    z = CharIntegerField(max_length=100, blank=True)


# <------------Research & Development------------>
class ResearchAndDevelopment(BaseDomain):
    # <------------Product Improvement------------>
    r_and_d_unit_defined_roles = CharIntegerField(max_length=100, blank=True)
    r_and_d_production_connection = CharIntegerField(max_length=100, blank=True)
    r_and_d_budget = CharIntegerField(max_length=100, blank=True)

    # <------------Innovation------------>
    innovation_planning = CharIntegerField(max_length=100, blank=True)
    innovation_process_guidelines = CharIntegerField(max_length=100, blank=True)
    customer_competitor_inspiration = CharIntegerField(max_length=100, blank=True)
    innovation_culture = CharIntegerField(max_length=100, blank=True)


# <------------Product Competitiveness------------>
class ProductCompetitiveness(BaseDomain):
    unique_feature = CharIntegerField(max_length=100, blank=True)


# <------------Branding------------>
class Branding(BaseDomain):
    has_documented_brand_identity = CharIntegerField(max_length=100,blank=True)
    has_defined_brand_personality = CharIntegerField(max_length=100,blank=True)
    tracks_and_manages_brand_reputation = CharIntegerField(max_length=100,blank=True)
    establishes_emotional_connection_with_customers = CharIntegerField(max_length=100,blank=True)
    has_brand_slogan = CharIntegerField(max_length=100,blank=True)
    has_customer_feedback_system = CharIntegerField(max_length=100,blank=True)
    is_brand_active_on_social_media = CharIntegerField(max_length=100,blank=True)
    employees_are_familiar_with_brand_values_and_mission = CharIntegerField(max_length=100,blank=True)
    is_brand_visual_design_consistent = CharIntegerField(max_length=100,blank=True)
    is_visual_design_of_brand_consistent = CharIntegerField(max_length=100,blank=True)






