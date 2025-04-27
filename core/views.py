from django.shortcuts import render
from django.http import HttpResponse
from .data import *
from .models import Order, Master, Service, Review
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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

    if request.method == "GET":
        # Получаем все заказы
        # Используем жадную загрузку для мастеров и услуг
        # all_orders = Order.objects.prefetch_related("master", "services").all()
        # all_orders = Order.objects.all()
        all_orders = Order.objects.select_related("master").prefetch_related("services").all()
    
        # Получаем строку поиска
        search_query = request.GET.get("search", None)

        if search_query:
            # Получаем чекбоксы
            check_boxes = request.GET.getlist("search_in")

            # Проверяем Чекбоксы и добавляем Q объекты в запрос
            # |= это оператор "или" для Q объектов
            filters = Q()

            if "phone" in check_boxes:
                # Полная запись где мы увеличиваем фильтры
                filters = filters | Q(phone__icontains=search_query)

            if "name" in check_boxes:
                # Сокращенная запись через inplace оператор
                filters |= Q(client_name__icontains=search_query)
            
            if "comment" in check_boxes:
                filters |= Q(comment__icontains=search_query)

            if filters:
                # Если фильтры появились. Если Q остался пустым, мы не попадем сюда
                all_orders = all_orders.filter(filters)

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