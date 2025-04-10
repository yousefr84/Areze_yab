from rest_framework import serializers
from areze_yab.models import *


class CharIntegerSerializerField(serializers.Field):
    def to_representation(self, value):
        return {
            "number": value.number,
            "text": value.text,
            "raw": value.raw
        }

    def to_internal_value(self, data):
        if isinstance(data, dict):
            return f"{data.get('number', '')}{data.get('text', '')}"
        return data


class SmartModelSerializer(serializers.ModelSerializer):
    def build_standard_field(self, field_name, model_field):
        if isinstance(model_field, CharIntegerField):
            return CharIntegerSerializerField(), self.get_field_kwargs(field_name, model_field)
        return super().build_standard_field(field_name, model_field)


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

class BrandingSerializer(SmartModelSerializer):
    class Meta:
        model = Branding
        fields = '__all__'