import re
import operator

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from rest_framework import serializers

from raspberry_awards.models import Nomination


class Interval:

    def __init__(self, producer, previousWin, followingWin):
        self.producer = producer
        self.previousWin = previousWin
        self.followingWin = followingWin
        self.interval = followingWin - previousWin

    def __str__(self):
        return str([self.producer, self.previousWin, self.followingWin, self.interval])

class IntervalSerializer(serializers.Serializer):
    producer = serializers.CharField(max_length=200)
    interval = serializers.IntegerField()
    previousWin = serializers.IntegerField()
    followingWin = serializers.IntegerField()

class IntervalsResponseSerializer(serializers.Serializer):
    min = IntervalSerializer(many=True)
    max = IntervalSerializer(many=True)

def intervals(request):
    winners = Nomination.objects.filter(winner=True)
    multiple_winners = [p for sublist in winners.values('producers').annotate(total=Count('producers'))
        .filter(total__gt=1).values_list('producers') for p in sublist]
    multiple_winners_dict = {}

    for w in winners.values_list('producers', 'year').filter(producers__in=multiple_winners):
        try:
            multiple_winners_dict[w[0]] += [w[1]]
        except KeyError:
            multiple_winners_dict[w[0]] = [w[1]]

    for y in multiple_winners_dict.values(): y.sort()

    intervals = []
    for w in multiple_winners_dict.items():
        for i in range(len(w[1])-1):
            intervals.append(Interval(producer=w[0], previousWin=w[1][i], followingWin=w[1][i+1]))
    intervals.sort(key=operator.attrgetter('interval'))
    min_interval_value = intervals[0].interval
    max_interval_value = intervals[-1].interval
    min_intervals = filter(lambda interval: interval.interval == min_interval_value, intervals)
    max_intervals = filter(lambda interval: interval.interval == max_interval_value, intervals)
    r = IntervalsResponseSerializer(data={'min': IntervalSerializer(min_intervals, many=True).data,
                                          'max': IntervalSerializer(max_intervals, many=True).data})
    r.is_valid();
    return JsonResponse(r.data)
