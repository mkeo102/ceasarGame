# Example file showing a circle moving on screen
import pygame

import random as rand

import pygame.freetype

import imgCache as cache


# Game modes

STARTING = 0
PLAYING = 1
DEAD = 2

# pygame setup
pygame.init()
pygame.font.init()
pygame.mixer.init()





screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
global dt
dt = 0
global score
score = 0

targetFrames = 0

MOVE_SPEED = 500

enemies = []




mode = STARTING

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 50)

ceasar_sprite       = pygame.transform.scale(cache.get_ceasar_image(pygame), (80,80))  #pygame.transform.scale(pygame.image.load(os.path.join('resources/sprites', 'ceasar.png')), (80,80))
rock_sprite         = pygame.transform.scale(cache.get_rock_image(pygame), (80,80))  #pygame.transform.scale(pygame.image.load(os.path.join('resources/sprites', 'rock-blurred.png')), (80,80))
background_image    = pygame.transform.scale(cache.get_background_image(pygame), (screen.get_width(), screen.get_height()))  #pygame.transform.scale(pygame.image.load(os.path.join('resources/backgrounds', 'background.jpg')), (screen.get_width(), screen.get_height()))

death_sound =  cache.get_death_noise(pygame) #pygame.mixer.Sound("./resources/sounds/death_Sound.mp3")


font = pygame.font.SysFont('Arial', 30)

played_death_sound = False
pygame.display.set_icon(ceasar_sprite)


def runMainMenu() :
    global mode 
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        mode = PLAYING
        return
    
    start_text = font.render("Press <space> to start!", False, (255,255,255))
    text_size = font.size("Press <space> to start!")
    screen.blit(start_text, ((screen.get_width() / 2) - text_size[0]/2, screen.get_height() / 2 - 15))
        

def runMainGame():
    global score, mode
    if len(enemies) < 10: 
        enemies.append(pygame.Vector2(rand.randint(50,screen.get_width() - 50), rand.randint(-50,5)))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos.x -= MOVE_SPEED * dt
    if keys[pygame.K_d]:
        player_pos.x += MOVE_SPEED * dt
        
    if player_pos.x <= 40:
        player_pos.x = 40
        
    if player_pos.x >= screen.get_width() - 40:
        player_pos.x = screen.get_width() - 40
        
    
    for enemy in enemies:
        enemy.y += (MOVE_SPEED ) * dt
        
        if enemy.y > screen.get_height() + 5:
            enemy.x = rand.randint(40,screen.get_width() - 40)
            enemy.y = 0
            score += 1
        
        if(player_pos.distance_to(enemy) <= 40): 
            mode = DEAD
            return 
        
        screen.blit(rock_sprite,(enemy.x - 40 ,enemy.y - 40))
        
    screen.blit(ceasar_sprite,(player_pos.x - 40 ,player_pos.y - 40))
        
    score_text = font.render(f"Score : {score}", False, (255,255,255))
    screen.blit(score_text, (10,10))

def runDeathScreen():
    global mode, score, enemies, player_pos, played_death_sound
    
    if not played_death_sound:
        played_death_sound = True
        death_sound.play()
        
    

    death_text = font.render("You Died!", False, (255,0,0))
    text_size = font.size("You Died!")
    screen.blit(death_text, ((screen.get_width() / 2) - text_size[0]/2, screen.get_height() / 2 - 15))
    
    
    death_text = font.render("Press <space> to replay!", False, (255,0,0))
    text_size = font.size("Press <space> to replay!")
    screen.blit(death_text, ((screen.get_width() / 2) - text_size[0]/2, screen.get_height() / 2 + 15))


    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        mode = PLAYING
        score = 0
        enemies = []
        player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 50)
        return

























while running:    
    
    if not pygame.mixer.get_busy() and not mode == DEAD:
        played_death_sound = False
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    screen.blit(background_image,(0,0))
    
    match mode:
        case 0: # STARTING
            runMainMenu() 
        case 1: # PLAYING
            runMainGame()
        case 2: # DEAD
            runDeathScreen()
#    
#    
#    if len(enemies) < 10: 
#        enemies.append(pygame.Vector2(rand.randint(50,screen.get_width() - 50), rand.randint(-50,5)))
#
#    keys = pygame.key.get_pressed()
#    if keys[pygame.K_a]:
#        player_pos.x -= MOVE_SPEED * dt
#    if keys[pygame.K_d]:
#        player_pos.x += MOVE_SPEED * dt
#        
#    if player_pos.x <= 40:
#        player_pos.x = 40
#        
#    if player_pos.x >= screen.get_width() - 40:
#        player_pos.x = screen.get_width() - 40
#        
#    
#    for enemy in enemies:
#        enemy.y += (MOVE_SPEED ) * dt
#        
#        if enemy.y > screen.get_height() + 5:
#            enemy.x = rand.randint(40,screen.get_width() - 40)
#            enemy.y = 0
#            score += 1
#        
#        if(player_pos.distance_to(enemy) <= 40): 
#            exit(0)
#        screen.blit(rock_sprite,(enemy.x - 40 ,enemy.y - 40))
            
        
    score_text = font.render(f"Score : {score}", False, (255,255,255))
    screen.blit(score_text, (10,10))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


pygame.mixer.stop()

pygame.quit()