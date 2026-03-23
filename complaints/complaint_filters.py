from django import template

register = template.Library()

@register.filter
def filter_status(complaints, status):
    if status.lower() == "all":
        return complaints
    return complaints.filter(status=status)