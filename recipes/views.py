from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'recipes/home.html')  # Implementação da view


def sobre(request):
    return HttpResponse('SOBRE')  # Implementação da view


def contato(request):
    return HttpResponse('CONTATO')  # Implementação da view