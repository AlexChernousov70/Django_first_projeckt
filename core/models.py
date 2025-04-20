from django.db import models


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
    email = models.EmailField(blank=True)
    experience = models.PositiveIntegerField(verbose_name="Стаж работы", help_text="Опыт работы в годах")
    # Многие ко многим
    # services = models.ManyToManyField("Service", related_name="masters")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
        ordering = ['name'] # сортировка по полю name

    def __str__(self):
        return f"{self.name} (Стаж: {self.experience} лет)"