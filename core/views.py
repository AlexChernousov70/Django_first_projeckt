from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .data import *
from .models import Order, Master, Service, Review
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .forms import ServiceForm, ReviewForm, OrderForm
import json
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Миксин для ограничения доступа к странице
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist


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

class OrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'core/orders_list.html'
    context_object_name = 'orders' # Автоматически добавит 'orders' в контекст
    ordering = ['-date_created'] # По умолчанию будет использоваться queryset из model
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("master").prefetch_related("services") # Добавляем prefetch_related для оптимизации запросов
        
        # Добавляем фильтрацию по полям
        search_query = self.request.GET.get("search") # Получаем значение из GET-параметра 'search'
        if search_query: 
            search_fields = self.request.GET.getlist("search_in")
            filters = Q()
            if "phone" in search_fields:
                filters |= Q(phone__icontains=search_query)
            if "name" in search_fields:
                filters |= Q(client_name__icontains=search_query)
            if "comment" in search_fields:
                filters |= Q(comment__icontains=search_query)
            queryset = queryset.filter(filters) if filters else queryset.none()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_orders_list'] = True
        return context

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'core/order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'  # Используем order_id из URL вместо pk по умолчанию, нужнен для корректной работы с параметром order_id

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Order.DoesNotExist:
            raise Http404("Заказ не найден")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        context.update({
            'master': order.master,
            'title': f'Заказ №{order.id}',
            'is_orders_detail': True
        })
        return context

class ServiceListView(ListView):
    model = Service
    template_name = 'core/service_list.html'
    context_object_name = 'services' # Автоматически добавит 'services' в контекст
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # Получаем стандартный контекст от ListView, например 'object_list'
        context['title'] = 'Услуги' # Добавляем свои данные в контекст
        return context

class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'core/service_create.html'
    success_url = reverse_lazy('service_list')  # Используем reverse_lazy для безопасного импорта куда перенаправлять после успешного создания
    def test_func(self):
        """Проверка, что пользователь является staff"""
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        """Добавляем заголовок в контекст"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание услуги'
        return context

    def form_valid(self, form):
        """Обработка валидной формы"""
        response = super().form_valid(form)
        messages.success(self.request, f"Услуга {self.object.name} успешно создана!")
        return response

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'core/review_form.html'
    success_url = reverse_lazy('thanks_for_the_review')

    def get_context_data(self, **kwargs):
        """Добавляем заголовок в контекст"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Написать отзыв'
        return context

    def form_valid(self, form):
        """Объединенная логика для AJAX и обычных запросов"""
        # Сохраняем отзыв с is_published=False
        review = form.save(commit=False)
        review.is_published = False
        self.object = form.save()
        
        # Добавляем сообщение
        messages.success(self.request, 'Отзыв успешно добавлен!')
        
        # Обработка AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Отзыв успешно добавлен!'
            })
            
        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка невалидной формы для AJAX"""
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
        return super().form_invalid(form)

    def get_initial(self):
        """Предзаполнение поля master из GET-параметра"""
        initial = super().get_initial()
        if 'master_id' in self.request.GET:
            initial['master'] = self.request.GET.get('master_id')
        return initial

class ThanksForReviewView(TemplateView):
    template_name = 'core/thanks_for_the_review.html'

class MastersServicesAjaxView(View):
    """AJAX-представление для получения услуг мастера"""
    
    def get(self, request, master_id=None):
        """Обработка GET-запросов"""
        master_id = master_id or request.GET.get('master_id')
        return self._process_request(master_id)

    def post(self, request, master_id=None):
        """Обработка POST-запросов"""
        try:
            data = json.loads(request.body)
            master_id = master_id or data.get('master_id')
            return self._process_request(master_id)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data")

    def _process_request(self, master_id):
        """Общая логика обработки запроса"""
        if not master_id:
            return HttpResponseBadRequest("Master ID is required")

        master = get_object_or_404(Master, id=master_id)
        services = master.services.only('id', 'name').all()
        
        response_data = [
            {
                "id": service.id,
                "name": service.name,
                "price": service.price,  # Добавил цену, если нужна
                "duration": service.duration  # И длительность, если требуется
            }
            for service in services
        ]
        
        return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

class OrderCreateView(CreateView):
    form_class = OrderForm
    template_name = 'core/order_form.html'

    def get_success_url(self):
        """Перенаправление на страницу благодарности с параметром source='order'"""
        return reverse('thanks') + '?source=order'

    def get_context_data(self, **kwargs):
        """Добавление дополнительного контекста"""
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Создание заказа',
            'button_text': 'Создать'
        })
        return context

    def form_valid(self, form):
        """Обработка валидной формы"""
        response = super().form_valid(form)
        client_name = form.cleaned_data.get('client_name')
        messages.success(self.request, f'Заказ для {client_name} успешно создан!')
        
        # Если реализованы уведомления (как в HW43)
        if hasattr(self, 'send_telegram_notification'):
            self.send_telegram_notification()
            
        return response

class MasterInfoAjaxView(View):
    """AJAX-представление для получения информации о мастере"""
    
    def get(self, request, *args, **kwargs):
        # Проверка AJAX-запроса
        if not request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success": False,
                "error": "Только AJAX-запросы разрешены"
            }, status=400)

        # Получение master_id
        master_id = request.GET.get("master_id")
        if not master_id:
            return JsonResponse({
                "success": False,
                "error": "Не указан ID мастера"
            }, status=400)

        # Получение данных мастера
        try:
            master = Master.objects.prefetch_related('services').get(pk=master_id)
            return JsonResponse({
                "success": True,
                "master": self._serialize_master(master)
            })
        except ObjectDoesNotExist:
            return JsonResponse({
                "success": False,
                "error": "Мастер не найден"
            }, status=404)

    def _serialize_master(self, master):
        """Сериализация данных мастера"""
        return {
            "id": master.id,
            "name": f"{master.first_name} {master.last_name}",
            "experience": master.experience,
            "photo": master.photo.url if master.photo else None,
            "services": list(
                master.services.values("id", "name", "price")
            ),
            "specialization": master.get_specialization_display() 
            if hasattr(master, 'get_specialization_display')
            else None,
        }