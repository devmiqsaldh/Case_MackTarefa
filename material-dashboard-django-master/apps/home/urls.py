# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.urls import include, path, re_path
from apps.home import views


urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    
    # nossos urls
    # path('', views.login_usuario, name="login"),
    # path('login', views.login_usuario, name="login"),
    # path("logout/", views.logout_usuario, name="logout"),
    
    path("home/", views.home, name="home"),
    path("cadastro_usuarios/", views.cadastro_usuarios, name="cadastro_usuarios"),
    
    path("cadastro_tarefa.html/", views.cadastro_tarefas, name="cadastro_tarefas"),
    
    path("cadastrar_tarefas/", views.cadastrar_tarefa, name="cadastrar_tarefa"),

    path("listagem_tarefas/", views.listagem_tarefas, name="listagem_tarefas"),
    
    path("editar_tarefas/<int:tarefa_id>/", views.editar_tarefa, name="editar_tarefa"),
    
    path("deletar_tarefa/<int:tarefa_id>/", views.deletar_tarefa, name="deletar_tarefa"),

      # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
