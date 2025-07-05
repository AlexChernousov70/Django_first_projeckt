from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .data import *
from .models import Order, Master, Service, Review
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .forms import ServiceForm, ReviewForm, OrderForm
import json

from django.views.generic import TemplateView, ListView

class LandingPageView(TemplateView):
    template_name = 'core/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'masters': Master.objects.prefetch_related('services').all(),
            'services': Service.objects.only('id', 'name', 'price', 'duration', 'image').order_by('name'),
            'reviews': Review.objects.all(),
        })
        return context
    
class ThanksView(TemplateView):
    template_name = 'core/thanks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters_count'] = Master.objects.count()
        return context



@login_required
def orders_list(request):
    orders = Order.objects.select_related("master").prefetch_related("services").order_by('-date_created')
    
    search_query = request.GET.get("search")
    if search_query:
        search_fields = request.GET.getlist("search_in")
        filters = Q()
        if "phone" in search_fields:
            filters |= Q(phone__icontains=search_query)
        if "name" in search_fields:
            filters |= Q(client_name__icontains=search_query)
        if "comment" in search_fields:
            filters |= Q(comment__icontains=search_query)
        orders = orders.filter(filters) if filters else orders.none()

    context = {
        'orders': orders,
        'is_orders_list': True
    }
    return render(request, 'core/orders_list.html', context)

@login_required
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
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
    services = Service.objects.all()
    context = {
        'title': 'Услуги',
        'services': services,
    }
    return render(request, 'core/service_list.html', context)

def service_create(request):
    if request.method == "GET":
        form = ServiceForm()
        context = {
            "title": "Создание услуги",
            "form": form,
        }
        return render(request, "core/service_create.html", context)

    elif request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            price = form.cleaned_data.get("price")

            new_service = Service.objects.create(
                name=name,
                description=description,
                price=price,
            )

            messages.success(request, f"Услуга {new_service.name} успешно создана!")
            return redirect("service_list")

        context = {
            "title": "Создание услуги",
            "form": form,
        }
        return render(request, "core/service_create.html", context)

def create_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.is_published = False
            form.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('thanks_for_the_review')
    else:
        form = ReviewForm()

    context = {
        "title": "Написать отзыв",
        "form": form,
    }
    return render(request, "core/review_form.html", context)

def thanks_for_the_review(request):
    return render(request, 'core/thanks_for_the_review.html')

def masters_services_by_id(request, master_id=None):
    if master_id is None:
        try:
            data = json.loads(request.body)
            master_id = data.get("master_id")
        except json.JSONDecodeError:
            return HttpResponse(status=400)

    master = get_object_or_404(Master, id=master_id)
    services = master.services.all()

    response_data = []
    for service in services:
        response_data.append(
            {
                "id": service.id,
                "name": service.name,
            }
        )
    return HttpResponse(
        json.dumps(response_data, ensure_ascii=False, indent=4),
        content_type="application/json",
    )

def order_create(request):
    if request.method == "GET":
        form = OrderForm()
        context = {
            "title": "Создание заказа",
            "form": form,
            "button_text": "Создать",
        }
        return render(request, "core/order_form.html", context)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            client_name = form.cleaned_data.get("client_name")
            messages.success(request, f"Заказ для {client_name} успешно создан!")
            return redirect("thanks")

        context = {
            "title": "Создание заказа",
            "form": form,
            "button_text": "Создать",
        }
        return render(request, "core/order_form.html", context)

def get_master_info(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        master_id = request.GET.get("master_id")
        if master_id:
            try:
                master = Master.objects.get(pk=master_id)
                master_data = {
                    "id": master.id,
                    "name": f"{master.first_name} {master.last_name}",
                    "experience": master.experience,
                    "photo": master.photo.url if master.photo else None,
                    "services": list(master.services.values("id", "name", "price")),
                }
                return JsonResponse({"success": True, "master": master_data})
            except Master.DoesNotExist:
                return JsonResponse({"success": False, "error": "Мастер не найден"})
        return JsonResponse({"success": False, "error": "Не указан ID мастера"})
    return JsonResponse({"success": False, "error": "Недопустимый запрос"})