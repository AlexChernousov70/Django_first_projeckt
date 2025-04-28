from django.shortcuts import render
from django.http import HttpResponse
from .data import *
from .models import Order, Master, Service, Review
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def landing(request):
    context = {
        'masters': Master.objects.prefetch_related('services').all(),
        'services': Service.objects.only('id', 'name', 'price', 'duration', 'image').order_by('name'),
        'reviews': Review.objects.all(), # сортировка уже прописана в моделях
    }

    return render(request, 'core/landing.html', context)

def thanks(request):
    context = {
        'masters_count': Master.objects.count(),
    }
    return render(request, 'core/thanks.html', context)

@login_required
def orders_list(request):
    # Базовый запрос с оптимизацией
    orders = Order.objects.select_related("master").prefetch_related("services").order_by('-date_created')
    
    # search_query - поиск по номеру телефона, имени клиента, комментарию
    search_query = request.GET.get("search")
    # Если есть поисковый запрос
    if search_query:
        # Разбиваем поисковый запрос на поля, в которых будем искать
        search_fields = request.GET.getlist("search_in")  # Без значений по умолчанию
        # Создаем фильтры для каждого поля
        filters = Q()
        if "phone" in search_fields:
            filters |= Q(phone__icontains=search_query)
        if "name" in search_fields:
            filters |= Q(client_name__icontains=search_query)
        if "comment" in search_fields:
            filters |= Q(comment__icontains=search_query)
        # Фильтруем заказы по фильтрам
        orders = orders.filter(filters) if filters else orders.none()

    context = {
        'orders': orders,
        'is_orders_list': True
    }
    return render(request, 'core/orders_list.html', context)

@login_required
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id) # Теперь у нас есть объект заказа, а не список
    except Order.DoesNotExist:
        # Если заказ не найден, возвращаем 404 - данные не найдены
        return HttpResponse(status=404)
    master = order.master
    context = {
        "order": order, 
        "master": master, 
        "title": f"Заказ №{order_id}",
        'is_orders_detail': True
    }
    return render(request, 'core/order_detail.html', context)