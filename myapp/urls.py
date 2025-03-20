from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
   # path('admin/dashboard', views.admin_dashboard, name='admin_dashboard'),
]