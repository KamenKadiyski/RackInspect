from tkinter.constants import CASCADE

from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=4)
    description = models.CharField(max_length=200)
    # Добавени са скоби ()
    number_of_positions = models.PositiveSmallIntegerField()
    number_of_levels = models.PositiveSmallIntegerField()

class Component(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

class InspectionRecord(models.Model):
    # Добавен е on_delete
    location = models.ForeignKey(to=Location, on_delete=models.CASCADE)
    # Добавени са скоби ()
    position = models.PositiveSmallIntegerField()
    level = models.CharField(max_length=2)
    component = models.ForeignKey(to=Component, on_delete=models.CASCADE)
    is_fixed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
