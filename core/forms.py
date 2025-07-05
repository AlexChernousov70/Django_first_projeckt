# Импорт служебных объектов Form
from django import forms
from django.core.exceptions import ValidationError
from .models import Review, Order, Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'duration', 'is_popular', 'image']
        labels = {
            'name': 'Название услуги',
            'description': 'Описание услуги',
            'price': 'Цена услуги',
            'duration': 'Время выполнения услуги (мин)',
            'is_popular': 'Популярная услуга',
            'image': 'Изображение услуги'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Введите название услуги',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Введите описание услуги',
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Введите цену услуги',
                'class': 'form-control'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'is_popular': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        error_messages = {
            'name': {
                'required': 'Пожалуйста, укажите название услуги',
                'max_length': 'Название услуги не должно превышать 200 символов'
            },
            'description': {
                'required': 'Необходимо добавить описание услуги'
            },
            'price': {
                'required': 'Пожалуйста, укажите стоимость услуги',
                'invalid': 'Введите корректную стоимость (например: 1500.00)',
                'max_digits': 'Стоимость не может содержать более 10 цифр',
                'max_decimal_places': 'Стоимость не может содержать более 2 знаков после запятой'
            },
        }

    def clean_description(self):
        """
        Метод валидации для поля description
        """
        description = self.cleaned_data.get('description')
        if 'плохое' in description.lower():
            raise ValidationError("В описании не должно быть слова 'плохое'")
        return description

class ReviewForm(forms.ModelForm):
    """Создаем форму на основе модели Review"""
    rating = forms.ChoiceField(
    choices=[
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ],
    widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
    label='Оценка'
    )

    class Meta:
        """
        Класс мета - в этом классе описывается модель, по которой будет строиться форма, и поля, которые будут отображаться в форме.
        """
        # от какой модели наследуемся
        model = Review
        # Поля, которые будут отображаться в форме
        fields = ['client_name', 'text', 'rating', 'master', 'photo']
        # Выводимые подсказки
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст вашего отзыва',
                'rows': 4
            }),
            'master': forms.Select(attrs={
                'class': 'form-select'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        # Подписи к полям
        labels = {
            'client_name': 'Ваше имя:',
            'text': 'Текст отзыва:',
            'rating': 'Оценка',
            'master': 'Мастер',
            'photo': 'Фотография (необязательно)'
        }

class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс form-control к каждому полю формы
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

    # def save(self):
    #     # Сохраняем объект заказа
    #     Сюда можно вклинить логику валидации на бекенде (проверить что мастер предоставляет ВСЕ выбранные услуги)
    #     super().save()

    class Meta:
        model = Order
        fields = [
            "client_name",
            "phone",
            "comment",
            "master",
            "services",
            "appointment_date",
        ]