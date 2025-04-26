from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator # необходимо для валидации поля rating модели Review


class Order(models.Model):
    """
    Класс = таблица в БД, атрибуты = поля в таблице
    """
    # Статусы заказов
    STATUS_CHOICES = [
        ("not_approved", "Не подтвержден"),
        ("moderated", "Прошел модерацию"),
        ("spam", "Спам"),
        ("approved", "Подтвержден"),
        ("in_awaiting", "В ожидании"),
        ("completed", "Завершен"),
        ("canceled", "Отменен"),
    ]

    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="not_approved", verbose_name="Статус") # определили строго определенный набор значений
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    # Один ко многим
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True, related_name="orders")
    # Многие ко многим
    services = models.ManyToManyField("Service", verbose_name="Услуги")
    appointment_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата и время записи")

    class Meta:
        """
        Используется для определения метаданных модели, для каждой модели свой класс Meta
        """
        verbose_name = "Заказ" # verbose_name - задаёт удобное для человека название модели в единственном числе. Используется в админ-панели Django и других местах интерфейса.
        verbose_name_plural = "Заказы" # verbose_name_plural - задаёт название модели во множественном числе. Если не указать, Django автоматически добавит "s" к verbose_name.
        ordering = ['-appointment_date'] # определяет порядок сортировки объектов модели по умолчанию. В данном случае ['-appointment_date'] означает сортировку по полю appointment_date в обратном порядке (от новых к старым).

    def __str__(self):
        return f"Заказ #{self.id} - {self.client_name} ({self.get_status_display()})"

class Master(models.Model):
    """Модель мастеров"""
    name = models.CharField(max_length=150, verbose_name="Имя")
    photo = models.ImageField(upload_to="images/masters/", blank=True, null=True, verbose_name="Фотография")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    email = models.EmailField(blank=True, verbose_name="Email")
    experience = models.PositiveIntegerField(verbose_name="Стаж работы", help_text="Опыт работы в годах")
    # Многие ко многим
    services = models.ManyToManyField("Service", related_name="masters")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
        ordering = ['name'] # сортировка по полю name

    def __str__(self):
        return f"{self.name} (Стаж: {self.experience} лет)"
    
class Service(models.Model):
    """Модель услуги"""
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена услуги")
    duration = models.PositiveIntegerField(help_text="Время выполнения в минутах", verbose_name="Время выполнения услуги")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(upload_to="images/services/", blank=True, null=True, verbose_name="Изображение услуги")

    class Meta:
        """Имена для отображения в админ-панели и в интерфейсе пользователя, а также сортировка по имени"""
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.price}₽"

class Review(models.Model):
    """Модель отзыва о мастере"""
    RATING_CHOICES = [
        (1, '1 - Плохо'),
        (2, '2 - Удовлетворительно'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]
    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Имя клиента"
    )
    master = models.ForeignKey(
        'Master',
        on_delete=models.CASCADE,
        verbose_name="Мастер",
        related_name='reviews'
    )
    photo = models.ImageField(
        upload_to="reviews/",
        blank=True,
        null=True,
        verbose_name="Фотография"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        verbose_name="Оценка"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликован"
    )

    class Meta:
        """Имена для отображения в админ-панели и в интерфейсе пользователя, а также сортировка по полям модели и индексы для ускорения запросов."""
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at'] # сортировка по полю created_at в обратном порядке (от новых к старым)
        indexes = [
            models.Index(fields=['-created_at', 'rating']),
        ] # создание индекса для ускорения запросов по полям created_at и rating

"""
Таблицы базы данных - это классы Python, которые наследуются от класса models.Model.
Каждая таблица имеет свои поля, которые определяются как атрибуты класса.
Поля могут быть разных типов, таких как CharField, IntegerField, DateField и т.д.

CharField - строка фиксированной длины (max_length - максимальная длина строки)
IntegerField - целое
DateField - дата
DateTimeField - дата и время
DecimalField - десятичное число (max_digits - максимальное количество цифр, decimal_places - количество цифр после запятой)
BooleanField - булево значение
ImageField - изображение (upload_to - путь для загрузки изображения)

verbose_name - имя поля для отображения в админ-панели и в интерфейсе пользователя
choices=STATUS_CHOICES - выбор из списка, который создаем сами
blank - можно ли оставить поле пустым(пустая строка ""), 
null - позволяет сохранить NULL в базе данных

ForeignKey - связь с другой таблицей
ManyToManyField - связь многие ко многим
on_delete - что делать с данными, если удалить запись из связанной таблицы
related_name - параметр, который используется в полях отношений (ForeignKey, ManyToManyField, OneToOneField) для определения имени обратной связи от связанной модели к модели, в которой определено поле.
"""