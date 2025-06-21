from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', help_text='Пользователь, создавший привычку.')
    place = models.CharField(max_length=255, verbose_name='Место', help_text='Место, где выполняется привычка.')
    time = models.TimeField(verbose_name='Время', help_text='Время выполнения привычки.')
    action = models.CharField(max_length=255, verbose_name='Действие', help_text='Описание действия, представляющего привычку.')
    is_pleasant = models.BooleanField(default=False, verbose_name='Признак приятной привычки', help_text='Укажите, является ли привычка приятной.')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='related_to', verbose_name='Связанная привычка', help_text='Приятная привычка, связанная с выполнением этой привычки.')
    periodicity = models.IntegerField(default=1, verbose_name='Периодичность (в днях)', help_text='Периодичность выполнения привычки (в днях, от 1 до 7).')
    reward = models.CharField(max_length=255, verbose_name='Вознаграждение', blank=True, help_text='Вознаграждение после выполнения привычки.') # Разрешаем пустое вознаграждение
    execution_time = models.IntegerField(verbose_name='Время на выполнение (в секундах)', help_text='Время, необходимое для выполнения привычки (в секундах).')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности', help_text='Укажите, является ли привычка публичной.')

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
            raise ValidationError("Нельзя выполнять привычку реже, чем раз в неделю (7 дней).")

    def save(self, *args, **kwargs):
        self.full_clean() # Вызываем clean() перед сохранением
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['time'] # Сортируем привычки по времени выполнения