import pygame
import random
import os

pygame.init()

#colors
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)

screen_height = 500
screen_width = 1000

window= pygame.display.set_mode((screen_width,screen_height))

#background image 
bgimg=pygame.image.load("D:\Python\snakeGame.py\snake_bg.png")
# making it equal to screen size
bgimg=pygame.transform.scale(bgimg, (screen_width,screen_height)).convert_alpha()
#convert alpha makes sure it doesnt affects game speed

pygame.display.set_caption("Snake and Apple")

pygame.display.update() #allows to update portion of screen, instead of entire area 

def plot_snake(window,color,snk_list,snake_size):
    for x, y in snk_list:
        pygame.draw.rect(window, black, [x,y, snake_size, snake_size])

clock = pygame.time.Clock()  #create an object to help track time and manage fps

font=pygame.font.SysFont(None, 50)  #default font
def text_screen(text, color, x, y):
    score_screen=font.render(text, True, color) 
    window.blit(score_screen,[x,y]) #blit means “a logical operation in which a block of data is rapidly moved or copied in memory”

def welcome():
    exit_game=False
    while not exit_game:
        window.fill("#FFB7CE")
        text_screen("SNAKE AND APPLE", black, 300,180)
        text_screen("PLEASE PRESS ENTER TO PLAY", black, 190,220)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    game_loop()

        pygame.display.update()
        clock.tick(60)

def game_loop():
    #game specific variable
    exit_game=False
    game_over=False
    snake_x=30
    snake_y=0
    snake_size=20
    fps = 60 #frames(or images displayed) per second; higher FPS smoother and more engaging gameplay
    velocity_x = 0
    velocity_y =0
    init_velocity=5

    #check if text file not present
    if (not os.path.exists("D:\Python\snakeGame.py\highscore.txt")):
        with open("D:\Python\snakeGame.py\highscore.txt", "w") as f:
            f.write("0")

    # r is read mode
    with open("D:\Python\snakeGame.py\highscore.txt", "r") as f:  
        highscore=f.read()

    food_x = random.randint(10, int(screen_width/2))
    food_y = random.randint(5, int(screen_height/2))
    score = 0
    
    snk_length=1
    snk_list=[]   # list of list i.e head list is appended in here

    while not exit_game:
        if game_over :
            with open("D:\Python\snakeGame.py\highscore.txt", "w") as f:
                f.write(str(highscore))
            window.fill(white)
            text_screen("Game Over! Press Enter To Continue", red,200,200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                # after press enter this will restart game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True    

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT: #for moving snake in x direction
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_DOWN:  #for moving snake in y direction
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_LEFT: #for moving snake in x direction
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP: #for moving snake in x direction
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 5
            #for snake to move
            snake_x  += velocity_x     
            snake_y += velocity_y

            if abs(snake_x-food_x)<10 and abs(snake_y-food_y)<10:
                score+=10
                food_x = random.randint(20, int(screen_width/2))
                food_y = random.randint(20, int(screen_height/2))
                snk_length += 3    
                if score>int(highscore):
                    highscore=score

            window.fill(white)
            window.blit(bgimg, (0,0))

            text_screen("Score: "+str(score),red,2,2)
 # didnt add in same line def text_screen mein 4 parameters onli jisme first is text
            text_screen("HighScore: "+str(highscore),red,200,2)
            pygame.draw.rect(window, red, [food_x, food_y, snake_size, snake_size])

 #pygame.draw.rect(window, black, [snake_x, snake_y, snake_size, snake_size])
            plot_snake(window,black,snk_list,snake_size)

            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]
#Snakes head is the last coordinate of list; snake’s head and snake’s any other body part is on the same co-ordinate means collision occurs so game over!
            if head in snk_list[:-1]:
                 game_over=True

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over=True

        pygame.display.update()  #ye krna padta to update upar wali line ke baad
        clock.tick(fps)  #tick claculate time passed in ms

    pygame.quit()
    quit()

welcome()
