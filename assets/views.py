from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Head, Institution, Report
from .serializers import (HeadSerializer, InstitutionSerializer,
                          ReportSerializer)


class ListCreateInstitutions(generics.ListCreateAPIView):
    serializer_class = InstitutionSerializer

    def post(self, request):

        data = request.data
        serializer = self.serializer_class(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Institution added'
        }, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Get a list of all instutution
        """
        institution = Institution.objects.all().order_by('name')
        serializer = self.serializer_class(
            institution,
            many=True
        )
        response = ({
            "institution": serializer.data
        })
        return Response(response)


class ListCreateHead(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = HeadSerializer

    def post(self, request, id, *args, **kwargs):

        # try:
        data = request.data
        id = self.kwargs.get('id')
        institution = Institution.objects.get(id=id)

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(institution=institution)

        return Response({
            'message': 'institution added'
            }, status=status.HTTP_201_CREATED)
        # except Exception:
        #     return Response({
        #         'message': 'institution does not exist'
        #     }, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        """
        Get a list of all heads
        """
        heads = Head.objects.all().order_by('name')
        # print("------------------------------------", commanders)
        serializer = self.serializer_class(
            heads,
            many=True
        )
        response = ({
            "heads": serializer.data
        })
        return Response(response)


class ListCreateReport(generics.ListCreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = ReportSerializer

    def post(self, request, *args, **kwargs):

        data = request.data

        # content_data = request.data.get('camp',None)

        id = self.kwargs.get('id')
        camp = Camp.objects.get(id=id)

        # content_data['camp'] = instance.id

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(camp=camp)

        return Response({
            'message': 'report added successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Get a list of all reports
        """
        reports = Report.objects.all().order_by('name')
        serializer = self.serializer_class(
            reports,
            many=True
        )
        response = ({
            "repo": serializer.data
        })
        return Response(response)
