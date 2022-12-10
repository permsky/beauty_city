import json
import logging
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render

from .models import CustomUser, Entry, Master, SMSCode, Salon, Procedure

logger = logging.getLogger(__name__)


def index(request):
    if request.method == 'POST':
        print(request.POST)
        phone_number = request.POST.get('tel2')
        user, _ = CustomUser.objects.get_or_create(phone_number=phone_number)
        code = SMSCode.objects.create(number='1234', client=user)
        print(code.number)
        code_text = request.POST.get(
            'num1') + request.POST.get('num2') + request.POST.get('num3') + request.POST.get('num4')
        print(code_text)
        if code_text == code.number:
            login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
            code.delete()
        else:
            print('Wrong code')
    else:
        salons = Salon.objects.all()
        procedures = Procedure.objects.all()

    context = {
        'salons': salons,
        'procedures': procedures
    }

    return render(request, 'index.html', context)


def adm(request):
    context = {}

    return render(request, 'admin.html', context)


@login_required
def notes(request):
    if request.method == 'GET':
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        entries = Entry.objects.filter(client=request.user)
        past_entries = (
            entries
            .filter(time_point__date__lte=current_date)
            .filter(time_point__time__lte=current_time)
        )
        future_entries = (
            entries
            .filter(time_point__date__gt=current_date)
            .filter(time_point__time__gt=current_time)
        )
        debt = entries.filter(status='not_payed').aggregate(Sum('service__price'))
        context = {
            'past_entries': past_entries,
            'future_entries': future_entries,
            'debt': debt
        }

    return render(request, 'notes.html', context)


def service(request):
    context = {}

    if request.method == 'POST':
        body = json.loads(request.body)
        logger.info('AJAX POST')

        return redirect('service_finally')

    return render(request, 'service.html', context)


def service_finally(request):
    context = {}

    return render(request, 'serviceFinally.html', context)
