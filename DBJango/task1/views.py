from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from .forms import UserRegister
from .models import *


class platform(TemplateView):
    template_name = 'platform.html'


def games(request):
    game_list = Game.objects.all()
    context = {"game_list": game_list, }
    return render(request, 'games.html', context)


class cart(TemplateView):
    template_name = 'cart.html'
# Create your views here.


info = {}


def sign_up_by_html(request):
    buyers = Buyer.objects.all()
    users = []
    for user in buyers:
        users.append(user.name)

    if request.method == 'POST':
        register_user = False
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = int(request.POST.get('age'))
        if username in users:
            info['error'] = f'Пользователь {username} уже существует'
        else:
            if repeat_password == password:
                if age >= 18:
                    register_user = True
                else:
                    info['error'] = 'Вы должны быть старше 18'
            else:
                info['error'] = 'Пароли не совпадают'
        if register_user:
            out_message = f'Приветствуем, {username}!'
            Buyer.objects.create(name=username, balance=0, age=age)
            print(out_message)
        else:
            out_message = info['error']
        return HttpResponse(out_message)
    return render(request, 'registration_page.html', info)


def sign_up_by_django(request):
    buyers = Buyer.objects.all()
    users = []
    for user in buyers:
        users.append(user.name)

    if request.method == 'POST':
        register_user = False
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = int(form.cleaned_data['age'])
            if username in users:
                info['error'] = f'Пользователь с именем {username} уже существует'
            else:
                if repeat_password == password:
                    if age >= 18:
                        register_user = True
                    else:
                        info['error'] = 'Вы должны быть старше 18'
                else:
                    info['error'] = 'Пароли не совпадают'
            if register_user:
                out_message = f'Приветствуем, {username}!'
                Buyer.objects.create(name=username,balance=0,age=age)
                print(out_message)
            else:
                out_message = info['error']
        return HttpResponse(out_message)

    else:
        form = UserRegister()
    info['form'] = form
    return render(request, 'registration_page.html', info)
