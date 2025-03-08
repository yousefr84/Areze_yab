from django.db import models


# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100)
    registrationNumber = models.CharField(max_length=100)
    nationalID = models.CharField(max_length=100)


class SalesAndMarketing(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # <------------Branding------------>
    brandIdentity = models.IntegerField()
    visualIdentityActivities = models.IntegerField()
    brandReputationManagement = models.IntegerField()
    brandTrustAndEmotionalConnection = models.IntegerField()
    # <------------MarketShare------------>
    marketResearchOpportunities = models.IntegerField()
    salesToIndustryRatio = models.IntegerField()
    marketLeadershipPotential = models.IntegerField()
    # <------------DistributionAndSalesChannels------------>
    orderDeliveryTimeliness = models.IntegerField()
    salesNetworkCoverage = models.IntegerField()
    salesAgencySupervision = models.IntegerField()
    salesRepProductAwareness = models.IntegerField()
    reliableTransportUsage = models.IntegerField()

    # <------------MarketingAndSalesStrategy------------>
    digitalMarketingUsage = models.IntegerField()
    marketResearchForMarketing = models.IntegerField()
    marketingPlanningAndGuidelines = models.IntegerField()
    marketingAndSalesNetworking = models.IntegerField()
    innovativeMarketingUsage = models.IntegerField()
    exhibitionParticipation = models.IntegerField()

    # <------------SalesHistory------------>
    salesAmountToCostRatio = models.IntegerField()
    salesGrowthLast3Months = models.IntegerField()
    salesToProductionRatio = models.IntegerField()

    # <------------TargetMarketKnowledge------------>
    targetMarketDefinition = models.IntegerField()
    marketRegulationsKnowledge = models.IntegerField()
    competitorAwareness = models.IntegerField()

    # <------------ExportActivities------------>
    exportActivitiesAndGlobalMarketUse = models.IntegerField()


# <------------Human Resources------------>
class HumanResources(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # <------------Workforce Numbers------------>
    daily_operations_with_current_workforce = models.IntegerField()
    backlog_of_daily_tasks = models.IntegerField()
    available_workforce_for_new_projects = models.IntegerField()

    # <------------Employee Retention------------>
    employees_with_minimum_5_years_experience = models.IntegerField()
    employee_satisfaction_percentage = models.IntegerField()
    employee_requests_for_new_jobs = models.IntegerField()
    employee_requests_for_early_retirement = models.IntegerField()
    organizational_support_for_employees = models.IntegerField()
    annual_salary_increase_adjusted_for_inflation = models.IntegerField()

    # <------------Employee Productivity------------>
    management_satisfaction_with_employees = models.IntegerField()
    employee_satisfaction_with_management = models.IntegerField()
    revenue_per_employee = models.IntegerField()
    employee_responsibility_and_commitment = models.IntegerField()

    # <------------Employee Performance Evaluation System------------>
    performance_evaluation_system_scheduling = models.IntegerField()
    up_to_date_technology_in_performance_evaluation = models.IntegerField()
    evaluation_criteria_alignment_with_job_description = models.IntegerField()
    practical_model_for_employee_ranking = models.IntegerField()

    # <------------Employee Training System------------>
    in_house_training_programs = models.IntegerField()
    support_for_attending_training_programs = models.IntegerField()

    # <------------Collaboration and Teamwork------------>
    manager_focus_on_team_processes = models.IntegerField()
    employee_interest_in_group_work = models.IntegerField()
    shared_workspaces_availability = models.IntegerField()
    weekly_fixed_meetings = models.IntegerField()
    manager_employee_interaction = models.IntegerField()

    # <------------Ethical Values Awareness------------>
    respect_for_employee_privacy = models.IntegerField()
    managers_behavior_towards_men_and_women = models.IntegerField()


# <------------Financial Resources------------>
class FinancialResources(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # <------------Operating Cash Flow------------>
    ability_to_maintain_positive_cash_flow = models.IntegerField()

    # <------------Current Ratio------------>
    ability_to_pay_financial_obligations = models.IntegerField()

    # <------------Working Capital------------>
    assets_for_short_term_financial_obligations = models.IntegerField()

    # <------------Capital Burn Rate------------>
    weekly_monthly_annual_expenses = models.IntegerField()

    # <------------Net Profit Margin------------>
    profitability_efficiency_comparison = models.IntegerField()

    # <------------Accounts Payable Turnover------------>
    ability_to_pay_accounts_payable = models.IntegerField()

    # <------------Total Financial Performance Cost------------>
    payment_processing_costs = models.IntegerField()

    # <------------Financial Activity Cost Ratio------------>
    financial_activity_cost_to_income_ratio = models.IntegerField()

    # <------------Financial Error Reporting------------>
    financial_report_accuracy_and_completeness = models.IntegerField()

    # <------------Budget Deviation------------>
    budget_vs_actual_difference = models.IntegerField()

    # <------------Sales Growth------------>
    sales_change_over_period = models.IntegerField()


# <------------Capital Structure------------>
class CapitalStructure(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # <------------Funding Sources------------>
    shareholder_funding_power = models.IntegerField()
    availability_of_resources_for_new_projects = models.IntegerField()

    # <------------Risk Tolerance------------>
    startup_investment_risk_tolerance = models.IntegerField()


# <------------Management & Organizational Structure------------>
class ManagementOrganizationalStructure(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # <------------Organizational Chart------------>
    comprehensive_organizational_chart = models.IntegerField()
    regular_chart_updates = models.IntegerField()

    # <------------Knowledge and Information Management System------------>
    information_system_for_knowledge_management = models.IntegerField()
    knowledge_management_system_integration = models.IntegerField()

    # <------------Workplace Organization System------------>
    workspace_design = models.IntegerField()
    five_s_in_daily_operations = models.IntegerField()

    # <------------Management Strategy and Vision------------>
    vision_and_mission_definition = models.IntegerField()
    employee_awareness_of_long_short_term_plans = models.IntegerField()
    activities_for_increasing_customer_awareness = models.IntegerField()

    # <------------Delegation of Authority------------>
    decision_making_power_for_lower_employees = models.IntegerField()


# <------------Customer Relationship Management------------>
class CustomerRelationshipManagement(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


    # <------------Feedback System------------>
    purchase_info_documentation = models.IntegerField()
    customer_feedback_system = models.IntegerField()
    customer_feedback_analysis = models.IntegerField()

    # <------------Facilities------------>
    special_sales_plan_for_loyal_customers = models.IntegerField()
    loyal_customer_payment_benefits = models.IntegerField()
    first_purchase_support_plan = models.IntegerField()

    # <------------Customer Retention------------>
    employee_training_for_customer_interaction = models.IntegerField()
    loyal_customer_count = models.IntegerField()


class ManufacturingAndProduction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # <------------Monthly Production------------>
    production_increase_planning = models.IntegerField()
    safety_stock_level = models.IntegerField()
    storage_cost = models.IntegerField()
    production_stability = models.IntegerField()
    max_capacity_utilization = models.IntegerField()

    # <------------Production Management System------------>
    production_process_documentation = models.IntegerField()
    defect_detection_and_resolution = models.IntegerField()
    production_process_flexibility = models.IntegerField()

    # <------------Production Technology------------>
    production_technology_level = models.IntegerField()
    iot_equipment_in_production_line = models.IntegerField()

    # <------------Market-Driven Production------------>
    production_sales_marketing_alignment = models.IntegerField()

    # <------------Production Efficiency------------>
    output_input_ratio = models.IntegerField()
    production_waste_ppm = models.IntegerField()

    # <------------National and International Standards------------>
    required_certifications = models.IntegerField()

    # <------------Warranty------------>
    warranty_after_sales = models.IntegerField()
    warranty_commitment = models.IntegerField()

    # <------------Quality Control System------------>
    quality_control_lab = models.IntegerField()
    z = models.IntegerField()


# <------------Research & Development------------>
class ResearchAndDevelopment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # <------------Product Improvement------------>
    r_and_d_unit_defined_roles = models.IntegerField()
    r_and_d_production_connection = models.IntegerField()
    r_and_d_budget = models.IntegerField()

    # <------------Innovation------------>
    innovation_planning = models.IntegerField()
    innovation_process_guidelines = models.IntegerField()
    customer_competitor_inspiration = models.IntegerField()
    innovation_culture = models.IntegerField()


# <------------Product Competitiveness------------>
class ProductCompetitiveness(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    unique_feature = models.IntegerField()
