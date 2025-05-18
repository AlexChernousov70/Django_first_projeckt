from django.shortcuts import render, redirect
from django.http import HttpResponse
from .data import *
from .models import Order, Master, Service, Review
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# messages - это встроенный модуль Django для отображения сообщений пользователю
from django.contrib import messages
from .forms import ServiceForm, ReviewForm, OrderForm


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

def service_list(request):
    services = Service.objects.all
    context = {
        'title': 'Услуги',
        'services': services,
    }
    return render(request, 'core/service_list.html', context)

def service_create(request):
    """
    Отображаем пустую форму при GET
    Определяем логику при отправке формы пользователем
    """
    # Если метод GET - возвращаем пустую форму
    if request.method == "GET":
        form = ServiceForm()
        context = {
            "title": "Создание услуги",
            "form": form,
        }
        return render(request, "core/service_create.html", context)

    elif request.method == "POST":
        # Создаем форму и передаем в нее POST данные
        form = ServiceForm(request.POST)

        # Если форма валидна:
        if form.is_valid():
            # Получаем очищенные(проверенные, валидные) данные из формы
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            price = form.cleaned_data.get("price")

            # Создаем новую услугу
            new_service = Service.objects.create(
                name=name,
                description=description,
                price=price,
            )

            # Даем пользователю уведомление об успешном создании
            messages.success(request, f"Услуга {new_service.name} успешно создана!")

            # Перенаправляем на страницу со всеми услугами
            return redirect("service_list")

        # В случае ошибок валидации Django автоматически заполнит form.errors и отобразит их в шаблоне, поэтому просто возвращаем форму
        context = {
            "title": "Создание услуги",
            "form": form,
        }
        return render(request, "core/service_create.html", context)

def create_review(request):
    """Функциональное представление для создания отзыва"""
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            # Дополнительная защита от опубликования (не смотря на то, что is_published исключено из формы)
            review = form.save(commit=False)  # Не сохраняем сразу в БД
            review.is_published = False       # Принудительно устанавливаем значение

            form.save() # Сохраняем отзыв в БД
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('thanks_for_the_review')
    else: # Если метод GET, создаем пустую форму
        form = ReviewForm()

    context = {
        "title": "Написать отзыв",
        "form": form,
    }
    return render(request, "core/review_form.html", context)

def thanks_for_the_review(request):
    return render(request, 'core/thanks_for_the_review.html')

def create_order(request):
    """Функциональное представление для записи на услугу"""
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() # Сохраняем отзыв в БД
            messages.success(request, 'Запись оформлена!')
            return redirect('landing')
    else: # Если метод GET, создаем пустую форму
        form = OrderForm()

    context = {
        "title": "Записаться",
        "form": form,
    }
    return render(request, "core/order_create.html", context)

def get_master_info(request):
    """
    Универсальное представление для получения информации о мастере через AJAX.
    Возвращает данные мастера в формате JSON.
    """
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        master_id = request.GET.get('master_id')
        if master_id:
            try:
                master = Master.objects.get(pk=master_id)
                # Формируем данные для ответа
                master_data = {
                    'id': master.id,
                    'name': f"{master.name}",
                    'experience': master.experience,
                    'photo': master.photo.url if master.photo else None,
                    'services': list(master.services.values('id', 'name', 'price')),
                }
                return JsonResponse({'success': True, 'master': master_data})
            except Master.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Мастер не найден'})
        return JsonResponse({'success': False, 'error': 'Не указан ID мастера'})
    return JsonResponse({'success': False, 'error': 'Недопустимый запрос'})