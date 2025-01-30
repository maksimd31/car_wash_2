# from django.utils import timezone
# from datetime import datetime,timedelta
# from django.db import models
# from django.contrib.auth.models import User
#
# class Day_one(models.Model):
#     user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
#     time_interval = models.ForeignKey(TimeInterval,on_delete=models.CASCADE)
#     date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#
#
#
#
# class TimeInterval(models.Model):
#     user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='time_intervals')
#     start_time = models.TimeField(null=True, blank=True, verbose_name='старт')
#     end_time = models.TimeField(null=True, blank=True, verbose_name='стоп')
#     duration = models.DurationField(null=True, blank=True, verbose_name='Длительность')
#     break_duration = models.DurationField(null=True, blank=True, verbose_name='Перерыв')  # New field
#     date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#
#     def save(self, *args, **kwargs):
#         if self.start_time and self.end_time:
#             self.duration = (datetime.combine(datetime.min, self.end_time) -
#                              datetime.combine(datetime.min, self.start_time))
#
#             # Calculate break duration
#             last_intervals = TimeInterval.objects.filter(user=self.user,
#                                                          date_create__date=self.date_create.date()).order_by(
#                 '-date_create')[:2]
#             if len(last_intervals) == 2:
#                 last_interval = last_intervals[0]
#                 second_last_interval = last_intervals[1]
#
#                 # Calculate the break duration
#                 last_end_time = datetime.combine(datetime.min, last_interval.start_time)
#                 second_last_end_time = datetime.combine(datetime.min, second_last_interval.end_time)
#
#                 # Calculate the break time in minutes
#                 break_time = (last_end_time - second_last_end_time).total_seconds() / 60
#
#                 # If break_time is positive, set it; otherwise, set it to zero
#                 self.break_duration = timedelta(minutes=max(0, break_time))
#             else:
#                 self.break_duration = timedelta(0)  # No break if there are less than 2 intervals
#
#         super().save(*args, **kwargs)
#
#
# class DailySummary(models.Model):
#     user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
#     date = models.DateField()
#     interval_count = models.PositiveIntegerField(default=0)
#     total_time = models.DurationField(default=timezone.timedelta())
#     date_create = models.DateTimeField(auto_now_add=True,null=True,blank=True)
#
#
#     def __str__(self):
#         return f"{self.date} - {self.user.username}"
#
#
#
# class StopwatchRecord(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     duration = models.DurationField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username} - {self.duration}"

from django.utils import timezone
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User

class TimeInterval(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='time_intervals')
    start_time = models.TimeField(null=True, blank=True, verbose_name='старт')
    end_time = models.TimeField(null=True, blank=True, verbose_name='стоп')
    duration = models.DurationField(null=True, blank=True, verbose_name='Длительность')
    break_duration = models.DurationField(null=True, blank=True, verbose_name='Перерыв')  # New field
    date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            self.duration = (datetime.combine(datetime.min, self.end_time) -
                             datetime.combine(datetime.min, self.start_time))

            # Calculate break duration
            last_intervals = TimeInterval.objects.filter(user=self.user,
                                                         date_create__date=self.date_create.date()).order_by(
                '-date_create')[:2]
            if len(last_intervals) == 2:
                last_interval = last_intervals[0]
                second_last_interval = last_intervals[1]

                # Calculate the break duration
                last_end_time = datetime.combine(datetime.min, last_interval.start_time)
                second_last_end_time = datetime.combine(datetime.min, second_last_interval.end_time)

                # Calculate the break time in minutes
                break_time = (last_end_time - second_last_end_time).total_seconds() / 60

                # If break_time is positive, set it; otherwise, set it to zero
                self.break_duration = timedelta(minutes=max(0, break_time))
            else:
                self.break_duration = timedelta(0)  # No break if there are less than 2 intervals

        super().save(*args, **kwargs)


class DailySummary(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date = models.DateField()
    interval_count = models.PositiveIntegerField(default=0)
    total_time = models.DurationField(default=timezone.timedelta())
    date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.user.username}"


class DayOne(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date = models.DateField()
    time_intervals = models.ManyToManyField(TimeInterval, related_name='day_ones')
    daily_summary = models.ForeignKey(DailySummary, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.user.username}"



