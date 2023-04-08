from wallets import views
from django.urls import path
from wallets import views

urlpatterns = [
    path('users/wallets/', views.WalletViewSet.as_view({'get': 'list'})),
    path('users/wallets/create/', views.WalletViewSet.as_view({'post': 'create'})),
    path('users/wallets/<int:pk>/', views.WalletViewSet.as_view({'get': 'retrieve'})),
    path('users/wallets/<int:pk>/update/', views.WalletViewSet.as_view({'patch': 'partial_update'})),
]
