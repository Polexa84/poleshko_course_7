from django.contrib import admin
from .models import Habit
from django.utils.html import format_html


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('get_action', 'time', 'place', 'user', 'is_pleasant', 'public_status')
    list_filter = ('user', 'is_pleasant', 'is_public', 'periodicity')
    search_fields = ('action', 'place', 'user__email', 'user__username')
    list_editable = ('is_pleasant',)
    list_per_page = 20
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'action', 'place', 'time')
        }),
        ('Детали привычки', {
            'fields': ('is_pleasant', 'periodicity', 'execution_time')
        }),
        ('Мотивация', {
            'fields': ('related_habit', 'reward'),
            'description': 'Выберите либо связанную привычку, либо вознаграждение'
        }),
        ('Видимость', {
            'fields': ('is_public',)
        })
    )

    def get_action(self, obj):
        return format_html(
            '<b>{}</b>',
            obj.action
        )

    get_action.short_description = 'Действие'

    def public_status(self, obj):
        if obj.is_public:
            return format_html(
                '<span style="color: green;">✓ Публичная</span>'
            )
        return format_html(
            '<span style="color: red;">✗ Приватная</span>'
        )

    public_status.short_description = 'Статус'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        return form