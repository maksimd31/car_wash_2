from django import template

register = template.Library()

@register.filter
def duration_format(duration):
    if duration:
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours} ч {minutes} мин {seconds} сек"
    return "00:00:00"
