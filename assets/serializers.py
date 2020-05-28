from rest_framework import serializers, utils

from .models import Head, Institution, Report


class GetHeadSerializer(serializers.ModelSerializer):

    # institution = InstitutionSerializer(read_only=True)
    principal = serializers.CharField(read_only=True)

    class Meta:
        model = Head
        fields = ('id', 'principal', 'contact')


class GetReportSerializer(serializers.ModelSerializer):

    report_name = serializers.CharField(read_only=True)
    class Meta:
        model = Report
        exclude = ('institution',)
class InstitutionSerializer(serializers.ModelSerializer):

    # principal = serializers.SerializerMethodField(read_only=True)
    head = serializers.SerializerMethodField(read_only=True)
    reports = serializers.SerializerMethodField(read_only=True)

    def get_head(self, obj):
        heads = Head.objects.filter(institution=obj.id)
        serializer = GetHeadSerializer(heads, many=True)

        return serializer.data

    def get_reports(self, obj):
        reports = Report.objects.filter(institution=obj.id)
        serializer = GetReportSerializer(reports, many=True)

        return serializer.data
    class Meta:
        model = Institution
        fields = ('id', 'name', 'population', 'head', 'reports')

class GetInstitutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = ('id', 'name', 'population')

class HeadSerializer(serializers.ModelSerializer):

    institution = GetInstitutionSerializer(read_only=True)
    # principal = serializers.CharField(read_only=True)

    class Meta:
        model = Head
        # exclude = ('heads',)
        fields = ('id', 'principal', 'contact', 'institution')

class ReportSerializer(serializers.ModelSerializer):

    institution = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Report
        fields = ('id', 'report_name', 'description', 'report',
                  'created_at', 'updated_at', 'institution',)
