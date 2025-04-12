from django.shortcuts import render


# Create your views here.

def homepage(request):
    return render(request, 'home/index.html')

def contact(request):
    return render(request, 'home/contact.html')

def services(request):
    return render(request, 'home/services.html')

def snake_game(request):
    return render(request, 'home/snake_game.html')
