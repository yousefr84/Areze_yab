import re
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField


# Create your models here.

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
    size= models.CharField(max_length=100)


class BaseDomain(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=True)
    date = models.DateField(auto_now=True)


class SalesAndMarketing(BaseDomain):
    # <------------Branding------------>
    brandIdentity = CharField(max_length=100,blank=True,null=True)
    visualIdentityActivities = CharField(max_length=100,blank=True,null=True)
    brandReputationManagement = CharField(max_length=100,blank=True,null=True)
    brandTrustAndEmotionalConnection = CharField(max_length=100,blank=True,null=True)
    # <------------MarketShare------------>
    marketResearchOpportunities = CharField(max_length=100,blank=True,null=True)
    salesToIndustryRatio = CharField(max_length=100,blank=True,null=True)
    marketLeadershipPotential = CharField(max_length=100,blank=True,null=True)
    # <------------DistributionAndSalesChannels------------>
    orderDeliveryTimeliness = CharField(max_length=100,blank=True,null=True)
    salesNetworkCoverage = CharField(max_length=100,blank=True,null=True)
    salesAgencySupervision = CharField(max_length=100,blank=True,null=True)
    salesRepProductAwareness = CharField(max_length=100,blank=True,null=True)
    reliableTransportUsage = CharField(max_length=100,blank=True,null=True)

    # <------------MarketingAndSalesStrategy------------>
    digitalMarketingUsage = CharField(max_length=100,blank=True,null=True)
    marketResearchForMarketing = CharField(max_length=100,blank=True,null=True)
    marketingPlanningAndGuidelines = CharField(max_length=100,blank=True,null=True)
    marketingAndSalesNetworking = CharField(max_length=100,blank=True,null=True)
    innovativeMarketingUsage = CharField(max_length=100,blank=True,null=True)
    exhibitionParticipation = CharField(max_length=100,blank=True,null=True)

    # <------------SalesHistory------------>
    salesAmountToCostRatio = CharField(max_length=100,blank=True,null=True)
    salesGrowthLast3Months = CharField(max_length=100,blank=True,null=True)
    salesToProductionRatio = CharField(max_length=100,blank=True,null=True)

    # <------------TargetMarketKnowledge------------>
    targetMarketDefinition = CharField(max_length=100,blank=True,null=True)
    marketRegulationsKnowledge = CharField(max_length=100,blank=True,null=True)
    competitorAwareness = CharField(max_length=100,blank=True,null=True)

    # <------------ExportActivities------------>
    exportActivitiesAndGlobalMarketUse = CharField(max_length=100,blank=True,null=True)
    # <------------Branding------------>
    brandIdentityNum = models.IntegerField(default=0)
    visualIdentityActivitiesNum = models.IntegerField(default=0)
    brandReputationManagementNum = models.IntegerField(default=0)
    brandTrustAndEmotionalConnectionNum = models.IntegerField(default=0)
    # <------------MarketShare------------>
    marketResearchOpportunitiesNum = models.IntegerField(default=0)
    salesToIndustryRatioNum = models.IntegerField(default=0)
    marketLeadershipPotentialNum = models.IntegerField(default=0)
    # <------------DistributionAndSalesChannels------------>
    orderDeliveryTimelinessNum = models.IntegerField(default=0)
    salesNetworkCoverageNum = models.IntegerField(default=0)
    salesAgencySupervisionNum = models.IntegerField(default=0)
    salesRepProductAwarenessNum = models.IntegerField(default=0)
    reliableTransportUsageNum = models.IntegerField(default=0)

    # <------------MarketingAndSalesStrategy------------>
    digitalMarketingUsageNum = models.IntegerField(default=0)
    marketResearchForMarketingNum = models.IntegerField(default=0)
    marketingPlanningAndGuidelinesNum = models.IntegerField(default=0)
    marketingAndSalesNetworkingNum = models.IntegerField(default=0)
    innovativeMarketingUsageNum = models.IntegerField(default=0)
    exhibitionParticipationNum = models.IntegerField(default=0)

    # <------------SalesHistory------------>
    salesAmountToCostRatioNum = models.IntegerField(default=0)
    salesGrowthLast3MonthsNum = models.IntegerField(default=0)
    salesToProductionRatioNum = models.IntegerField(default=0)

    # <------------TargetMarketKnowledge------------>
    targetMarketDefinitionNum = models.IntegerField(default=0)
    marketRegulationsKnowledgeNum = models.IntegerField(default=0)
    competitorAwarenessNum = models.IntegerField(default=0)

    # <------------ExportActivities------------>
    exportActivitiesAndGlobalMarketUseNum = models.IntegerField(default=0)


# <------------Human Resources------------>
class HumanResources(BaseDomain):
    # <------------Workforce Numbers------------>
    daily_operations_with_current_workforce = CharField(max_length=100,blank=True,null=True)
    backlog_of_daily_tasks = CharField(max_length=100,blank=True,null=True)
    available_workforce_for_new_projects = CharField(max_length=100,blank=True,null=True)

    # <------------Employee Retention------------>
    employees_with_minimum_5_years_experience = CharField(max_length=100,blank=True,null=True)
    employee_satisfaction_percentage = CharField(max_length=100,blank=True,null=True)
    employee_requests_for_new_jobs = CharField(max_length=100,blank=True,null=True)
    employee_requests_for_early_retirement = CharField(max_length=100,blank=True,null=True)
    organizational_support_for_employees = CharField(max_length=100,blank=True,null=True)
    annual_salary_increase_adjusted_for_inflation = CharField(max_length=100,blank=True,null=True)

    # <------------Employee Productivity------------>
    management_satisfaction_with_employees = CharField(max_length=100,blank=True,null=True)
    employee_satisfaction_with_management = CharField(max_length=100,blank=True,null=True)
    revenue_per_employee = CharField(max_length=100,blank=True,null=True)
    employee_responsibility_and_commitment = CharField(max_length=100,blank=True,null=True)

    # <------------Employee Performance Evaluation System------------>
    performance_evaluation_system_scheduling = CharField(max_length=100,blank=True,null=True)
    up_to_date_technology_in_performance_evaluation = CharField(max_length=100,blank=True,null=True)
    evaluation_criteria_alignment_with_job_description = CharField(max_length=100,blank=True,null=True)
    practical_model_for_employee_ranking = CharField(max_length=100,blank=True,null=True)

    # <------------Employee Training System------------>
    in_house_training_programs = CharField(max_length=100,blank=True,null=True)
    support_for_attending_training_programs = CharField(max_length=100,blank=True,null=True)

    # <------------Collaboration and Teamwork------------>
    manager_focus_on_team_processes = CharField(max_length=100,blank=True,null=True)
    employee_interest_in_group_work = CharField(max_length=100,blank=True,null=True)
    shared_workspaces_availability = CharField(max_length=100,blank=True,null=True)
    weekly_fixed_meetings = CharField(max_length=100,blank=True,null=True)
    manager_employee_interaction = CharField(max_length=100,blank=True,null=True)

    # <------------Ethical Values Awareness------------>
    respect_for_employee_privacy = CharField(max_length=100,blank=True,null=True)
    managers_behavior_towards_men_and_women = CharField(max_length=100,blank=True,null=True)

    daily_operations_with_current_workforceNum = models.IntegerField(default=0)
    backlog_of_daily_tasksNum = models.IntegerField(default=0)
    available_workforce_for_new_projectsNum = models.IntegerField(default=0)

    # <------------Employee Retention------------>
    employees_with_minimum_5_years_experienceNum = models.IntegerField(default=0)
    employee_satisfaction_percentageNum = models.IntegerField(default=0)
    employee_requests_for_new_jobsNum = models.IntegerField(default=0)
    employee_requests_for_early_retirementNum = models.IntegerField(default=0)
    organizational_support_for_employeesNum = models.IntegerField(default=0)
    annual_salary_increase_adjusted_for_inflationNum = models.IntegerField(default=0)

    # <------------Employee Productivity------------>
    management_satisfaction_with_employeesNum = models.IntegerField(default=0)
    employee_satisfaction_with_managementNum = models.IntegerField(default=0)
    revenue_per_employeeNum = models.IntegerField(default=0)
    employee_responsibility_and_commitmentNum = models.IntegerField(default=0)

    # <------------Employee Performance Evaluation System------------>
    performance_evaluation_system_schedulingNum = models.IntegerField(default=0)
    up_to_date_technology_in_performance_evaluationNum = models.IntegerField(default=0)
    evaluation_criteria_alignment_with_job_descriptionNum = models.IntegerField(default=0)
    practical_model_for_employee_rankingNum = models.IntegerField(default=0)

    # <------------Employee Training System------------>
    in_house_training_programsNum = models.IntegerField(default=0)
    support_for_attending_training_programsNum = models.IntegerField(default=0)

    # <------------Collaboration and Teamwork------------>
    manager_focus_on_team_processesNum = models.IntegerField(default=0)
    employee_interest_in_group_workNum = models.IntegerField(default=0)
    shared_workspaces_availabilityNum = models.IntegerField(default=0)
    weekly_fixed_meetingsNum = models.IntegerField(default=0)
    manager_employee_interactionNum = models.IntegerField(default=0)

    # <------------Ethical Values Awareness------------>
    respect_for_employee_privacyNum = models.IntegerField(default=0)
    managers_behavior_towards_men_and_womenNum = models.IntegerField(default=0)


# <------------Financial Resources------------>
class FinancialResources(BaseDomain):
    # <------------Operating Cash Flow------------>
    ability_to_maintain_positive_cash_flow = CharField(max_length=100,blank=True,null=True)

    # <------------Current Ratio------------>
    ability_to_pay_financial_obligations = CharField(max_length=100,blank=True,null=True)

    # <------------Working Capital------------>
    assets_for_short_term_financial_obligations = CharField(max_length=100,blank=True,null=True)

    # <------------Capital Burn Rate------------>
    weekly_monthly_annual_expenses = CharField(max_length=100,blank=True,null=True)

    # <------------Net Profit Margin------------>
    profitability_efficiency_comparison = CharField(max_length=100,blank=True,null=True)

    # <------------Accounts Payable Turnover------------>
    ability_to_pay_accounts_payable = CharField(max_length=100,blank=True,null=True)

    # <------------Total Financial Performance Cost------------>
    payment_processing_costs = CharField(max_length=100,blank=True,null=True)

    # <------------Financial Activity Cost Ratio------------>
    financial_activity_cost_to_income_ratio = CharField(max_length=100,blank=True,null=True)

    # <------------Financial Error Reporting------------>
    financial_report_accuracy_and_completeness = CharField(max_length=100,blank=True,null=True)

    # <------------Budget Deviation------------>
    budget_vs_actual_difference = CharField(max_length=100,blank=True,null=True)

    # <------------Sales Growth------------>
    sales_change_over_period = CharField(max_length=100,blank=True,null=True)

    ability_to_maintain_positive_cash_flowNum = models.IntegerField(default=0)

    # <------------Current Ratio------------>
    ability_to_pay_financial_obligationsNum = models.IntegerField(default=0)

    # <------------Working Capital------------>
    assets_for_short_term_financial_obligationsNum = models.IntegerField(default=0)

    # <------------Capital Burn Rate------------>
    weekly_monthly_annual_expensesNum = models.IntegerField(default=0)

    # <------------Net Profit Margin------------>
    profitability_efficiency_comparisonNum = models.IntegerField(default=0)

    # <------------Accounts Payable Turnover------------>
    ability_to_pay_accounts_payableNum = models.IntegerField(default=0)

    # <------------Total Financial Performance Cost------------>
    payment_processing_costsNum = models.IntegerField(default=0)

    # <------------Financial Activity Cost Ratio------------>
    financial_activity_cost_to_income_ratioNum = models.IntegerField(default=0)

    # <------------Financial Error Reporting------------>
    financial_report_accuracy_and_completenessNum = models.IntegerField(default=0)

    # <------------Budget Deviation------------>
    budget_vs_actual_differenceNum = models.IntegerField(default=0)

    # <------------Sales Growth------------>
    sales_change_over_periodNum = models.IntegerField(default=0)

# <------------Capital Structure------------>
class CapitalStructure(BaseDomain):
    # <------------Funding Sources------------>
    shareholder_funding_power = CharField(max_length=100,blank=True,null=True)
    availability_of_resources_for_new_projects = CharField(max_length=100,blank=True,null=True)

    # <------------Risk Tolerance------------>
    startup_investment_risk_tolerance = CharField(max_length=100,blank=True,null=True)
    shareholder_funding_powerNum = models.IntegerField(default=0)
    availability_of_resources_for_new_projectsNum = models.IntegerField(default=0)

    # <------------Risk Tolerance------------>
    startup_investment_risk_toleranceNum = models.IntegerField(default=0)

# <------------Management & Organizational Structure------------>
class ManagementOrganizationalStructure(BaseDomain):
    # <------------Organizational Chart------------>
    comprehensive_organizational_chart = CharField(max_length=100,blank=True,null=True)
    regular_chart_updates = CharField(max_length=100,blank=True,null=True)

    # <------------Knowledge and Information Management System------------>
    information_system_for_knowledge_management = CharField(max_length=100,blank=True,null=True)
    knowledge_management_system_integration = CharField(max_length=100,blank=True,null=True)

    # <------------Workplace Organization System------------>
    workspace_design = CharField(max_length=100,blank=True,null=True)
    five_s_in_daily_operations = CharField(max_length=100,blank=True,null=True)

    # <------------Management Strategy and Vision------------>
    vision_and_mission_definition = CharField(max_length=100,blank=True,null=True)
    employee_awareness_of_long_short_term_plans = CharField(max_length=100,blank=True,null=True)
    activities_for_increasing_customer_awareness = CharField(max_length=100,blank=True,null=True)

    # <------------Delegation of Authority------------>
    decision_making_power_for_lower_employees = CharField(max_length=100,blank=True,null=True)
    # <------------Organizational Chart------------>
    comprehensive_organizational_chartNum = models.IntegerField(default=0)
    regular_chart_updatesNum = models.IntegerField(default=0)

    # <------------Knowledge and Information Management System------------>
    information_system_for_knowledge_managementNum = models.IntegerField(default=0)
    knowledge_management_system_integrationNum = models.IntegerField(default=0)

    # <------------Workplace Organization System------------>
    workspace_designNum = models.IntegerField(default=0)
    five_s_in_daily_operationsNum = models.IntegerField(default=0)

    # <------------Management Strategy and Vision------------>
    vision_and_mission_definitionNum = models.IntegerField(default=0)
    employee_awareness_of_long_short_term_plansNum = models.IntegerField(default=0)
    activities_for_increasing_customer_awarenessNum = models.IntegerField(default=0)

    # <------------Delegation of Authority------------>
    decision_making_power_for_lower_employeesNum = models.IntegerField(default=0)


# <------------Customer Relationship Management------------>
class CustomerRelationshipManagement(BaseDomain):
    # <------------Feedback System------------>
    purchase_info_documentation = CharField(max_length=100,blank=True,null=True)
    customer_feedback_system = CharField(max_length=100,blank=True,null=True)
    customer_feedback_analysis = CharField(max_length=100,blank=True,null=True)

    # <------------Facilities------------>
    special_sales_plan_for_loyal_customers = CharField(max_length=100,blank=True,null=True)
    loyal_customer_payment_benefits = CharField(max_length=100,blank=True,null=True)
    first_purchase_support_plan = CharField(max_length=100,blank=True,null=True)

    # <------------Customer Retention------------>
    employee_training_for_customer_interaction = CharField(max_length=100,blank=True,null=True)
    loyal_customer_count = CharField(max_length=100,blank=True,null=True)


    # <------------Feedback System------------>
    purchase_info_documentationNum = models.IntegerField(default=0)
    customer_feedback_systemNum = models.IntegerField(default=0)
    customer_feedback_analysisNum = models.IntegerField(default=0)

    # <------------Facilities------------>
    special_sales_plan_for_loyal_customersNum = models.IntegerField(default=0)
    loyal_customer_payment_benefitsNum = models.IntegerField(default=0)
    first_purchase_support_planNum = models.IntegerField(default=0)

    # <------------Customer Retention------------>
    employee_training_for_customer_interactionNum = models.IntegerField(default=0)
    loyal_customer_countNum = models.IntegerField(default=0)

class ManufacturingAndProduction(BaseDomain):
    # <------------Monthly Production------------>
    production_increase_planning = CharField(max_length=100,blank=True,null=True)
    safety_stock_level = CharField(max_length=100,blank=True,null=True)
    storage_cost = CharField(max_length=100,blank=True,null=True)
    production_stability = CharField(max_length=100,blank=True,null=True)
    max_capacity_utilization = CharField(max_length=100,blank=True,null=True)

    # <------------Production Management System------------>
    production_process_documentation = CharField(max_length=100,blank=True,null=True)
    defect_detection_and_resolution = CharField(max_length=100,blank=True,null=True)
    production_process_flexibility = CharField(max_length=100,blank=True,null=True)

    # <------------Production Technology------------>
    production_technology_level = CharField(max_length=100,blank=True,null=True)
    iot_equipment_in_production_line = CharField(max_length=100,blank=True,null=True)

    # <------------Market-Driven Production------------>
    production_sales_marketing_alignment = CharField(max_length=100,blank=True,null=True)

    # <------------Production Efficiency------------>
    output_input_ratio = CharField(max_length=100,blank=True,null=True)
    production_waste_ppm = CharField(max_length=100,blank=True,null=True)

    # <------------National and International Standards------------>
    required_certifications = CharField(max_length=100,blank=True,null=True)

    # <------------Warranty------------>
    warranty_after_sales = CharField(max_length=100,blank=True,null=True)
    warranty_commitment = CharField(max_length=100,blank=True,null=True)

    # <------------Quality Control System------------>
    quality_control_lab = CharField(max_length=100,blank=True,null=True)
    z = CharField(max_length=100,blank=True,null=True)



    production_increase_planningNum = models.IntegerField(default=0)
    safety_stock_levelNum = models.IntegerField(default=0)
    storage_costNum = models.IntegerField(default=0)
    production_stabilityNum = models.IntegerField(default=0)
    max_capacity_utilizationNum = models.IntegerField(default=0)

    # <------------Production Management System------------>
    production_process_documentationNum = models.IntegerField(default=0)
    defect_detection_and_resolutionNum = models.IntegerField(default=0)
    production_process_flexibilityNum = models.IntegerField(default=0)

    # <------------Production Technology------------>
    production_technology_levelNum = models.IntegerField(default=0)
    iot_equipment_in_production_lineNum = models.IntegerField(default=0)

    # <------------Market-Driven Production------------>
    production_sales_marketing_alignmentNum = models.IntegerField(default=0)

    # <------------Production Efficiency------------>
    output_input_ratioNum = models.IntegerField(default=0)
    production_waste_ppmNum = models.IntegerField(default=0)

    # <------------National and International Standards------------>
    required_certificationsNum = models.IntegerField(default=0)

    # <------------Warranty------------>
    warranty_after_salesNum = models.IntegerField(default=0)
    warranty_commitmentNum = models.IntegerField(default=0)

    # <------------Quality Control System------------>
    quality_control_labNum = models.IntegerField(default=0)
    zNum = models.IntegerField(default=0)


# <------------Research & Development------------>
class ResearchAndDevelopment(BaseDomain):
    # <------------Product Improvement------------>
    r_and_d_unit_defined_roles = CharField(max_length=100,blank=True,null=True)
    r_and_d_production_connection = CharField(max_length=100,blank=True,null=True)
    r_and_d_budget = CharField(max_length=100,blank=True,null=True)

    # <------------Innovation------------>
    innovation_planning = CharField(max_length=100,blank=True,null=True)
    innovation_process_guidelines = CharField(max_length=100,blank=True,null=True)
    customer_competitor_inspiration = CharField(max_length=100,blank=True,null=True)
    innovation_culture = CharField(max_length=100,blank=True,null=True)


    # <------------Product Improvement------------>
    r_and_d_unit_defined_rolesNum = models.IntegerField(default=0)
    r_and_d_production_connectionNum = models.IntegerField(default=0)
    r_and_d_budgetNum = models.IntegerField(default=0)

    # <------------Innovation------------>
    innovation_planningNum = models.IntegerField(default=0)
    innovation_process_guidelinesNum = models.IntegerField(default=0)
    customer_competitor_inspirationNum = models.IntegerField(default=0)
    innovation_cultureNum = models.IntegerField(default=0)


# <------------Product Competitiveness------------>
class ProductCompetitiveness(BaseDomain):
    unique_feature = CharField(max_length=100,blank=True,null=True)
    unique_featureNum = models.IntegerField(default=0)

# <------------Branding------------>
class Branding(BaseDomain):
    has_documented_brand_identity = CharField(max_length=100,blank=True,null=True)
    has_defined_brand_personality = CharField(max_length=100,blank=True,null=True)
    tracks_and_manages_brand_reputation = CharField(max_length=100,blank=True,null=True)
    establishes_emotional_connection_with_customers = CharField(max_length=100,blank=True,null=True)
    has_brand_slogan = CharField(max_length=100,blank=True,null=True)
    has_customer_feedback_system = CharField(max_length=100,blank=True,null=True)
    is_brand_active_on_social_media = CharField(max_length=100,blank=True,null=True)
    employees_are_familiar_with_brand_values_and_mission = CharField(max_length=100,blank=True,null=True)
    is_brand_visual_design_consistent = CharField(max_length=100,blank=True,null=True)
    is_visual_design_of_brand_consistent = CharField(max_length=100,blank=True,null=True)




    has_documented_brand_identityNum = models.IntegerField(default=0)
    has_defined_brand_personalityNum = models.IntegerField(default=0)
    tracks_and_manages_brand_reputationNum = models.IntegerField(default=0)
    establishes_emotional_connection_with_customersNum = models.IntegerField(default=0)
    has_brand_sloganNum = models.IntegerField(default=0)
    has_customer_feedback_systemNum = models.IntegerField(default=0)
    is_brand_active_on_social_mediaNum = models.IntegerField(default=0)
    employees_are_familiar_with_brand_values_and_missionNum = models.IntegerField(default=0)
    is_brand_visual_design_consistentNum = models.IntegerField(default=0)
    is_visual_design_of_brand_consistentNum = models.IntegerField(default=0)
    






