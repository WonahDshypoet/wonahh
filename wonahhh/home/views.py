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
    
    pygame.init() # pygame initialization and setup

    # Colors needed in game

    white = (255, 255, 255)
    yellow = (255, 255, 102)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)

    # Screen size and game caption declaration

    width = 600
    height = 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Snake Game 🐍')

    # Time and block of snake for the food and speed of game

    clock = pygame.time.Clock()
    snake_block = 10
    snake_speed = 15

    # fonts used in game 
    
    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)

    # Functions used in Our Game include:

    '''
    - Score func.: used to record the score and prepare it to be rendered.
    
    - Snake func.: used to create the snake, it increases the length as well.
    
    - Message func.: used to display the messages in the game.
    
    - Gameloop func.: used for the game logic. follow code to understand in depth.
    '''
        
    def score(value):
        value = score_font.render("Score: " + str(value), True, yellow)
        screen.blit(value, [0, 0])
        
    def snake(snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block])

    def message(msg, color):
        mesg = font_style.render(msg, True, color)
        screen.blit(mesg, [width / 6, height / 3])

    def gameLoop():
        game_over = False 
        game_close = False

        # Coordinate of snake head, should be at the middle of the screen
        
        x = width / 2
        y = height / 2

        # Movements of the snake, it wouldn't move till an arrow is hit because it is positioned at 0
        
        dx = 0
        dy = 0

        # The snake is a list that will be added to as it eats more food (pixels), it is currently set to just one block
        
        snake_list = []
        length = 1
        score_value = 0

        # The random grid aligned location for the food
        
        foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
        
        while not game_over:

            while game_close:
                screen.fill(blue)
                message("You lost! Press Q-Quit or C-Play Again", red)
                score(length - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            gameLoop()

            # Observe the x and y, that's where the direction really happens, ooh observe the signs as well, don't forget your geometry 
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        dx = -snake_block
                        dy = 0
                    elif event.key == pygame.K_RIGHT:
                        dx = snake_block
                        dy = 0
                    elif event.key == pygame.K_UP:
                        dy = -snake_block
                        dx = 0
                    elif event.key == pygame.K_DOWN:
                        dy = snake_block
                        dx = 0

            if x >= width or x < 0 or y >= height or y < 0: # logic to end game if snake hits wall by growing to large 
                game_close = True
            x += dx
            y += dy
            screen.fill(blue)
            pygame.draw.rect(screen, green, [foodx, foody, snake_block, snake_block]) # Playground creation
            snake_head = []
            
            # Snake increase after eating
            
            snake_head.append(x)
            snake_head.append(y)
            snake_list.append(snake_head)
            if len(snake_list) > length:
                del snake_list[0]
            
            # Logic to handle collision and show scores 
            
            for block in snake_list[:-1]:
                if block == snake_head:
                    game_close = True
            snake(snake_block, snake_list)
            score(score_value)
            pygame.display.update()
            
            if x == foodx and y == foody:
                foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
                length += 1
                score_value += 5

            clock.tick(snake_speed)

        pygame.quit()
        quit()

    gameLoop()
    return render(request, 'home/snake_game.html')

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
