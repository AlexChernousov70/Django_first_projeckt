"""
Настройка URL-адресов для проекта barbershop.

Список urlpatterns связывает URL-адреса с представлениями. Подробнее см. документацию:
https://docs.djangoproject.com/en/5.1/topics/http/urls/
Примеры:

Для view-функций:
1. Импортируйте view: from my_app import views
2. Добавьте URL в urlpatterns: path('', views.home, name='home')

Для view-классов:
1. Импортируйте view: from other_app.views import Home
2. Добавьте URL в urlpatterns: path('', Home.as_view(), name='home')

Подключение другого URL-конфига:
1. Импортируйте функцию include(): from django.urls import include, path
2. Добавьте URL в urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from core.views import landing


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    # Подключаем маршруты из приложения core
    path('barbershop/', include('core.urls')),
]
