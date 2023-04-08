from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .. import views

urlpatterns = [
    path('users/', views.UserViewSet.as_view({'get': 'get_user_info'})),
    path('users/create/', views.UserViewSet.as_view({'post': 'create_user'})),
    path('users/update/', views.UserViewSet.as_view({'patch': 'update_personal_info'})),
    path('users/verify/', views.UserViewSet.as_view({'post': 'verify_user'})),
    path('users/token/create/', views.UserViewSet.as_view({'post': 'create_token'})),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/password/update/', views.UserViewSet.as_view({'post': 'update_password'})),
    path('users/password/verify/', views.UserViewSet.as_view({'patch': 'verify_update_password'})),
]
