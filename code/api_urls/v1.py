from django.urls import path, include

urlpatterns = [
    path('', include('users.urls.v1')),
    path('', include('wallets.urls.v1')),
    path('', include('payments.urls.v1')),
]
