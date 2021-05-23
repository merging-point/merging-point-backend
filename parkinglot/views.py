import json
import math
import requests
import threading
from django.db.models import Count
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from user.models import User
from .models import Parkinglot
from .serializers import ParkinglotSerializer, MarkParkinglotSerailizer


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

    idx_param = [
        openapi.Parameter(
            'idx',
            openapi.IN_QUERY,
            description="The idx of the parkinglot",
            type=openapi.TYPE_NUMBER,
        ),
    ]

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated],
    )
    @swagger_auto_schema(
        manual_parameters=idx_param,
        responses={200: MarkParkinglotSerailizer},
    )
    def mark_use(self, request):
        idx = request.GET.get('idx')
        request.user.parked_at = idx
        request.user.save()
        return Response({"parked_at": request.user.parked_at})

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated],
    )
    @swagger_auto_schema(responses={200: MarkParkinglotSerailizer})
    def mark_moved(self, request):
        request.user.parked_at = -1
        request.user.save()
        return Response({"parked_at": request.user.parked_at})

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(
        manual_parameters=closest_param,
        responses={200: ParkinglotSerializer},
    )
    def closest(self, request):
        # south west lat lng, north east lat lng
        required_parameters = [
            'center_latitude', 'center_longtitude', 'south_west_latitude',
            'south_west_longtitude', 'north_east_latitude',
            'north_east_longtitude'
        ]

        # validate get parameters
        for required_parameter in required_parameters:
            if required_parameter not in request.GET:
                return Response(
                    data={
                        'error':
                        'following fields are missing: ' +
                        ', '.join(required_parameters)
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # three points
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

        # get average
        temp = Parkinglot.objects.filter(
            parking_compartments_cnt__gte=50).only('parking_compartments_cnt')
        total = 0
        for t in temp:
            total += t.parking_compartments_cnt * 0.04
        avg = total / len(temp)

        # get near parking lots
        found_parking_lots = Parkinglot.objects.filter(
            latitude__lte=north_east_point.latitude,
            latitude__gte=south_west_point.latitude,
            longtitude__lte=north_east_point.longtitude,
            longtitude__gte=south_west_point.longtitude,
        )
        serializer = ParkinglotSerializer(many=True, data=found_parking_lots)
        serializer.is_valid()

        parked_info = {}

        for x in User.objects.all().values('parked_at').annotate(
                parked_cnt=Count("parked_at")).order_by('parked_at'):
            parked_info[x['parked_at']] = x['parked_cnt']

        # add the average bigger percentage
        response_data = []
        for data in serializer.data:
            spots_for_disabled_cnt = data['parking_compartments_cnt'] * 0.04
            data['avg_bigger_percentage'] = round(
                (spots_for_disabled_cnt - avg) / avg *
                100)  # rounded percentage
            data['parked_cnt'] = parked_info.get(data['idx'], 0)
            response_data.append(data)
        # SELECT parked_at, COUNT(*) FROM user GROUP BY parked_at

        # sort by short distance
        def calc_diagonal_distance(target_latitude, target_longtitude,
                                   center_latitude, center_longtitude):
            width = abs(float(target_latitude) - float(center_latitude))
            height = abs(float(target_longtitude) - float(center_longtitude))

            return (math.sqrt(width**2 + height**2))

        response_data.sort(key=lambda x: (calc_diagonal_distance(
            x['latitude'], x['longtitude'], center_point.latitude, center_point
            .longtitude), ), )  # sort by short distance

        # add estimated time for the top 10 parking lots
        closest_top10 = response_data[:10]

        def get_arrival_duration(start, goal) -> int:
            headers = {
                'X-NCP-APIGW-API-KEY-ID': 'jygh7x1jrq',
                'X-NCP-APIGW-API-KEY':
                'cTOEcsLwF32zsLPa7imyo44sGwFACyImh6i3Z32a'
            }
            response = requests.get(
                f"https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving?start={start}&goal={goal}&option=traoptimal",
                headers=headers,
            ).text
            response_json = json.loads(response)
            status_code = response_json['code']

            if status_code != 0:
                return -1

            traoptimals = response_json['route']['traoptimal']
            min_durations = traoptimals[0]['summary']['duration']
            for traoptimal in traoptimals[1:]:
                cursor = traoptimal['summary']['duration']
                if min_durations > cursor:
                    min_durations = cursor
            return min_durations

        # get arrival time using thread
        def arrival_duration_thread(id: int):
            closest_top10[i]['estimated_time'] = get_arrival_duration(
                f"{closest_top10[i]['longtitude']},{closest_top10[i]['latitude']}",
                f"{center_point.longtitude},{center_point.latitude}",
            )

        threads = [None] * 10
        for i in range(len(closest_top10)):
            threads[i] = threading.Thread(
                target=arrival_duration_thread,
                args=(i, ),
            )

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        return Response(closest_top10 + response_data[10:])
