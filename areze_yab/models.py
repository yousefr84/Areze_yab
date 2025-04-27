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
    size = models.CharField(max_length=100)
    company_domain = models.CharField(max_length=100)
    is_company = models.BooleanField(default=True)


class BaseDomain(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=True)
    date = models.DateField(auto_now=True)


class SalesAndMarketingS(BaseDomain):
    documented_sales_strategy = models.CharField(max_length=100, blank=True, null=True)
    sales_strategy_alignment_with_goals = models.CharField(max_length=100, blank=True, null=True)
    documented_and_transparent_sales_process = models.CharField(max_length=100, blank=True, null=True)
    regular_post_sale_follow_up = models.CharField(max_length=100, blank=True, null=True)
    adequate_sales_team_size_and_expertise = models.CharField(max_length=100, blank=True, null=True)
    sales_team_training_program = models.CharField(max_length=100, blank=True, null=True)
    regular_market_analysis_for_opportunities_and_threats = models.CharField(max_length=100, blank=True, null=True)
    accurate_up_to_date_target_market_data = models.CharField(max_length=100, blank=True, null=True)
    customer_relationship_management_system = models.CharField(max_length=100, blank=True, null=True)
    regular_customer_data_and_experience_analysis = models.CharField(max_length=100, blank=True, null=True)
    digital_marketing_tools_usage = models.CharField(max_length=100, blank=True, null=True)
    digital_marketing_sales_strategy_alignment = models.CharField(max_length=100, blank=True, null=True)
    special_offers_targeted_discounts_for_sales = models.CharField(max_length=100, blank=True, null=True)

    documented_sales_strategyNum = models.IntegerField(default=0)
    sales_strategy_alignment_with_goalsNum = models.IntegerField(default=0)
    documented_and_transparent_sales_processNum = models.IntegerField(default=0)
    regular_post_sale_follow_upNum = models.IntegerField(default=0)
    adequate_sales_team_size_and_expertiseNum = models.IntegerField(default=0)
    sales_team_training_programNum = models.IntegerField(default=0)
    regular_market_analysis_for_opportunities_and_threatsNum = models.IntegerField(default=0)
    accurate_up_to_date_target_market_dataNum = models.IntegerField(default=0)
    customer_relationship_management_systemNum = models.IntegerField(default=0)
    regular_customer_data_and_experience_analysisNum = models.IntegerField(default=0)
    digital_marketing_tools_usageNum = models.IntegerField(default=0)
    digital_marketing_sales_strategy_alignmentNum = models.IntegerField(default=0)
    special_offers_targeted_discounts_for_salesNum = models.IntegerField(default=0)


class SalesAndMarketingM(BaseDomain):
    regular_sales_strategy_updates = models.CharField(max_length=100, blank=True, null=True)
    sales_strategy_suitability_for_target_segments = models.CharField(max_length=100, blank=True, null=True)
    sales_strategy_with_short_long_term_goals = models.CharField(max_length=100, blank=True, null=True)
    documented_transparent_sales_process_for_team = models.CharField(max_length=100, blank=True, null=True)
    using_specialized_software_for_sales_process_management = models.CharField(max_length=100, blank=True, null=True)
    sales_process_flexibility_for_market_changes = models.CharField(max_length=100, blank=True, null=True)
    using_data_analytics_to_improve_sales_process = models.CharField(max_length=100, blank=True, null=True)
    regular_evaluation_of_sales_team_based_on_performance = models.CharField(max_length=100, blank=True, null=True)
    continuous_training_for_sales_team_skills = models.CharField(max_length=100, blank=True, null=True)
    sales_team_goals_alignment_with_company_goals = models.CharField(max_length=100, blank=True, null=True)
    regular_feedback_and_coaching_for_sales_team = models.CharField(max_length=100, blank=True, null=True)
    regular_market_analysis = models.CharField(max_length=100, blank=True, null=True)
    competitor_analysis_and_using_data_for_sales_strategy = models.CharField(max_length=100, blank=True, null=True)
    market_analysis_attention_to_new_needs_and_demand_changes = models.CharField(max_length=100, blank=True, null=True)
    advanced_crm_system_for_customer_relationship_management = models.CharField(max_length=100, blank=True, null=True)
    crm_system_ability_to_analyze_customer_data_and_behavior = models.CharField(max_length=100, blank=True, null=True)
    digital_analytics_tools_for_evaluating_marketing_campaigns = models.CharField(max_length=100, blank=True, null=True)
    optimizing_digital_marketing_based_on_analytics_data = models.CharField(max_length=100, blank=True, null=True)
    regular_targeted_advertising_for_new_customers = models.CharField(max_length=100, blank=True, null=True)
    using_discounts_and_special_offers_for_sales_promotion = models.CharField(max_length=100, blank=True, null=True)

    regular_sales_strategy_updatesNum = models.IntegerField(default=0)
    sales_strategy_suitability_for_target_segmentsNum = models.IntegerField(default=0)
    sales_strategy_with_short_long_term_goalsNum = models.IntegerField(default=0)
    documented_transparent_sales_process_for_teamNum = models.IntegerField(default=0)
    using_specialized_software_for_sales_process_managementNum = models.IntegerField(default=0)
    sales_process_flexibility_for_market_changesNum = models.IntegerField(default=0)
    using_data_analytics_to_improve_sales_processNum = models.IntegerField(default=0)
    regular_evaluation_of_sales_team_based_on_performanceNum = models.IntegerField(default=0)
    continuous_training_for_sales_team_skillsNum = models.IntegerField(default=0)
    sales_team_goals_alignment_with_company_goalsNum = models.IntegerField(default=0)
    regular_feedback_and_coaching_for_sales_teamNum = models.IntegerField(default=0)
    regular_market_analysisNum = models.IntegerField(default=0)
    competitor_analysis_and_using_data_for_sales_strategyNum = models.IntegerField(default=0)
    market_analysis_attention_to_new_needs_and_demand_changesNum = models.IntegerField(default=0)
    advanced_crm_system_for_customer_relationship_managementNum = models.IntegerField(default=0)
    crm_system_ability_to_analyze_customer_data_and_behaviorNum = models.IntegerField(default=0)
    digital_analytics_tools_for_evaluating_marketing_campaignsNum = models.IntegerField(default=0)
    optimizing_digital_marketing_based_on_analytics_dataNum = models.IntegerField(default=0)
    regular_targeted_advertising_for_new_customersNum = models.IntegerField(default=0)
    using_discounts_and_special_offers_for_sales_promotionNum = models.IntegerField(default=0)


class SalesAndMarketingL(BaseDomain):
    sales_strategy_including_multiple_channels_online_offline_partners = models.CharField(max_length=100, blank=True,
                                                                                          null=True,
                                                                                          db_column="sales_channels_strategy")
    sales_strategy_tailored_for_each_target_market = models.CharField(max_length=100, blank=True, null=True)
    sales_strategy_with_plans_for_new_market_development = models.CharField(max_length=100, blank=True, null=True)
    automated_sales_process_for_efficiency_and_error_reduction = models.CharField(max_length=100, blank=True, null=True)
    kpis_defined_for_each_stage_of_sales_process = models.CharField(max_length=100, blank=True, null=True)
    regular_evaluation_and_improvement_of_sales_process = models.CharField(max_length=100, blank=True, null=True)
    using_market_experiences_and_customer_feedback_for_sales_strategy_improvement = models.CharField(max_length=100,
                                                                                                     blank=True,
                                                                                                     null=True,
                                                                                                     db_column="market_feedback_strategy_improvement")
    performance_based_motivational_programs_for_sales_team = models.CharField(max_length=100, blank=True, null=True)
    continuous_sales_training_for_team = models.CharField(max_length=100, blank=True, null=True)
    advanced_market_analysis_tools = models.CharField(max_length=100, blank=True, null=True)
    identifying_new_markets_with_updated_data = models.CharField(max_length=100, blank=True, null=True)
    crm_integrated_with_other_systems = models.CharField(max_length=100, blank=True, null=True)
    crm_real_time_customer_data_update = models.CharField(max_length=100, blank=True, null=True)
    advanced_digital_marketing_tools_usage = models.CharField(max_length=100, blank=True, null=True)
    digital_campaign_optimization_based_on_data_analysis = models.CharField(max_length=100, blank=True, null=True)
    advertising_campaign_alignment_with_target_customers = models.CharField(max_length=100, blank=True, null=True)
    advertising_adjustment_based_on_customer_needs = models.CharField(max_length=100, blank=True, null=True)

    sales_strategy_including_multiple_channels_online_offline_partnersNum = models.IntegerField(default=0,
                                                                                                db_column="sales_channels_strategy_num")
    sales_strategy_tailored_for_each_target_marketNum = models.IntegerField(default=0)
    sales_strategy_with_plans_for_new_market_developmentNum = models.IntegerField(default=0)
    automated_sales_process_for_efficiency_and_error_reductionNum = models.IntegerField(default=0)
    kpis_defined_for_each_stage_of_sales_processNum = models.IntegerField(default=0)
    regular_evaluation_and_improvement_of_sales_processNum = models.IntegerField(default=0)
    using_market_experiences_and_customer_feedback_for_sales_strategy_improvementNum = models.IntegerField(default=0,
                                                                                                           db_column="market_feedback_strategy_improvement_num")
    performance_based_motivational_programs_for_sales_teamNum = models.IntegerField(default=0)
    continuous_sales_training_for_teamNum = models.IntegerField(default=0)
    advanced_market_analysis_toolsNum = models.IntegerField(default=0)
    identifying_new_markets_with_updated_dataNum = models.IntegerField(default=0)
    crm_integrated_with_other_systemsNum = models.IntegerField(default=0)
    crm_real_time_customer_data_updateNum = models.IntegerField(default=0)
    advanced_digital_marketing_tools_usageNum = models.IntegerField(default=0)
    digital_campaign_optimization_based_on_data_analysisNum = models.IntegerField(default=0)
    advertising_campaign_alignment_with_target_customersNum = models.IntegerField(default=0)
    advertising_adjustment_based_on_customer_needsNum = models.IntegerField(default=0)


# <------------Human Resources------------>
class HumanResourcesS(BaseDomain):
    staffing_sufficiency = models.CharField(max_length=100, blank=True, null=True)
    recruitment_planning = models.CharField(max_length=100, blank=True, null=True)
    employee_turnover_rate = models.CharField(max_length=100, blank=True, null=True)
    employee_turnover_reasons_attention = models.CharField(max_length=100, blank=True, null=True)
    employee_performance_evaluation = models.CharField(max_length=100, blank=True, null=True)
    employee_productivity_tool = models.CharField(max_length=100, blank=True, null=True)
    performance_evaluation_impact = models.CharField(max_length=100, blank=True, null=True)
    employee_training_programs = models.CharField(max_length=100, blank=True, null=True)
    training_impact_on_performance = models.CharField(max_length=100, blank=True, null=True)
    employee_collaboration_effectiveness = models.CharField(max_length=100, blank=True, null=True)
    teamwork_culture_exists = models.CharField(max_length=100, blank=True, null=True)
    ethical_standards_attention = models.CharField(max_length=100, blank=True, null=True)
    employee_professional_ethics = models.CharField(max_length=100, blank=True, null=True)

    staffing_sufficiencyNum = models.IntegerField(default=0)
    recruitment_planningNum = models.IntegerField(default=0)
    employee_turnover_rateNum = models.IntegerField(default=0)
    employee_turnover_reasons_attentionNum = models.IntegerField(default=0)
    employee_performance_evaluationNum = models.IntegerField(default=0)
    employee_productivity_toolNum = models.IntegerField(default=0)
    performance_evaluation_impactNum = models.IntegerField(default=0)
    employee_training_programsNum = models.IntegerField(default=0)
    training_impact_on_performanceNum = models.IntegerField(default=0)
    employee_collaboration_effectivenessNum = models.IntegerField(default=0)
    teamwork_culture_existsNum = models.IntegerField(default=0)
    ethical_standards_attentionNum = models.IntegerField(default=0)
    employee_professional_ethicsNum = models.IntegerField(default=0)


class HumanResourcesM(BaseDomain):
    staffing_vs_workload = models.CharField(max_length=100, blank=True, null=True)
    recruitment_plan = models.CharField(max_length=100, blank=True, null=True)
    employee_retention_level = models.CharField(max_length=100, blank=True, null=True)
    employee_exit_reasons_analysis = models.CharField(max_length=100, blank=True, null=True)
    key_employee_retention_plan = models.CharField(max_length=100, blank=True, null=True)
    employee_performance_measurability = models.CharField(max_length=100, blank=True, null=True)
    productivity_evaluator = models.CharField(max_length=100, blank=True, null=True)
    employee_exit_alignment_with_goals = models.CharField(max_length=100, blank=True, null=True)
    structured_performance_evaluation = models.CharField(max_length=100, blank=True, null=True)
    performance_evaluation_salary_promotion_impact = models.CharField(max_length=100, blank=True, null=True)
    performance_evaluation_impact_on_salary_promotion = models.CharField(max_length=100, blank=True, null=True)
    continuous_employee_training = models.CharField(max_length=100, blank=True, null=True)
    training_effectiveness_evaluation = models.CharField(max_length=100, blank=True, null=True)
    training_budget_allocation = models.CharField(max_length=100, blank=True, null=True)
    interdepartmental_collaboration = models.CharField(max_length=100, blank=True, null=True)
    collaboration_enhancement_programs = models.CharField(max_length=100, blank=True, null=True)
    teamwork_culture = models.CharField(max_length=100, blank=True, null=True)
    ethical_behavior_of_employees = models.CharField(max_length=100, blank=True, null=True)
    managers_as_role_models_for_ethics = models.CharField(max_length=100, blank=True, null=True)
    professional_ethics_code = models.CharField(max_length=100, blank=True, null=True)

    staffing_vs_workloadNum = models.IntegerField(default=0)
    recruitment_planNum = models.IntegerField(default=0)
    employee_retention_levelNum = models.IntegerField(default=0)
    employee_exit_reasons_analysisNum = models.IntegerField(default=0)
    key_employee_retention_planNum = models.IntegerField(default=0)
    employee_performance_measurabilityNum = models.IntegerField(default=0)
    productivity_evaluatorNum = models.IntegerField(default=0)
    employee_exit_alignment_with_goalsNum = models.IntegerField(default=0)
    structured_performance_evaluationNum = models.IntegerField(default=0)
    performance_evaluation_salary_promotion_impactNum = models.IntegerField(default=0)
    performance_evaluation_impact_on_salary_promotionNum = models.IntegerField(default=0)
    continuous_employee_trainingNum = models.IntegerField(default=0)
    training_effectiveness_evaluationNum = models.IntegerField(default=0)
    training_budget_allocationNum = models.IntegerField(default=0)
    interdepartmental_collaborationNum = models.IntegerField(default=0)
    collaboration_enhancement_programsNum = models.IntegerField(default=0)
    teamwork_cultureNum = models.IntegerField(default=0)
    ethical_behavior_of_employeesNum = models.IntegerField(default=0)
    managers_as_role_models_for_ethicsNum = models.IntegerField(default=0)
    professional_ethics_codeNum = models.IntegerField(default=0)


class HumanResourcesL(BaseDomain):
    current_staff_meets_workload = models.CharField(max_length=100, blank=True, null=True)
    organizational_structure_updated_for_growth = models.CharField(max_length=100, blank=True, null=True)
    employee_turnover_rate_last_year = models.CharField(max_length=100, blank=True, null=True)
    employee_satisfaction_loyalty_program = models.CharField(max_length=100, blank=True, null=True)
    key_department_productivity_evaluation = models.CharField(max_length=100, blank=True, null=True)
    resources_for_productivity_increase = models.CharField(max_length=100, blank=True, null=True)
    formal_performance_evaluation_system = models.CharField(max_length=100, blank=True, null=True)
    feedback_leads_to_performance_improvement = models.CharField(max_length=100, blank=True, null=True)
    structured_training_program_exists = models.CharField(max_length=100, blank=True, null=True)
    training_leads_to_performance_improvement = models.CharField(max_length=100, blank=True, null=True)
    team_collaboration_level = models.CharField(max_length=100, blank=True, null=True)
    team_conflict_management = models.CharField(max_length=100, blank=True, null=True)
    ethical_values_in_behavior = models.CharField(max_length=100, blank=True, null=True)
    ethical_values_in_recruitment = models.CharField(max_length=100, blank=True, null=True)

    current_staff_meets_workloadNum = models.IntegerField(default=0)
    organizational_structure_updated_for_growthNum = models.IntegerField(default=0)
    employee_turnover_rate_last_yearNum = models.IntegerField(default=0)
    employee_satisfaction_loyalty_programNum = models.IntegerField(default=0)
    key_department_productivity_evaluationNum = models.IntegerField(default=0)
    resources_for_productivity_increaseNum = models.IntegerField(default=0)
    formal_performance_evaluation_systemNum = models.IntegerField(default=0)
    feedback_leads_to_performance_improvementNum = models.IntegerField(default=0)
    structured_training_program_existsNum = models.IntegerField(default=0)
    training_leads_to_performance_improvementNum = models.IntegerField(default=0)
    team_collaboration_levelNum = models.IntegerField(default=0)
    team_conflict_managementNum = models.IntegerField(default=0)
    ethical_values_in_behaviorNum = models.IntegerField(default=0)
    ethical_values_in_recruitmentNum = models.IntegerField(default=0)


# <------------Branding------------>
class BrandingS(BaseDomain):
    brand_identity_clarity = models.CharField(max_length=100, blank=True, null=True)
    staff_brand_awareness = models.CharField(max_length=100, blank=True, null=True)
    customer_brand_awareness = models.CharField(max_length=100, blank=True, null=True)
    social_media_presence = models.CharField(max_length=100, blank=True, null=True)
    customer_brand_experience = models.CharField(max_length=100, blank=True, null=True)
    customer_feedback_usage = models.CharField(max_length=100, blank=True, null=True)
    customer_loyalty_programs = models.CharField(max_length=100, blank=True, null=True)
    repeat_purchase_frequency = models.CharField(max_length=100, blank=True, null=True)
    willingness_to_pay_more = models.CharField(max_length=100, blank=True, null=True)
    brand_performance_evaluation = models.CharField(max_length=100, blank=True, null=True)
    customer_data_for_performance = models.CharField(max_length=100, blank=True, null=True)
    brand_strategy_documentation = models.CharField(max_length=100, blank=True, null=True)
    continuous_brand_investment = models.CharField(max_length=100, blank=True, null=True)
    current_brand_innovation = models.CharField(max_length=100, blank=True, null=True)

    brand_identity_clarityNum = models.IntegerField(default=0)
    staff_brand_awarenessNum = models.IntegerField(default=0)
    customer_brand_awarenessNum = models.IntegerField(default=0)
    social_media_presenceNum = models.IntegerField(default=0)
    customer_brand_experienceNum = models.IntegerField(default=0)
    customer_feedback_usageNum = models.IntegerField(default=0)
    customer_loyalty_programsNum = models.IntegerField(default=0)
    repeat_purchase_frequencyNum = models.IntegerField(default=0)
    willingness_to_pay_moreNum = models.IntegerField(default=0)
    brand_performance_evaluationNum = models.IntegerField(default=0)
    customer_data_for_performanceNum = models.IntegerField(default=0)
    brand_strategy_documentationNum = models.IntegerField(default=0)
    continuous_brand_investmentNum = models.IntegerField(default=0)
    current_brand_innovationNum = models.IntegerField(default=0)


class BrandingM(BaseDomain):
    clear_brand_identity = models.CharField(max_length=100, blank=True, null=True)
    brand_identity_alignment_with_strategy = models.CharField(max_length=100, blank=True, null=True)
    brand_identity_for_cultural_clarity = models.CharField(max_length=100, blank=True, null=True)
    brand_recognition_in_target_market = models.CharField(max_length=100, blank=True, null=True)
    digital_advertising_for_brand_awareness = models.CharField(max_length=100, blank=True, null=True)
    advertising_campaigns_for_brand_awareness = models.CharField(max_length=100, blank=True, null=True)
    brand_association_with_quality = models.CharField(max_length=100, blank=True, null=True)
    market_research_for_customer_experience = models.CharField(max_length=100, blank=True, null=True)
    customer_feedback_for_brand_experience = models.CharField(max_length=100, blank=True, null=True)
    processes_for_measuring_customer_experience = models.CharField(max_length=100, blank=True, null=True)
    customer_feedback_for_product_service_improvement = models.CharField(max_length=100, blank=True, null=True)
    special_programs_for_customer_loyalty = models.CharField(max_length=100, blank=True, null=True)
    loyal_customers_for_brand_promotion = models.CharField(max_length=100, blank=True, null=True)
    customer_loyalty_rewards = models.CharField(max_length=100, blank=True, null=True)
    regular_brand_performance_evaluation = models.CharField(max_length=100, blank=True, null=True)

    clear_brand_identityNum = models.IntegerField(default=0)
    brand_identity_alignment_with_strategyNum = models.IntegerField(default=0)
    brand_identity_for_cultural_clarityNum = models.IntegerField(default=0)
    brand_recognition_in_target_marketNum = models.IntegerField(default=0)
    digital_advertising_for_brand_awarenessNum = models.IntegerField(default=0)
    advertising_campaigns_for_brand_awarenessNum = models.IntegerField(default=0)
    brand_association_with_qualityNum = models.IntegerField(default=0)
    market_research_for_customer_experienceNum = models.IntegerField(default=0)
    customer_feedback_for_brand_experienceNum = models.IntegerField(default=0)
    processes_for_measuring_customer_experienceNum = models.IntegerField(default=0)
    customer_feedback_for_product_service_improvementNum = models.IntegerField(default=0)
    special_programs_for_customer_loyaltyNum = models.IntegerField(default=0)
    loyal_customers_for_brand_promotionNum = models.IntegerField(default=0)
    customer_loyalty_rewardsNum = models.IntegerField(default=0)
    regular_brand_performance_evaluationNum = models.IntegerField(default=0)


class BrandingL(BaseDomain):
    brand_identity_alignment_with_culture = models.CharField(max_length=100, blank=True, null=True)
    employee_involvement_in_brand_identity = models.CharField(max_length=100, blank=True, null=True)
    brand_identity_implementation_at_touchpoints = models.CharField(max_length=100, blank=True, null=True)
    use_of_various_ad_campaigns_for_brand_awareness = models.CharField(max_length=100, blank=True, null=True)
    use_of_multiple_channels_for_brand_promotion = models.CharField(max_length=100, blank=True, null=True)
    use_of_data_and_analytics_in_ad_campaign_evaluation = models.CharField(max_length=100, blank=True, null=True)
    regular_brand_awareness_evaluation = models.CharField(max_length=100, blank=True, null=True)
    market_research_for_brand_experience = models.CharField(max_length=100, blank=True, null=True)
    using_customer_data_for_brand_personalization = models.CharField(max_length=100, blank=True, null=True)
    regular_customer_experience_evaluation = models.CharField(max_length=100, blank=True, null=True)
    using_customer_feedback_for_brand_experience_improvement = models.CharField(max_length=100, blank=True, null=True)
    has_loyalty_program_for_customers = models.CharField(max_length=100, blank=True, null=True)
    use_loyal_customers_for_brand_awareness = models.CharField(max_length=100, blank=True, null=True)

    brand_identity_alignment_with_cultureNum = models.IntegerField(default=0)
    employee_involvement_in_brand_identityNum = models.IntegerField(default=0)
    brand_identity_implementation_at_touchpointsNum = models.IntegerField(default=0)
    use_of_various_ad_campaigns_for_brand_awarenessNum = models.IntegerField(default=0)
    use_of_multiple_channels_for_brand_promotionNum = models.IntegerField(default=0)
    use_of_data_and_analytics_in_ad_campaign_evaluationNum = models.IntegerField(default=0)
    regular_brand_awareness_evaluationNum = models.IntegerField(default=0)
    market_research_for_brand_experienceNum = models.IntegerField(default=0)
    using_customer_data_for_brand_personalizationNum = models.IntegerField(default=0)
    regular_customer_experience_evaluationNum = models.IntegerField(default=0)
    using_customer_feedback_for_brand_experience_improvementNum = models.IntegerField(default=0)
    has_loyalty_program_for_customersNum = models.IntegerField(default=0)
    use_loyal_customers_for_brand_awarenessNum = models.IntegerField(default=0)


class Financial(BaseDomain):
    net_sales = models.CharField(max_length=100, blank=True, null=True)
    net_profit_period = models.CharField(max_length=100, blank=True, null=True)
    total_assets_end_period = models.CharField(max_length=100, blank=True, null=True)
    average_assets_year = models.CharField(max_length=100, blank=True, null=True)
    equity_end_period = models.CharField(max_length=100, blank=True, null=True)
    financial_expenses = models.CharField(max_length=100, blank=True, null=True)
    sales_change_percentage = models.CharField(max_length=100, blank=True, null=True)
