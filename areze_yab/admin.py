from django.contrib import admin
from .models import *


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nationalID')


@admin.register(SalesAndMarketingS)
class SalesAndMarketingAdmin(admin.ModelAdmin):
    list_display = ('company','date')


@admin.register(HumanResourcesS)
class HumanResourcesAdmin(admin.ModelAdmin):
    list_display = ('company','date')





class CompanyInline(admin.TabularInline):
    model = Company.user.through  # برای مدیریت رابطه چند‌به‌چند
    extra = 1

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'username', 'is_company')
    inlines = [CompanyInline]


