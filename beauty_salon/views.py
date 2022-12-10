import json
import logging

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from .models import CustomUser, SMSCode

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

    context = {}

    return render(request, 'index.html', context)


def adm(request):
    context = {}

    return render(request, 'admin.html', context)


def notes(request):
    context = {}

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
