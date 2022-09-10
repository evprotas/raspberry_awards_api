from rest_framework import serializers
from raspberry_awards.interval import Interval


class IntervalSerializer(serializers.Serializer):
    producer = serializers.CharField(max_length=200)
    interval = serializers.IntegerField()
    previousWin = serializers.IntegerField()
    followingWin = serializers.IntegerField()

    def create(self, validated_data):
        return Interval(**validated_data)

    class Meta:
        model = Interval
        fields = ['producer', 'previousWin', 'followingWin']
        read_only_fields = ['interval']

class IntervalsResponseSerializer(serializers.Serializer):
    min = IntervalSerializer(many=True)
    max = IntervalSerializer(many=True)