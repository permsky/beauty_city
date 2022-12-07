from django.shortcuts import render


def index(request):
    # context = {
    #     'signup_form': CustomUserCreationForm,
    #     'login_form': UserAuthenticationForm,
    # }

    context = {}

    return render(request, 'index.html', context)
