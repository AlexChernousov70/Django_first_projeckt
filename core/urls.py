# core/urls.py
from django.urls import path
from .views import ThanksView, ServiceListView, OrdersListView, OrderDetailView, ServiceCreateView, create_review, ThanksForReviewView, order_create, get_master_info, masters_services_by_id

# Эти маршруты будут доступны с префиксом /barbershop/
urlpatterns = [

    path('thanks/', ThanksView.as_view(), name="thanks"),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/create/', ServiceCreateView.as_view(), name='service_create'),
    path('review/create/', create_review, name='create_review'),
    path('thanks/review/', ThanksForReviewView.as_view(), name='thanks_for_the_review'),
    path("masters_services/", masters_services_by_id, name="masters_services_by_id_ajax"),
    path("order_create/", order_create, name="order_create"),
    path("api/master-info/", get_master_info, name="get_master_info"),
]
