from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


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
