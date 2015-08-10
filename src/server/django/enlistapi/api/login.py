# coding=utf-8
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

__author__ = 'nakayama'


# Post #
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth.login(request, user)
                return HttpResponse(status=200, reason="Login successful!")
            else:
                return HttpResponse(status=400, reason='Erro: Usuário não está ativo!')
        else:
            return HttpResponse(status=400, reason='Erro: Senha ou email incorretos!')

    else:
        return HttpResponse(status=400, reason="Wrong method!")


def register(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])

        if user:
            msg = "Desculpe, ja existe uma conta registrada com este email!"
            return render(request, 'login/index.html', {'msg': msg})