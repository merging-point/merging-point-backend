import math
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Parkinglot
from .serializers import ParkinglotSerializer


class Point:
    latitude: float
    longtitude: float

    def __init__(self, latitude: float, longtitude: float):
        self.latitude = latitude
        self.longtitude = longtitude


class ParkinglotViewSet(viewsets.ViewSet):
    closest_param = [
        openapi.Parameter(
            'center_latitude',
            openapi.IN_QUERY,
            description="center latitude",
            type=openapi.TYPE_NUMBER,
        ),
        openapi.Parameter(
            'center_longtitude',
            openapi.IN_QUERY,
            description="center longtitude",
            type=openapi.TYPE_NUMBER,
        ),
        openapi.Parameter(
            'north_east_latitude',
            openapi.IN_QUERY,
            description="north_east_latitude",
            type=openapi.TYPE_NUMBER,
        ),
        openapi.Parameter(
            'north_east_longtitude',
            openapi.IN_QUERY,
            description="north east longtitude",
            type=openapi.TYPE_NUMBER,
        ),
        openapi.Parameter(
            'south_west_latitude',
            openapi.IN_QUERY,
            description="south west latitude",
            type=openapi.TYPE_NUMBER,
        ),
        openapi.Parameter(
            'south_west_longtitude',
            openapi.IN_QUERY,
            description="south west longtitude",
            type=openapi.TYPE_NUMBER,
        ),
    ]

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(manual_parameters=closest_param,
                         responses={200: ParkinglotSerializer})
    def closest(self, request):
        # south west lat lng, north east lat lng
        center_point = Point(
            request.GET.get('center_latitude'),
            request.GET.get('center_longtitude'),
        )
        south_west_point = Point(
            request.GET.get('south_west_latitude'),
            request.GET.get('south_west_longtitude'),
        )
        north_east_point = Point(
            request.GET.get('north_east_latitude'),
            request.GET.get('north_east_longtitude'),
        )

        temp = Parkinglot.objects.filter(
            parking_compartments_cnt__gte=50).only('parking_compartments_cnt')

        total = 0
        for t in temp:
            total += t.parking_compartments_cnt * 0.04

        avg = total / len(temp)

        found_parking_lots = Parkinglot.objects.filter(
            latitude__lte=north_east_point.latitude,
            latitude__gte=south_west_point.latitude,
            longtitude__lte=north_east_point.longtitude,
            longtitude__gte=south_west_point.longtitude,
        )

        serializer = ParkinglotSerializer(many=True, data=found_parking_lots)
        serializer.is_valid()

        response_data = []

        for data in serializer.data:
            spots_for_disabled_cnt = data['parking_compartments_cnt'] * 0.04
            data['avg_bigger_percentage'] = round(
                (spots_for_disabled_cnt - avg) / avg *
                100)  # rounded percentage
            response_data.append(data)

        def calc_diagonal_distance(target_latitude, target_longtitude,
                                   center_latitude, center_longtitude):
            width = abs(float(target_latitude) - float(center_latitude))
            height = abs(float(target_longtitude) - float(center_longtitude))

            return (math.sqrt(width**2 + height**2))

        response_data.sort(key=lambda x: (calc_diagonal_distance(
            x['latitude'], x['longtitude'], center_point.latitude, center_point
            .longtitude)))  # sort by short distance

        return Response(response_data)