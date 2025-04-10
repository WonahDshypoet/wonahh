from django.shortcuts import render


# Create your views here.

def homepage(request):
    return render(request, 'home/index.html')

def style(request):
    return render(request, 'home/style.css')

def contact(request):
    return render(request, 'home/contact.html')

def services(request):
    return render(request, 'home/services.html')

def meeeeee(request):
    return render(request, 'home/meeeeee.jpg')

def download(request):
    return render(request, 'home/download.jpg')

def snake_game(request):
    return render(request, 'home/Snake_game.py')