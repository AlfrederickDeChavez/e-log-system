from django.urls import path
from .views import bulletin, room_service, department_service, utilities, task, not_found, assets, asset_details


urlpatterns = [
    path('', bulletin, name='home'),
    path('bulletin/', bulletin, name='bulletin'),
    path('tasks/', task, name='task'),
    path('room-service/', room_service, name='room'),
    path('department-service/', department_service, name='department'),
    path('mis-utilities/', utilities, name='utilities'),
    path('assets/',assets, name="assets"),
    path('assets/<str:pk>/', asset_details, name="asset_details"),
    path('404-record-not-found/', not_found, name='not_found')
]