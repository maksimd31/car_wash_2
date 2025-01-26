from django.utils import timezone
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class TimeInterval(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='time_intervals')
    start_time = models.TimeField(null=True, blank=True, verbose_name='старт')
    end_time = models.TimeField(null=True, blank=True, verbose_name='стоп')
    duration = models.DurationField(null=True, blank=True, verbose_name='Длительность')
    date_create = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            self.duration = (datetime.combine(datetime.min, self.end_time) -
                             datetime.combine(datetime.min, self.start_time))
        super().save(*args, **kwargs)


class DailySummary(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date = models.DateField()
    interval_count = models.PositiveIntegerField(default=0)
    total_time = models.DurationField(default=timezone.timedelta())

    def __str__(self):
        return f"{self.date} - {self.user.username}"



class StopwatchRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.duration}"
