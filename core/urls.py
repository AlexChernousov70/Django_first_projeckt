# core/urls.py
from django.urls import path
from .views import ThanksView, ThanksForReviewView, ServiceListView, OrdersListView, OrderDetailView, ServiceCreateView, ReviewCreateView, OrderCreateView, MasterInfoAjaxView, masters_services_by_id

# Эти маршруты будут доступны с префиксом /barbershop/
urlpatterns = [

    path('thanks/', ThanksView.as_view(), name="thanks"),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/create/', ServiceCreateView.as_view(), name='service_create'),
    path('review/create/', ReviewCreateView.as_view(), name='review_create'),
    path('thanks/review/', ThanksForReviewView.as_view(), name='thanks_for_the_review'),
    path("masters_services/", masters_services_by_id, name="masters_services_by_id_ajax"),
    path("order_create/", OrderCreateView.as_view(), name="order_create"),
    path("api/master-info/", MasterInfoAjaxView.as_view(), name="get_master_info"),
]
