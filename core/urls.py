# core/urls.py
from django.urls import path
from .views import thanks, orders_list, order_detail, service_list, service_create, create_review, thanks_for_the_review, order_create, get_master_info, masters_services_by_id

# Эти маршруты будут доступны с префиксом /barbershop/
urlpatterns = [
    path('thanks/', thanks, name='thanks'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('services/', service_list, name='service_list'),
    path('services/create/', service_create, name='service_create'),
    path('review/create/', create_review, name='create_review'),
    path('thanks/review/', thanks_for_the_review, name='thanks_for_the_review'),
    path("masters_services/", masters_services_by_id, name="masters_services_by_id_ajax"),
    path("order_create/", order_create, name="order_create"),
    path("api/master-info/", get_master_info, name="get_master_info"),
]
