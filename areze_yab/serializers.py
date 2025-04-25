from rest_framework import serializers
from areze_yab.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_company=validated_data.get('is_company', False),
            name=validated_data.get('name'),
            registrationNumber=validated_data.get('registrationNumber')
        )
        return user


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class SalesAndMarketingSSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = SalesAndMarketingS
        fields = '__all__'


class SalesAndMarketingMSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = SalesAndMarketingM
        fields = '__all__'


class SalesAndMarketingLSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = SalesAndMarketingL
        fields = '__all__'


class HumanResourcesSSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = HumanResourcesS
        fields = '__all__'


class HumanResourcesMSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = HumanResourcesM
        fields = '__all__'


class HumanResourcesLSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = HumanResourcesL
        fields = '__all__'


# <------------Financial Resources Serializer------------>
class FinancialResourcesSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = FinancialResources
        fields = '__all__'


# <------------Capital Structure Serializer------------>
class CapitalStructureSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = CapitalStructure
        fields = '__all__'


# <------------Management & Organizational Structure Serializer------------>
class ManagementOrganizationalStructureSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = ManagementOrganizationalStructure
        fields = '__all__'


# <------------Customer Relationship Management Serializer------------>
class CustomerRelationshipManagementSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = CustomerRelationshipManagement
        fields = '__all__'


# <------------Research & Development Serializer------------>
class ResearchAndDevelopmentSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = ResearchAndDevelopment
        fields = '__all__'


# <------------Product Competitiveness Serializer------------>
class ProductCompetitivenessSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = ProductCompetitiveness
        fields = '__all__'


class ManufacturingAndProductionSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = ManufacturingAndProduction
        fields = '__all__'


class BrandingSSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = BrandingS
        fields = '__all__'


class BrandingMSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = BrandingM
        fields = '__all__'


class BrandingLSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = BrandingL
        fields = '__all__'
