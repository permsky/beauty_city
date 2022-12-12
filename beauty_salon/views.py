import json
import logging
import re
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.shortcuts import redirect, render

from .models import (
    CustomUser,
    Entry,
    Master,
    SMSCode,
    Salon,
    SchedulePoint,
    Procedure,
    Comment
)


logger = logging.getLogger(__name__)


def index(request):
    salons = Salon.objects.all()
    procedures = Procedure.objects.all()
    masters = Master.objects.all().annotate(comment_count=Count('ratings'))
    comments = Comment.objects.all()

    context = {
        'salons': salons,
        'procedures': procedures,
        'masters': masters,
        'comments': comments,
    }
    if request.method == 'POST' and not 'num1' in request.POST:
        body = json.loads(request.body)
        phone_number = request.session['phone_number'] = body['phone_number']
        user, _ = CustomUser.objects.get_or_create(phone_number=phone_number)
        SMSCode.objects.filter(client=user).delete()
        SMSCode.objects.create(number='1234', client=user)
    if request.method == 'POST' and 'num1' in request.POST:
        user = CustomUser.objects.get(
            phone_number=request.session['phone_number'])
        code = SMSCode.objects.get(client=user)
        code_text = (
            request.POST.get('num1')
            + request.POST.get('num2')
            + request.POST.get('num3')
            + request.POST.get('num4')
        )
        if code_text == code.number:
            login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
            code.delete()
        else:
            print('Wrong code')
            code.delete()

    return render(request, 'index.html', context)


def adm(request):
    context = {}

    return render(request, 'admin.html', context)


@login_required
def notes(request):
    current_date = datetime.now().date()
    entries = Entry.objects.filter(client=request.user)
    past_entries = entries.filter(time_point__date__lt=current_date)
    future_entries = entries.filter(time_point__date__gt=current_date)
    current_entries = entries.filter(time_point__date=current_date)
    debt = entries.filter(status='not_payed').aggregate(Sum('service__price'))
    context = {
        'past_entries': past_entries,
        'future_entries': future_entries,
        'current_entries': current_entries,
        'debt': debt
    }
    if request.method == 'POST':
        print(request.POST)
        request.user.first_name = request.POST['fname']
        entry = Entry.objects.get(id=request.POST['noteNumber'])
        Comment.objects.create(
            text=request.POST['popupTextarea'],
            date=entry.time_point.date,
            rating=request.POST['masterRating'],
            master=entry.time_point.master,
            client=request.user
        )

    return render(request, 'notes.html', context)


def service(request):
    if request.method == 'POST':
        service = json.loads(request.body)

        request.session['service'] = service

        return redirect('service_finally')
    else:
        # TODO удалить услугу при создании новой.
        # del request.session['service']

        salons = Salon.objects.all()

        context = {
            'salons': salons,
        }

        return render(request, 'service.html', context)


def service_finally(request):
    context = {}

    if service := request.session.get('service'):

        salon = service.get('salon')
        master = service.get('master')
        prof = service.get('prof')
        service = service.get('service')

        salon = salon.split('#', maxsplit=1)[0].strip()
        salon = Salon.objects.get(name=salon)

        master = Master.objects.get(name=master)

        price = int(re.sub(r'[\D]', '', service))

        service = service.replace('₽', '').strip()
        service = re.sub(r'[\d]', '', service).strip()

        service = Procedure.objects.get(name=service)

        if request.method == 'POST':
            user, is_new_user = CustomUser.objects.get_or_create(
                phone_number=request.POST.get('tel')
            )

            if is_new_user:
                user.username = request.POST.get('fname')
                user.save()

            login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])

            entry = Entry(
                status='not_payed',
                client=user,
                service=service,
                salon=salon,
                time_point=SchedulePoint.objects.all().filter(status='available').first()
            )

            entry.save()

            del request.session['service']

            return redirect('notes')

        else:
            context = {
                'salon': salon,
                'master': master,
                'prof': prof,
                'price': price,
                'service': service
            }
    else:
        return redirect('service')

    return render(request, 'serviceFinally.html', context)
