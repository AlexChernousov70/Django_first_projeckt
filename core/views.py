from django.shortcuts import render
from django.http import HttpResponse
from .data import *
from .models import Order, Master, Service, Review
from django.contrib.auth.decorators import login_required

def landing(request):
    context = {
        'masters': Master.objects.all(),
        'services': Service.objects.all(),
        'reviews': Review.objects.all(),
    }

    return render(request, 'core/landing.html', context)

def thanks(request):
    context = {
        'masters_count': Master.objects.count(),
    }
    return render(request, 'core/thanks.html', context)
    
@login_required
def orders_list(request):

    orders = Order.objects.all().order_by('-date_created') # получение всех объектов, сортированных по дате создания
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