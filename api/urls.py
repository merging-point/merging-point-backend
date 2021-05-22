from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from parkinglot.views import ParkinglotViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'parkinglot', ParkinglotViewSet, basename="parkinglot")

urlpatterns = []

urlpatterns += router.urls