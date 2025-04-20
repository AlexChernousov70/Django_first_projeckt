from django import template

register = template.Library()

@register.filter
def status_class(status):
    status_map = {
        'новая': 'status-new',
        'подтвержденная': 'status-confirmed',
        'отмененная': 'status-cancelled',
        'выполненная': 'status-completed'
    }
    return status_map.get(status.lower(), '')