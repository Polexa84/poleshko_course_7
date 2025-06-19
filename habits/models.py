from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='related_to', verbose_name='Связанная привычка')
    periodicity = models.IntegerField(default=1, verbose_name='Периодичность (в днях)')
    reward = models.CharField(max_length=255, verbose_name='Вознаграждение', blank=True) # Разрешаем пустое вознаграждение
    execution_time = models.IntegerField(verbose_name='Время на выполнение (в секундах)')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности')

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"

    def clean(self):
        if self.related_habit and self.reward:
            raise ValidationError("Нельзя выбирать и связанную привычку, и вознаграждение одновременно.")

        if self.execution_time > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки.")

        if self.is_pleasant:
            if self.related_habit or self.reward:
                raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")

        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError("Нельзя выполнять привычку чаще чем 1 раз в день или реже, чем раз в неделю.")

    def save(self, *args, **kwargs):
        self.full_clean() # Вызываем clean() перед сохранением
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'