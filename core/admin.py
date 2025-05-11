from django.contrib import admin
from .models import Order, Master, Service, Review
from django.contrib.admin import SimpleListFilter


# Регистрация в одну строку
admin.site.register(Order)
admin.site.register(Master)
admin.site.register(Service)


class ReviewAdmin(admin.ModelAdmin):
    """
    Этот класс позволяет настроить отображение отзывов в админ-панели. Он определяет, какие поля и фильтры будут отображаться в списке отзывов, а также какие действия можно выполнять с отзывами (например, публикация или снятие с публикации).
    """
    # Определяем поля, которые будут отображаться в списке отзывов
    list_display = ('id', 'client_name', 'master', 'rating', 'created_at', 'is_published')
    list_filter = ('is_published', 'rating', 'master', 'created_at')
    search_fields = ('client_name', 'text')
    list_editable = ('is_published',)
    list_per_page = 20
    date_hierarchy = 'created_at'
    actions = ['publish_selected', 'unpublish_selected']

    # Определяем поля, которые будут отображаться в форме редактирования отзыва
    fieldsets = (
        ('Основная информация', {
            'fields': ('client_name', 'master', 'rating', 'text')
        }),
        ('Модерация', {
            'fields': ('is_published', 'photo'),
            'classes': ('collapse',)
        }),
    )
    
    # Определяем методы для массовой публикации и снятия с публикации отзывов
    def publish_selected(self, queryset):
        queryset.update(is_published=True)
    publish_selected.short_description = "Опубликовать выбранные отзывы"
    
    def unpublish_selected(self, queryset):
        queryset.update(is_published=False)
    unpublish_selected.short_description = "Снять с публикации выбранные отзывы"

admin.site.register(Review, ReviewAdmin)

