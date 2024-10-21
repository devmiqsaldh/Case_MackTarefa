# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Tarefa
from django.utils.dateparse import parse_datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout



@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        print("asssd")
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# nossas funções
@login_required(login_url="/login/")
def home(request):
    return render(request, "home/index.html")

@login_required(login_url="/login/")
def cadastro_usuarios(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return HttpResponse("As senhas não batem")
        email_repetido = User.objects.filter(email=email)
        if email_repetido:
            return HttpResponse("O email já esta cadastrado")
        if email and username and password1 and password2:
            user = User.objects.create_user(username=username, email=email, password=password1)
            print(f'Usuário {user.username} criado com sucesso!')  
            return redirect("login")

    return render(request, "home/cadastro_usuarios.html")

@login_required(login_url="/login/")
def cadastro_tarefas(request):
     return render(request, "home/cadastro_tarefas.html")

@login_required(login_url="/login/")
def cadastrar_tarefa(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        materia = request.POST.get('materia')
        descricao = request.POST.get('descricao')
        prazo = request.POST.get('prazo')
        status = request.POST.get('status')
        usuario = request.user
        Tarefa.objects.create(titulo= titulo, materia=materia, descricao=descricao, prazo=prazo, status=status, usuario=usuario)
        # tarefa.save()
        # print(tarefa)
        
        tarefas = {
            'tarefas': Tarefa.objects.filter(usuario=request.user)
        }
    
    return render(request, "home/listagem_tarefas.html", tarefas )

@login_required(login_url="/login/")
def listagem_tarefas(request):
    tarefasEncontradas = Tarefa.objects.filter(usuario=request.user)
    tarefas = {
            'tarefas': tarefasEncontradas
        }
    
    return render(request, "home/listagem_tarefas.html", tarefas )

@login_required(login_url="/login/")
def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        materia = request.POST.get('materia')
        descricao = request.POST.get('descricao')
        prazo = request.POST.get('prazo')
        status = request.POST.get('status')

        if titulo and materia and descricao and prazo and status:
            # prazo = parse_datetime(prazo)  # Converte a string de data e hora para um objeto datetime
            tarefa.titulo = titulo
            tarefa.materia = materia
            tarefa.descricao = descricao
            tarefa.prazo = prazo
            tarefa.status = status
            tarefa.save()
            return redirect("listagem_tarefas")
        else:
            return render(request, "home/editar_tarefas.html", {'tarefa': tarefa, 'error': 'Preencha todos os campos.'})

    return render(request, "home/editar_tarefas.html", {'tarefa': tarefa})

@login_required(login_url="/login/")
def deletar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    
    # if request.method == 'POST':
    tarefa.delete()
    return redirect("listagem_tarefas")
    
    # return render(request, "home/index.html", {'tarefa': tarefa})
# Exemplos 

def login_usuario(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        senha = request.POST.get('password')
        
        user = User.objects.filter(email=email).first()
        
        print (user.username)
        print (senha)
        user = authenticate(username=user.username, password=senha)
        print(user)
        if user:
            login(request, user)
            return redirect('home')
        return HttpResponse("usuário ou senha inválidos.")
    
        
def logout_usuario(request):
    logout(request)  # Faz logout do usuário
    # messages.success(request, "Você foi desconectado com sucesso!")  # Mensagem de sucesso
    return redirect('login')