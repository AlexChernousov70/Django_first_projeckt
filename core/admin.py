from django.contrib import admin
from .models import Order, Master, Service, Review


# Регистрация в одну строку
admin.site.register(Order)
admin.site.register(Master)
admin.site.register(Service)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Этот класс позволяет настроить отображение отзывов в админ-панели. Он определяет, какие поля и фильтры будут отображаться в списке отзывов, а также какие действия можно выполнять с отзывами (например, публикация или снятие с публикации).
    """
    list_display = ('client_name', 'master', 'rating', 'created_at', 'is_published')
    list_filter = ('is_published', 'rating', 'master')
    search_fields = ('client_name', 'text')
    list_editable = ('is_published',)
    readonly_fields = ('created_at',)
    
    # Дополнительные действия
    actions = ['publish_reviews', 'unpublish_reviews']
    
    def publish_reviews(self, request, queryset):
        queryset.update(is_published=True)
    publish_reviews.short_description = "Опубликовать выбранные отзывы"
    
    def unpublish_reviews(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_reviews.short_description = "Снять с публикации выбранные отзывы"
    
    # Определяем методы для массовой публикации и снятия с публикации отзывов
    def publish_selected(self, request, queryset):
        queryset.update(is_published=True)
    publish_selected.short_description = "Опубликовать выбранные отзывы"
    
    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_selected.short_description = "Снять с публикации выбранные отзывы"