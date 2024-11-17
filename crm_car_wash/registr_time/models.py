import time  # Добавьте этот импорт

from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.FloatField(null=True, blank=True)
    elapsed_time = models.FloatField(default=0)
    intervals = models.JSONField(default=list)

    def __str__(self):
        return f'Timer for {self.user.username}'
