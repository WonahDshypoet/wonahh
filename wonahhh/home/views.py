from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def homepage(request):
    return render(request, 'home/index.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST('name')
        email = request.POST('email')
        message = request.POST('message')

        full_message = f"From: {name} <{email}>\n\n{message}"

        send_mail(
            subject="New Contact Form Submission",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )
        return redirect('Thank you for contacting me. I would reply you very shortly.')
 
    return render(request, 'home/contact.html')

def services(request):
    return render(request, 'home/services.html')

def snake_game(request):
    return render(request, 'home/snake_game.html')
