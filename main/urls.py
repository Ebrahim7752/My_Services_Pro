from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'), 
    path('login/', views.login_view, name='login'),
     path('download/', views.download_apk, name='download_main_app'),         
    path('download/<int:app_id>/', views.download_apk, name='download_app'), 

    path('complete-profile/', views.complete_profile, name="complete_profile"),
 
   path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
   path('staff/mainapp/', views.staff_mainapp, name='staff_mainapp'),
   path('user/profile/', views.profile_view, name='profile_view'),         
path('user/downloads/', views.user_downloads, name='user_downloads'),

    path('app/<int:app_id>/', views.app_detail, name='app_detail'),
    # urls.py
path('api/download/<int:app_id>/', views.api_download_app, name='api_download_app'),
path('staff/download-stats/', views.staff_download_stats, name='staff_download_stats'),


    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/users/', views.staff_users, name='staff_users'),
    path('staff/users/create/', views.create_user, name='create_user'),
    path('staff/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('staff/apps/', views.staff_apps, name='staff_apps'),
    path('staff/apps/create/', views.create_app, name='create_app'),
    path('staff/apps/edit/<int:app_id>/', views.edit_app, name='edit_app'),

# Users
path('staff/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

# Apps
path('staff/apps/delete/<int:app_id>/', views.delete_app, name='delete_app'),


  

]














