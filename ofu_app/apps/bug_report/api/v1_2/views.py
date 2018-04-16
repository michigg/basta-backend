# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from apps.bug_report.api.v1_2.serializers import BugMsgSerializer, BugMsgCategoriesSerializer, \
    BugMsgPrioritiesSerializer, BugMsgStatesSerializer, BugMsgDetailSerializer
from apps.bug_report.models import BugMsg
from rest_framework import generics, views, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@permission_classes((AllowAny,))
class ApiBugMsgs(generics.ListCreateAPIView):
    serializer_class = BugMsgSerializer
    queryset = BugMsg.objects.order_by('-registration_date')


@permission_classes((AllowAny,))
class ApiBugMsgUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = BugMsgDetailSerializer
    queryset = BugMsg.objects.all()


@permission_classes((AllowAny,))
class ApiBugPriorities(views.APIView):

    def get(self, request):
        data = BugMsg.API_Priorities
        results = BugMsgPrioritiesSerializer(data, many=True).data
        return Response(results, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class ApiBugCategories(views.APIView):

    def get(self, request):
        data = BugMsg.API_CATEGORIES
        results = BugMsgCategoriesSerializer(data, many=True).data
        return Response(results, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class ApiBugStates(views.APIView):

    def get(self, request):
        data = BugMsg.API_STATES
        results = BugMsgStatesSerializer(data, many=True).data
        return Response(results, status=status.HTTP_200_OK)
