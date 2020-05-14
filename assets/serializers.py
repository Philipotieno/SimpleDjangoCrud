from rest_framework import serializers, utils

from .models import Head, Institution, Report


class InstitutionSerializer(serializers.ModelSerializer):

    principle = serializers.SerializerMethodField(read_only=True)

    def get_principle(self, instance):
        return instance.id
    class Meta:
        model = Institution
        fields = ('id', 'name', 'population', 'principle')

class HeadSerializer(serializers.ModelSerializer):

    institution = InstitutionSerializer(read_only=True)
    principle = serializers.CharField(read_only=True)

    class Meta:
        model = Head
        fields = ('id', 'principle', 'contact', 'institution')

class ReportSerializer(serializers.ModelSerializer):

    institution = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Report
        fields = ('id', 'name', 'description', 'report',
                  'created_at', 'updated_at', 'institution',)
