# core/urls.py
from django.urls import path
from .views import thanks, orders_list, order_detail, service_list, service_create, create_review, thanks_for_the_review, create_order, get_master_info

# Эти маршруты будут доступны с префиксом /barbershop/
urlpatterns = [
    path('thanks/', thanks, name='thanks'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('services/', service_list, name='service_list'),
    path('services/create/', service_create, name='service_create'),
    path('review/create/', create_review, name='create_review'),
    path('thanks/review/', thanks_for_the_review, name='thanks_for_the_review'),
    path('order/create/', create_order, name='create_order'),
    path('api/master-info/', get_master_info, name='get_master_info'),
]
