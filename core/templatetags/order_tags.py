from django import template

register = template.Library()

@register.filter
def status_class(status):
    status_map = {
        'not_approved': 'bg-warning',
        'moderated': 'bg-info',
        'spam': 'bg-danger',
        'approved': 'bg-success',
        'in_awaiting': 'bg-primary',
        'completed': 'bg-success',
        'canceled': 'bg-secondary',
    }
    return status_map.get(status, '')