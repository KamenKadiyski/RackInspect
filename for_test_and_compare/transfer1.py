from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    """Складова зона или сектор (напр. Зона А, Сектор 3)"""
    name = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=200, blank=True)
    number_of_positions = models.PositiveSmallIntegerField()
    number_of_levels = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Component(models.Model):
    """Компоненти: Вертикална рамка, Хоризонтална греда, Осигурителен щифт, Палета и др."""
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class InspectionRecord(models.Model):
    """Запис за инспекция на конкретно местоположение на рафта"""

    # Светофарна система за оценка на риска (EN 15635 стандарт)
    class RiskLevel(models.TextChoices):
        NONE = 'GREEN', 'Зелен (Нисък риск / Наблюдение)'
        AMBER = 'AMBER', 'Жълт (Сериозен дефект / Ремонт до 28 дни)'
        RED = 'RED', 'Червен (Критичен дефект / Незабавно разтоварване)'

    inspector = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Инспектор")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='inspections')

    # Позиция (цифра) и Ниво (буква: A, B, C...)
    position = models.PositiveSmallIntegerField()
    level = models.CharField(max_length=2)  # Може да добавите валидация за букви (A-Z)

    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    risk_level = models.CharField(max_length=10, choices=RiskLevel.choices, default=RiskLevel.NONE)

    # Коментари и бележки
    comments = models.TextField(blank=True, help_text="Описание на щетата или специфични бележки")

    # Статус на ремонта
    is_fixed = models.BooleanField(default=False, verbose_name="Поправено ли е?")
    fixed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата на ремонт")

    # Снимка на щетата (изисква инсталиран Pillow: pip install Pillow)
    image = models.ImageField(upload_to='inspection_photos/', null=True, blank=True)

    # Одит на времето
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        # Индекси за по-бързо търсене по локация, позиция и ниво
        indexes = [
            models.Index(fields=['location', 'position', 'level']),
        ]

    def __str__(self):
        return f"{self.location.name}-{self.position}{self.level} | {self.component.name} ({self.risk_level})"
