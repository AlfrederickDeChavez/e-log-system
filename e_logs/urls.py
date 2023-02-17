from django.urls import path
from .views import bulletin, room_service, department_service, utilities, task


urlpatterns = [
    path('', bulletin, name='home'),
    path('bulletin/', bulletin, name='bulletin'),
    path('tasks/', task, name='task'),
    path('room-service/', room_service, name='room'),
    path('department-service/', department_service, name='department'),
    path('mis-utilities/', utilities, name='utilities')
]