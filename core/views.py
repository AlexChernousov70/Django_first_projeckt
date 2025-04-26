from django.shortcuts import render
from django.http import HttpResponse
from .data import *
from .models import Order, Master, Service


def landing(request):
    context = {
        'masters': Master.objects.all(),
        'services': Service.objects.all(),
    }

    return render(request, 'core/landing.html', context)

def thanks(request):
    context = {
        'masters_count': len(masters)
    }
    return render(request, 'core/thanks.html', context)
    

def orders_list(request):
    context = {
        'orders': orders
    }
    return render(request, 'core/orders_list.html', context)

def order_detail(request, order_id):
    try:
        order = [o for o in orders if o["id"] == order_id][0]
    except IndexError:
        # Если заказ не найден, возвращаем 404 - данные не найдены
        return HttpResponse(status=404)
    master_id = order["master_id"]
    master = next(m for m in masters if m["id"] == master_id)
    context = {"order": order, "master": master, "title": f"Заказ №{order_id}"}
    return render(request, 'order_detail.html', context)