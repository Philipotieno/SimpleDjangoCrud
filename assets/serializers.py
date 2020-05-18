from rest_framework import serializers, utils

from .models import Head, Institution, Report


class GetHeadSerializer(serializers.ModelSerializer):

    # institution = InstitutionSerializer(read_only=True)
    principal = serializers.CharField(read_only=True)

    class Meta:
        model = Head
        fields = ('id', 'principal', 'contact')


class InstitutionSerializer(serializers.ModelSerializer):

    # principal = serializers.SerializerMethodField(read_only=True)
    heads = serializers.SerializerMethodField(read_only=True)

    def get_heads(self, obj):
        heads = Head.objects.filter(institution=obj.id)
        serializer = GetHeadSerializer(heads, many=True)

        return serializer.data
    # def get_principal(self, instance):
    #     return instance.id
    class Meta:
        model = Institution
        fields = ('id', 'name', 'population', 'heads')

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
        fields = ('id', 'name', 'description', 'report',
                  'created_at', 'updated_at', 'institution',)
