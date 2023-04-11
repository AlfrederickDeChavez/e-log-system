from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views 


urlpatterns = [
    path('', bulletin, name='home'),
    path('bulletin/', bulletin, name='bulletin'),
    path('tasks/', task, name='task'),
    path('bhtl-tasks/', bhtl_task, name='bhtl-tasks'),
    path('room-service/', room_service, name='room'),
    path('department-service/', department_service, name='department'),
    path('mis-utilities/', utilities, name='utilities'),
    path('assets/',assets, name="assets"),
    path('assets/<str:pk>/', asset_details, name="asset-details"),
    path('create-asset/', create_asset, name="create-asset"),
    path('update-asset/<str:pk>', update_asset, name="update-asset"),
    path('delete-asset/<str:pk>', delete_asset, name="delete-asset"),
    path('save-as-pdf/<str:pk>', print_asset, name='print-asset'),
    path('accounts/login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('404-record-not-found/', not_found, name='not_found'),
    path('audit-logs/', audit_logs, name="audit-logs"),
    path('versions/<int:pk>', versions, name='versions'),
    path("password-reset/", password_reset_request, name="password_reset")
    # path("accounts/password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset")
]