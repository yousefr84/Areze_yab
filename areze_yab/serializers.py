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


class SalesAndMarketingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesAndMarketing
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class HumanResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanResources
        fields = '__all__'


# <------------Financial Resources Serializer------------>
class FinancialResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialResources
        fields = '__all__'


# <------------Capital Structure Serializer------------>
class CapitalStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapitalStructure
        fields = '__all__'


# <------------Management & Organizational Structure Serializer------------>
class ManagementOrganizationalStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementOrganizationalStructure
        fields = '__all__'


# <------------Customer Relationship Management Serializer------------>
class CustomerRelationshipManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRelationshipManagement
        fields = '__all__'


# <------------Research & Development Serializer------------>
class ResearchAndDevelopmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchAndDevelopment
        fields = '__all__'


# <------------Product Competitiveness Serializer------------>
class ProductCompetitivenessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCompetitiveness
        fields = '__all__'


class ManufacturingAndProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturingAndProduction
        fields = '__all__'
