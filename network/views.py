from django.shortcuts import render
from django.http import HttpResponse

def health(request):
    return HttpResponse("OK: Django 5.x on Python 3.11.x")