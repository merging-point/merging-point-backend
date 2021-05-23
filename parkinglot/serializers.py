from rest_framework import serializers
from .models import Parkinglot


class MarkParkinglotSerailizer(serializers.Serializer):
    parked_at = serializers.IntegerField()


class ParkinglotSerializer(serializers.ModelSerializer):
    spots_for_disabled_cnt = serializers.IntegerField(read_only=True)
    avg_bigger_percentage = serializers.ReadOnlyField(read_only=True)
    estimated_time = serializers.IntegerField(read_only=True)
    parked_cnt = serializers.IntegerField(read_only=True)

    class Meta:
        model = Parkinglot
        fields = '__all__'