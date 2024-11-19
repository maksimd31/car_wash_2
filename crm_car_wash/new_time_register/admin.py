from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TimeInterval, DailySummary

admin.site.register(TimeInterval)
admin.site.register(DailySummary)
