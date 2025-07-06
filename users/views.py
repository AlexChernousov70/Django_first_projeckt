from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login
from django.shortcuts import redirect

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