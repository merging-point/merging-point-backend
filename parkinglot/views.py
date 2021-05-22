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
    @swagger_auto_schema(manual_parameters=closest_param)
    def closest(self, request):
        # south west lat lng, north east lat lng
        south_west_point = Point(
            request.GET.get('south_west_latitude'),
            request.GET.get('south_west_longtitude'),
        )
        north_east_point = Point(
            request.GET.get('north_east_latitude'),
            request.GET.get('north_east_longtitude'),
        )

        found_parking_lots = Parkinglot.objects.filter(
            latitude__lte=north_east_point.latitude,
            latitude__gte=south_west_point.latitude,
            longtitude__lte=north_east_point.longtitude,
            longtitude__gte=south_west_point.longtitude,
        )
        serializer = ParkinglotSerializer(many=True, data=found_parking_lots)
        serializer.is_valid()
        return Response(serializer.data)