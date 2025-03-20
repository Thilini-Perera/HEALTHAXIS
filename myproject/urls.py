"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from django.urls import path
from myapp.views import base_design, check_availability, login_view, search_items,signup,dashboard ,udashboard, add_item, item_list
from myapp.views import registration_request_view
from myapp.views import sales_prediction_view
from myapp.views import register_user
from myapp.views import users
from myapp.views import processed_orders
from myapp.views import reg_request
from myapp.views import shipped_orders
from myapp.views import Rship_orders
from myapp.views import delivered_orders
from myapp.views import cd_orders
from myapp.views import update_stocks
from myapp.views import delete_user
from myapp.views import logout_view
from myapp.views import index
from myapp.views import user_pendingorders
from myapp.views import user_processedorders
from myapp.views import user_shippedorders
from myapp.views import user_deliveredorders
from myapp.views import user_cancelledorders
from myapp.views import create_order
from myapp.views import place_order
from myapp.views import cancel_order
from myapp.views import admin_update_orderstatus_process
from myapp.views import admin_update_orderstatus_ready
from myapp.views import admin_update_orderstatus_shipped
from myapp.views import admin_update_orderstatus_delivered
from myapp.views import admin_update_price
from myapp.views import generate_monthly_sales_report
from myapp.views import welcome


   
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('welcome/', welcome, name='welcome'),
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('admin_dashboard/', dashboard, name='dashboard'),
    path('user_dashboard/', udashboard, name='udashboard'),
    path('add_item/', add_item, name='add_item'),
    path('item_list/', item_list, name='item_list'),   
    path('registration_request/',registration_request_view, name='registration_request'),
    path('sales_prediction/', sales_prediction_view, name='sales_prediction'),
    path('register_user/<int:request_id>/', register_user, name='register_user'),
    path('users/', users, name='users'),
    path('delete_user/<int:uid>/',delete_user, name='delete_user'),
    path('processed_orders/',processed_orders, name='processed_orders'),
    path('reg_request/',reg_request, name='reg_request'),  
    path('shipped_orders/',shipped_orders, name='shipped_orders'),
    path('Rship_orders/',Rship_orders, name='Rship_orders'),
    path('delivered_orders/',delivered_orders, name='delivered_orders'), 
    path('cd_orders/',cd_orders, name='cd_orders'),           
    path('update_stocks/', update_stocks, name='update_stocks'),  
    path('logout/', logout_view, name='logout'),
    path('index/', index, name='index'),
    path('user_pendingorders/', user_pendingorders, name='user_pendingorders'),
    path('user_processedorders/', user_processedorders, name='user_processedorders'),
    path('user_shippedorders/', user_shippedorders, name='user_shippedorders'),
    path('user_deliveredorders/', user_deliveredorders, name='user_deliveredorders'),
    path('user_cancelledorders/', user_cancelledorders, name='user_cancelledorders'),
    path('create_order/', create_order, name='create_order'),
    path('place_order/', place_order, name='place_order'),
    path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order'),
    path('admin_update_orderstatus_process/<int:order_id>/', admin_update_orderstatus_process, name='admin_update_orderstatus_process'),
    path('admin_update_orderstatus_ready/<int:order_id>/', admin_update_orderstatus_ready, name='admin_update_orderstatus_ready'),
    path('admin_update_orderstatus_shipped/<int:order_id>/', admin_update_orderstatus_shipped, name='admin_update_orderstatus_shipped'),
    path('admin_update_orderstatus_delivered/<int:order_id>/', admin_update_orderstatus_delivered, name='admin_update_orderstatus_delivered'),
    path('admin_update_price', admin_update_price, name='admin_update_price'),
    path('generate_monthly_sales_report/', generate_monthly_sales_report, name='generate_monthly_sales_report'),
    path('search-items/',search_items, name='search_items'),
    path("check-availability/", check_availability, name="check_availability"),
    path("base-design/", base_design, name="base_design")
]





