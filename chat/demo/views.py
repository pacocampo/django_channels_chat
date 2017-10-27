from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room
# Create your views here.

@login_required
def index(request):
    '''obtenemos y regresamos a index.html todas las salas de chat disponibles'''
    rooms = Room.objects.all()
    return render(request, 'index.html', {'rooms':rooms})