from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q  # Импортируем Q для сложных запросов

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Кастомный бэкенд аутентификации, позволяющий войти по email или username
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
            
        try:
            # Ищем пользователя по username или email (без учета регистра)
            user = User.objects.get(
                Q(username__iexact=username) | 
                Q(email__iexact=username)
            )
            
            # Проверяем пароль и активность пользователя
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
                
        except User.DoesNotExist:
            # Пользователь не найден
            return None
        except User.MultipleObjectsReturned:
            # Нашли несколько пользователей (не должно происходить, если email уникален)
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None