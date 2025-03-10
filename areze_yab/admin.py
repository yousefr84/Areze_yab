from django.contrib import admin
from .models import *

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass
@admin.register(SalesAndMarketing)
class SalesAndMarketingAdmin(admin.ModelAdmin):
    pass
@admin.register(HumanResources)
class HumanResourcesAdmin(admin.ModelAdmin):
    pass

@admin.register(FinancialResources)
class FinancialResourcesAdmin(admin.ModelAdmin):
    pass

@admin.register(CapitalStructure)
class CapitalStructureAdmin(admin.ModelAdmin):
    pass
@admin.register(CustomerRelationshipManagement)
class CustomerRelationshipManagementAdmin(admin.ModelAdmin):
    pass
@admin.register(ManagementOrganizationalStructure)
class ManagementOrganizationalStructureAdmin(admin.ModelAdmin):
    pass
@admin.register(ManufacturingAndProduction)
class ManufacturingAndProductionAdmin(admin.ModelAdmin):
    pass
@admin.register(ProductCompetitiveness)
class ProductCompetitivenessAdmin(admin.ModelAdmin):
    pass
@admin.register(ResearchAndDevelopment)
class ResearchAndDevelopmentAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class ModelNameAdmin(admin.ModelAdmin):
    pass