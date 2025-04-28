from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import random
import pygame


# Create your views here.

def homepage(request):
    return render (request, 'home/index.html')

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']

            full_message = f"From: {name} <{email}>\n\n{message}"

            send_mail(
                subject="New Contact Form Submission",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect('home/contact.html') # replace with your success template
        except Exception as e:
            print("Mail error:", e)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return render(request, 'home/contact.html')

def services(request):
    return render(request, 'home/services.html')

def snake_game(request):
    return render(request, 'home/snake_game.html')

@csrf_exempt
def guess_game(request):
    if 'guess' not in request.session or 'remaining_guesses' not in request.session:
        # Start a new game
        request.session['guess'] = random.randint(1, 100)
        request.session['remaining_guesses'] = 5

    message = ''
    if request.method == 'POST':
        try:
            num = int(request.POST.get('guess'))
            correct_number = request.session['guess']
            remaining_guesses = request.session['remaining_guesses']

            if num == correct_number:
                message = "🎯 Correct guess! Well done!"
                del request.session['guess']
                del request.session['remaining_guesses']
            else:
                remaining_guesses -= 1
                request.session['remaining_guesses'] = remaining_guesses
                if remaining_guesses <= 0:
                    message = f"💥 Game over! The correct number was {correct_number}."
                    del request.session['guess']
                    del request.session['remaining_guesses']
                else:
                    hint = "Too low" if num < correct_number else "Too high"
                    message = f"{hint}! You have {remaining_guesses} guesses left."

        except ValueError:
            message = "Please enter a valid number."

    context = {'message': message}
    return render(request, 'home/guess_game.html', context)
