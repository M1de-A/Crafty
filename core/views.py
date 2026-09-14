from django.shortcuts import redirect
from django.conf import settings
from django.views.decorators.http import require_POST

@require_POST
def set_language(request):
    lang = request.POST.get('language', 'ru')
    if lang in {'ru', 'en'}:
        request.session['crafty_language'] = lang
    return redirect(request.POST.get('next') or request.META.get('HTTP_REFERER') or '/')

@require_POST
def set_currency(request):
    currency = request.POST.get('currency', 'RUB')
    if currency == 'RUB':
        request.session['crafty_currency'] = currency
    return redirect(request.POST.get('next') or request.META.get('HTTP_REFERER') or '/')
