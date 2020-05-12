from rest_framework import serializers, utils

from .models import Head, Institution, Report


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'

class HeadSerializer(serializers.ModelSerializer):

    institution = serializers.CharField(read_only=True)

    class Meta:
        model = Head
        fields = ('id', 'name', 'contact', 'institution')

class ReportSerializer(serializers.ModelSerializer):

    institution = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Report
        fields = ('id', 'name', 'description', 'report',
                  'created_at', 'updated_at', 'institution',)
