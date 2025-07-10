# core/models.py

from django.db import models

class User(models.Model):
    HOBBY = 'HOBBY'
    PRO = 'PRO'
    PLAN_CHOICES = [(HOBBY, 'Hobby'), (PRO, 'Pro')]

    id = models.CharField(primary_key=True, max_length=32)
    username = models.CharField(max_length=100)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES)

class DeployedApp(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apps')
    active = models.BooleanField(default=True)
