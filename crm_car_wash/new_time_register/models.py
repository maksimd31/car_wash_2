# from django.db import models
#
# # Create your models here.
# import time  # Добавьте этот импорт
#
# from django.contrib.auth.models import User
# from django.db import models
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
#
# class Timer(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     start_time = models.FloatField(null=True, blank=True)
#     elapsed_time = models.FloatField(default=0)
#     intervals = models.JSONField(default=list)
#     intervals_1 = models.JSONField(default=list)
#
#
#     def __str__(self):
#         return f'Timer for {self.user.username}'

from django.db import models
from django.contrib.auth.models import User
import json


class Timer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_time = models.FloatField(null=True, blank=True)
    elapsed_time = models.FloatField(default=0)
    intervals = models.TextField(default='[]')  # Хранение интервалов в виде JSON

    def get_intervals(self):
        return json.loads(self.intervals)

    def set_intervals(self, intervals):
        self.intervals = json.dumps(intervals)


#
# class TimeSegment(models.Model):
#     start_time = models.DateTimeField(null=True, blank=True)
#     end_time = models.DateTimeField(null=True, blank=True)
#     duration = models.DurationField(null=True, blank=True)
#
#     def save(self, *args, **kwargs):
#         if self.start_time and self.end_time:
#             self.duration = self.end_time - self.start_time
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return f"Segment from {self.start_time} to {self.end_time} with duration {self.duration}"

# from django.db import models
# from django.utils import timezone
#
# class TimeSegment(models.Model):
#     start_time = models.DateTimeField(null=True, blank=True)
#     end_time = models.DateTimeField(null=True, blank=True)
#     duration = models.DurationField(null=True, blank=True)
#
#     def save(self, *args, **kwargs):
#         if self.start_time and self.end_time:
#             # Убедитесь, что оба времени имеют временную зону
#             if self.start_time.tzinfo is None:
#                 self.start_time = timezone.make_aware(self.start_time)
#             if self.end_time.tzinfo is None:
#                 self.end_time = timezone.make_aware(self.end_time)
#             self.duration = self.end_time - self.start_time
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return f"Segment from {self.start_time} to {self.end_time} with duration {self.duration}"
class TimeInterval(models.Model):
    start_time = models.DateTimeField('Start Time')
    end_time = models.DateTimeField('End Time')
    duration = models.DurationField('Duration')

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Time Interval: {self.start_time} - {self.end_time} ({self.duration})"
