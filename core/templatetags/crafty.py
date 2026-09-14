from django import template
from django.utils.formats import number_format
register = template.Library()

@register.filter
def money(value):
    try:
        return f"{number_format(value, decimal_pos=0, use_l10n=True)} ₽"
    except (TypeError, ValueError):
        return f"{value} ₽"


@register.filter
def status_passed(value, order):
    ranks={'new':0,'paid':1,'processing':2,'shipped':3,'delivered':4,'completed':5,'cancelled':99,'return':98,'dispute':100}
    current=ranks.get(getattr(order,'status',''),-1); target=ranks.get(str(value),-1)
    if getattr(order,'status','')=='cancelled': return target <= 2 and target >= 0
    if getattr(order,'status','')=='return': return target <= 5 and target >= 0
    return target < current
