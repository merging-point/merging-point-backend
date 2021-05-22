from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from user.views import UserView
from parkinglot.views import ParkinglotViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, basename="user")
router.register(r'parkinglot', ParkinglotViewSet, basename="parkinglot")

urlpatterns = [
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('token/verify', TokenVerifyView.as_view()),
]

urlpatterns += router.urls