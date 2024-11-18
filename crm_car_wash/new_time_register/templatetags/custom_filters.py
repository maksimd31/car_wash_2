# from django import template
#
# register = template.Library()
#
# @register.filter
# def duration_format(duration):
#     if duration:
#         total_seconds = int(duration.total_seconds())
#         hours, remainder = divmod(total_seconds, 3600)
#         minutes, seconds = divmod(remainder, 60)
#         return f"{hours} ч {minutes} мин {seconds} сек"
#     return "00:00:00"
#
#
from django import template
from datetime import timedelta

register = template.Library()


@register.filter
def duration_format(duration):
    if isinstance(duration, str):
        # Если это строка, попробуйте преобразовать ее в timedelta
        # Например, если строка в формате "HH:MM:SS"
        parts = duration.split(':')
        if len(parts) == 3:
            hours, minutes, seconds = map(int, parts)
            duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        else:
            return "00:00:00"  # Если формат неверный, возвращаем 00:00:00

    if isinstance(duration, timedelta):
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours} ч {minutes} мин {seconds} сек"

    return "00:00:00"  # Если duration не строка и не timedelta
