import re
import operator

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from raspberry_awards.models import Nomination
from raspberry_awards.service import NominationService
from raspberry_awards.serializers import IntervalSerializer
from raspberry_awards.serializers import IntervalsResponseSerializer
from raspberry_awards.interval import Interval

class Intervals(APIView):
    def get(self, request):    
        min_intervals = NominationService.get_min_win_interval()
        max_intervals = NominationService.get_max_win_interval()
        r = IntervalsResponseSerializer(data={'min': IntervalSerializer(min_intervals, many=True).data,
                                              'max': IntervalSerializer(max_intervals, many=True).data})
        r.is_valid();
        return Response(r.validated_data)
