from django.shortcuts import render


def index(request):
    # context = {
    #     'signup_form': CustomUserCreationForm,
    #     'login_form': UserAuthenticationForm,
    # }

    context = {}

    return render(request, 'index.html', context)


def adm(request):
    context = {}

    return render(request, 'admin.html', context)
