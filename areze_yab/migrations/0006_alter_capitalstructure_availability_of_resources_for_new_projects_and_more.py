# Generated by Django 5.1.6 on 2025-03-09 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('areze_yab', '0005_rename_quality_control_standards_manufacturingandproduction_z_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capitalstructure',
            name='availability_of_resources_for_new_projects',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='capitalstructure',
            name='shareholder_funding_power',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='capitalstructure',
            name='startup_investment_risk_tolerance',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customerrelationshipmanagement',
            name='customer_feedback_analysis',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customerrelationshipmanagement',
            name='customer_feedback_system',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customerrelationshipmanagement',
            name='employee_training_for_customer_interaction',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customerrelationshipmanagement',
            name='first_purchase_support_plan',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customerrelationshipmanagement',
            name='loyal_customer_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customerrelationshipmanagement',
            name='loyal_customer_payment_benefits',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customerrelationshipmanagement',
            name='purchase_info_documentation',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customerrelationshipmanagement',
            name='special_sales_plan_for_loyal_customers',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialresources',
            name='ability_to_maintain_positive_cash_flow',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialresources',
            name='ability_to_pay_accounts_payable',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialresources',
            name='ability_to_pay_financial_obligations',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialresources',
            name='assets_for_short_term_financial_obligations',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialresources',
            name='budget_vs_actual_difference',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialresources',
            name='financial_activity_cost_to_income_ratio',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialresources',
            name='financial_report_accuracy_and_completeness',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialresources',
            name='payment_processing_costs',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialresources',
            name='profitability_efficiency_comparison',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialresources',
            name='sales_change_over_period',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialresources',
            name='weekly_monthly_annual_expenses',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='annual_salary_increase_adjusted_for_inflation',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='available_workforce_for_new_projects',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='backlog_of_daily_tasks',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='daily_operations_with_current_workforce',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='employee_interest_in_group_work',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='employee_requests_for_early_retirement',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='employee_requests_for_new_jobs',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='employee_responsibility_and_commitment',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='employee_satisfaction_percentage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='employee_satisfaction_with_management',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='employees_with_minimum_5_years_experience',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='evaluation_criteria_alignment_with_job_description',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='in_house_training_programs',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='management_satisfaction_with_employees',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='manager_employee_interaction',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='manager_focus_on_team_processes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='managers_behavior_towards_men_and_women',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='organizational_support_for_employees',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='performance_evaluation_system_scheduling',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='practical_model_for_employee_ranking',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='respect_for_employee_privacy',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='revenue_per_employee',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='shared_workspaces_availability',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='support_for_attending_training_programs',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='up_to_date_technology_in_performance_evaluation',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='humanresources',
            name='weekly_fixed_meetings',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='managementorganizationalstructure',
            name='activities_for_increasing_customer_awareness',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='managementorganizationalstructure',
            name='comprehensive_organizational_chart',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='managementorganizationalstructure',
            name='decision_making_power_for_lower_employees',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='managementorganizationalstructure',
            name='employee_awareness_of_long_short_term_plans',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='managementorganizationalstructure',
            name='five_s_in_daily_operations',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='managementorganizationalstructure',
            name='information_system_for_knowledge_management',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='managementorganizationalstructure',
            name='knowledge_management_system_integration',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='managementorganizationalstructure',
            name='regular_chart_updates',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='managementorganizationalstructure',
            name='vision_and_mission_definition',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='managementorganizationalstructure',
            name='workspace_design',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='defect_detection_and_resolution',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='iot_equipment_in_production_line',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='max_capacity_utilization',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='output_input_ratio',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='production_increase_planning',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='production_process_documentation',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='production_process_flexibility',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='production_sales_marketing_alignment',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='production_stability',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='production_technology_level',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='production_waste_ppm',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='quality_control_lab',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='required_certifications',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='safety_stock_level',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='storage_cost',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='warranty_after_sales',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='warranty_commitment',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturingandproduction',
            name='z',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productcompetitiveness',
            name='unique_feature',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='researchanddevelopment',
            name='customer_competitor_inspiration',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='researchanddevelopment',
            name='innovation_culture',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='researchanddevelopment',
            name='innovation_planning',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='researchanddevelopment',
            name='innovation_process_guidelines',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='researchanddevelopment',
            name='r_and_d_budget',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='researchanddevelopment',
            name='r_and_d_production_connection',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='researchanddevelopment',
            name='r_and_d_unit_defined_roles',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='brandIdentity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='brandReputationManagement',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='brandTrustAndEmotionalConnection',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='competitorAwareness',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='digitalMarketingUsage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='exhibitionParticipation',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='exportActivitiesAndGlobalMarketUse',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='innovativeMarketingUsage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='marketLeadershipPotential',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='marketRegulationsKnowledge',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='marketResearchForMarketing',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='marketResearchOpportunities',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='marketingAndSalesNetworking',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='marketingPlanningAndGuidelines',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='orderDeliveryTimeliness',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='reliableTransportUsage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='salesAgencySupervision',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='salesAmountToCostRatio',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='salesGrowthLast3Months',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='salesNetworkCoverage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='salesRepProductAwareness',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='salesToIndustryRatio',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='salesToProductionRatio',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='targetMarketDefinition',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salesandmarketing',
            name='visualIdentityActivities',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
