# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tarefa(models.Model):
    titulo = models.CharField(max_length=100)
    materia = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    prazo = models.DateField()
    status = models.CharField(max_length=100)
    usuario= models.ForeignKey(User, on_delete=models.CASCADE, default=1)
