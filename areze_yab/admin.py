from django.contrib import admin
from .models import *


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nationalID')


@admin.register(SalesAndMarketing)
class SalesAndMarketingAdmin(admin.ModelAdmin):
    list_display = ('company','date')


@admin.register(HumanResources)
class HumanResourcesAdmin(admin.ModelAdmin):
    list_display = ('company','date')


@admin.register(FinancialResources)
class FinancialResourcesAdmin(admin.ModelAdmin):
    list_display = ('company','date')


@admin.register(CapitalStructure)
class CapitalStructureAdmin(admin.ModelAdmin):
    list_display = ('company','date')


@admin.register(CustomerRelationshipManagement)
class CustomerRelationshipManagementAdmin(admin.ModelAdmin):
    list_display = ('company','date')


@admin.register(ManagementOrganizationalStructure)
class ManagementOrganizationalStructureAdmin(admin.ModelAdmin):
    list_display = ('company','date')


@admin.register(ManufacturingAndProduction)
class ManufacturingAndProductionAdmin(admin.ModelAdmin):
    list_display = ('company','date')


@admin.register(ProductCompetitiveness)
class ProductCompetitivenessAdmin(admin.ModelAdmin):
    list_display = ('company', 'date')


@admin.register(ResearchAndDevelopment)
class ResearchAndDevelopmentAdmin(admin.ModelAdmin):
    list_display = ('company', 'date')


class CompanyInline(admin.TabularInline):
    model = Company.user.through  # برای مدیریت رابطه چند‌به‌چند
    extra = 1

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'username', 'is_company')
    inlines = [CompanyInline]