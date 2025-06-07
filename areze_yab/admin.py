from django.contrib import admin
from httpx import options

from .models import *


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nationalID')




class CompanyInline(admin.TabularInline):
    model = Company.user.through  # برای مدیریت رابطه چند‌به‌چند
    extra = 1

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'username', 'is_company')
    inlines = [CompanyInline]

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('id', 'company','domain')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'questionnaire_id')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name','id', 'subdomain_id','subdomain')
@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('name','id', 'question_id')
@admin.register(SubDomain)
class SubDomainAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain_id','name')
@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Report)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')



@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'price')