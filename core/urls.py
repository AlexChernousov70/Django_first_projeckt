# core/urls.py
from django.urls import path
from .views import thanks, orders_list, order_detail, service_list, service_create

# Эти маршруты будут доступны с префиксом /barbershop/
urlpatterns = [
    path('thanks/', thanks, name='thanks'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('services/', service_list, name='service_list'),
    path('services/create/', service_create, name='service_create'),
]
