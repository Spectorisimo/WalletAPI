from django.urls import path
from payments import views

urlpatterns = [
    path('users/wallets/<int:pk>/transfer/', views.WalletTransactionViewSet.as_view({'post': 'transfer'})),
    path('users/wallets/<int:pk>/deposit/', views.WalletTransactionViewSet.as_view({'post': 'deposit'})),
    path('users/wallets/<int:pk>/withdraw/', views.WalletTransactionViewSet.as_view({'post': 'withdraw'})),
    path('users/wallets/<int:pk>/transactions/', views.WalletTransactionViewSet.as_view({'get': 'get_transactions'})),
]
