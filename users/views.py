from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .forms import UserProfileUpdateForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    authentication_form = LoginForm  # Указываем нашу кастомную форму
    redirect_authenticated_user = True  # Перенаправлять уже авторизованных пользователей
    
    def form_valid(self, form):
        # Получаем username/email, который ввел пользователь
        username = form.cleaned_data.get('username')
        # Находим пользователя для приветствия
        try:
            user = User.objects.get(
                models.Q(username__iexact=username) | 
                models.Q(email__iexact=username)
            )
            messages.success(self.request, f'Добро пожаловать, {user.username}!')
        except:
            messages.success(self.request, 'Добро пожаловать!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка входа. Проверьте имя пользователя и пароль.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        """
        этот метод определяет URL, на который будет выполнено перенаправление после успешного входа в систему.
        """
        next_url = self.request.GET.get('next')
        return next_url if next_url else reverse_lazy('landing')
    
class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.user.is_authenticated: # гарантирует, что сообщение добавится после выхода пользователя из системы
            messages.info(request, 'Вы успешно вышли из системы.')
        return response
    
    def get_next_page(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else reverse_lazy('landing')
    
def get_next_page(self):
    next_url = self.request.GET.get('next')
    return next_url if next_url else reverse_lazy('landing') # Это позволит поддерживать перенаправление после выхода, если в URL был передан next
    
class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('landing')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)  # Автоматический вход после регистрации
        messages.success(self.request, 'Регистрация прошла успешно! Добро пожаловать!')
        return response
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'Вы уже авторизованы!')
            return redirect('landing')
        return super().dispatch(request, *args, **kwargs)
    

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = User  # Используем стандартную модель User
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        """Проверяем, что пользователь запрашивает свой профиль."""
        user = super().get_object(queryset)
        if user != self.request.user:
            raise PermissionDenied("Вы можете просматривать только свой профиль.")
        return user

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileUpdateForm
    template_name = 'users/profile_update_form.html'
    success_url = reverse_lazy('profile_detail')  # Перенаправление после успешного обновления

    def get_object(self, queryset=None):
        return self.request.user  # Редактируем текущего пользователя

    def form_valid(self, form):
        if not any(m.message == 'Профиль успешно обновлён!' for m in messages.get_messages(self.request)): # Проверяем, что сообщение еще не было добавлено
            messages.success(self.request, 'Профиль успешно обновлён!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('profile_detail', kwargs={'pk': self.request.user.pk})