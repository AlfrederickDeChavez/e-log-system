from django.urls import path
from .views import *

urlpatterns = [
    path('', bulletin, name='home'),
    path('bulletin/', bulletin, name='bulletin'),
    path('tasks/', task, name='task'),
    path('room-service/', room_service, name='room'),
    path('department-service/', department_service, name='department'),
    path('mis-utilities/', utilities, name='utilities'),
    path('assets/',assets, name="assets"),
    path('assets/<str:pk>/', asset_details, name="asset_details"),
    path('create-asset/', create_asset, name="create-asset"),
    path('update-asset/<str:pk>', update_asset, name="update-asset"),
    path('delete-asset/<str:pk>', delete_asset, name="delete-asset"),
    path('login/', login_view, name="login"),
    path('404-record-not-found/', not_found, name='not_found')
]