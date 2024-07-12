#import and initialize pygame
import pygame
from pygame import mixer
import math
import random

mixer.init()
pygame.init()

#set the width and height of screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

#create the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Planet Defence')

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define variables
moving_forward = False
turning_left = False
turning_right = False
shoot = False
start_game = False
end_game = False
start_time = 0
start_intro = False

#load music
def play_song(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1, 0.0, 3000)

play_song('audio/ThemeSong.mp3')

#load images
main_menu_img = pygame.image.load('img/MainMenu.png').convert_alpha()
stars_img = pygame.image.load('img/Stars.png').convert_alpha()
laser_img = pygame.image.load('img/laser.png').convert_alpha()
health_pickup_img = pygame.image.load('img/HealthPickup.png').convert_alpha()
ammo_pickup_img = pygame.image.load('img/AmmoPickup.png').convert_alpha()
item_pickups = {'Health':health_pickup_img, 'Ammo':ammo_pickup_img}

#define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (235, 65, 54)
#define font
font = pygame.font.SysFont('Futura', 25)
large_font = pygame.font.SysFont('Futura', 60)



#draws text on screen
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))
#draws the background
def draw_bg():
    screen.fill(BLACK)
    screen.blit(stars_img, (0,0))
def draw_main_menu():
    screen.fill(BLACK)
    img = main_menu_img
    img = pygame.transform.scale(img, (img.get_width() * .245, img.get_height() * .245))
    screen.blit(img, (0,0))

#create the asteroids
def spawn_asteroids():
    screen_edges = ['top', 'bottom', 'left', 'right']
    spawn_position = random.choice(screen_edges)
    if spawn_position == 'top':
        x = random.randint(0, SCREEN_WIDTH)
        y = 0
    if spawn_position == 'bottom':
        x = random.randint(0, SCREEN_WIDTH)
        y = SCREEN_HEIGHT
    if spawn_position == 'left':
        x = 0
        y = random.randint(0, SCREEN_HEIGHT)
    if spawn_position == 'right':
        x = SCREEN_WIDTH
        y = random.randint(0, SCREEN_HEIGHT)
    asteroid = Asteroid(x, y, .1)
    asteroids_group.add(asteroid)

#reset game
def reset_game():
    # Reset player
    player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20)
    player.alive = True
    player.ammo = player.starting_ammo
    player.angle = 0
    # Reset planet
    planet.health = 100
    planet.alive = True
    # Clear sprite groups
    asteroids_group.empty()
    laser_group.empty()
    item_pickups_group.empty()
    # Reset game state variables
    global start_game, end_game, start_time
    start_game = False
    end_game = False
    start_time = 0






#Player object
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.angle = 0
        self.shoot_cooldown = 0
        self.starting_ammo = ammo
        self.ammo = ammo
        img = pygame.image.load('img/player.png').convert_alpha()
        self.original_image = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if planet.health == 0:
            self.alive = False

    def move(self, moving_forward, turning_left, turning_right):
        #reset movement variables
        dx = 0
        dy = 0
        #assign movement variables
        if moving_forward:
            rad_angle = math.radians(self.angle)
            dx = -self.speed * math.sin(rad_angle)
            dy = -self.speed * math.cos(rad_angle)
            self.rect.x += dx
            self.rect.y += dy
        if turning_left:
            self.angle += 5
        if turning_right:
            self.angle -= 5

        # Rotate the image and update the rect
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

    def draw(self):
        screen.blit(self.image, self.rect)

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 15
            laser_x_pos = self.rect.centerx + self.rect.width * 0.5 * -math.sin(math.radians(self.angle))
            laser_y_pos = self.rect.centery + self.rect.height * 0.5 * -math.cos(math.radians(self.angle))
            laser = Laser(laser_x_pos, laser_y_pos, self.angle)
            laser_group.add(laser)
            self.ammo -= 1





#Planet object
class Planet(pygame.sprite.Sprite):
    def __init__(self, scale):
        self.alive = True
        self.health = 100
        self.max_health = 100
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/planet.png').convert_alpha()
        self.image = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            player.alive = False
            self.kill()

    def draw(self):
        screen.blit(self.image, self.rect)






#Asteroid object
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        self.alive = True
        self.health = 100
        self.max_health = 100
        self.speed = 1
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/asteroid.png').convert_alpha()
        self.image = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def ai(self):
        if self.alive and planet.alive:
            #get distance to the middle of the screen
            center_screen_x = screen.get_width() / 2
            center_screen_y = screen.get_height() / 2
            direction_x = center_screen_x - self.rect.centerx
            direction_y = center_screen_y - self.rect.centery
            distance_to_center = (direction_x ** 2 + direction_y ** 2) ** 0.5
            if distance_to_center != 0:
                direction_x /= distance_to_center
                direction_y /= distance_to_center
            #update the movement
            self.rect.x += direction_x * self.speed
            self.rect.y += direction_y * self.speed

    def update(self):
        self.check_alive()
        self.ai()
        #check collisions with characters
        if pygame.sprite.spritecollide(planet, asteroids_group, False):
            for asteroid in pygame.sprite.spritecollide(planet, asteroids_group, False):
                if asteroid.alive:
                    asteroid.health -= 100
                    self.kill()
                    planet.health -= 25

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.kill()
            #Create item pickups
            item_type = random.randint(1,2)
            if item_type == 1:
                item_pickup = ItemPickups('Ammo', self.rect.centerx, self.rect.centery)
                item_pickups_group.add(item_pickup)
            elif item_type == 2:
                item_pickup = ItemPickups('Health', self.rect.centerx, self.rect.centery)
                item_pickups_group.add(item_pickup)

    def draw(self):
        screen.blit(self.image, self.rect)
   



#Screen Fade object
class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 2: #vertical screen fade down
            pygame.draw.rect(screen, self.color, (0,0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True
        return fade_complete


#create screen fade
death_fade = ScreenFade(2, PINK, 4)





#Laser object
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 2
        self.original_image = pygame.transform.scale(laser_img, (laser_img.get_width() * .005, laser_img.get_height() * .005))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = angle
        rad_angle = math.radians(self.angle)
        self.dx = -self.speed * math.sin(rad_angle)
        self.dy = -self.speed * math.cos(rad_angle)

    def update(self):
        self.rect.x += (self.dx * self.speed)
        self.rect.y += (self.dy * self.speed)
        # Rotate the image and update the rect
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
        #check collisions with characters
        collisions =  pygame.sprite.spritecollide(self, asteroids_group, False)
        for asteroid in collisions:
            asteroid.health -= 25
            self.kill()





#item object
class ItemPickups(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_pickups[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        #check for collisions w/ player
        if pygame.sprite.collide_rect(self, player):
            #check what kind of item was picked up
            if self.item_type == 'Ammo':
                player.ammo += 10
            elif self.item_type == 'Health':
                planet.health += 25
                if planet.health > planet.max_health:
                    planet.health = planet.max_health

            #delete the item
            self.kill()

    def draw(self):
        screen.blit(self.image, self.rect)




#HealthBar object
class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        #update w/ new health
        self.health = health
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen, WHITE, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * health_percentage, 20))
    


#create sprite groups
laser_group = pygame.sprite.Group()
item_pickups_group = pygame.sprite.Group()
asteroids_group = pygame.sprite.Group()


#create objects
player = Spaceship(screen.get_width()/2, screen.get_height()/2 - 20, .1, 2, 20)
planet = Planet(.5)
health_bar = HealthBar(90, 10, planet.health, planet.health)

#create gameplay loop
running = True

while running:

    clock.tick(FPS)

    if not start_game and not end_game:
        #draw menu
        draw_main_menu()
    if end_game:
        if death_fade.fade():
            draw_text('You Died!', large_font, WHITE, SCREEN_WIDTH/2-100, 90)
            draw_text(f'You Survived: {time_survived:.2f} Seconds', large_font, WHITE, SCREEN_WIDTH/2-300, SCREEN_HEIGHT/2-20)
            draw_text('Press \'M\' To Go Back To Main Menu', large_font, WHITE, SCREEN_WIDTH/2 - 350, SCREEN_HEIGHT-80)
    elif start_game:
        draw_bg()

        #Display Stats
        draw_text('HEALTH: ', font, WHITE, 10, 12.5)
        health_bar.draw(planet.health)
        draw_text('AMMO: ', font, WHITE, 10, 35)
        time_survived = (pygame.time.get_ticks() - start_time) / 1000
        draw_text(f'Time Survived: {time_survived:.2f} Seconds', font, WHITE, 10, 60)
        for laser in range(player.ammo):
            img = pygame.transform.scale(laser_img, (laser_img.get_width() * .005, laser_img.get_height() * .005))
            img = pygame.transform.rotate(img, 90)
            screen.blit(img, (80 + (laser * 8), 34))

        #show player
        player.update()
        planet.draw()
        player.draw()

        if len(asteroids_group) < 2 and player.alive:
            spawn_asteroids()
        for asteroid in asteroids_group:    
            asteroid.update()
            asteroid.draw()
        

        laser_group.update()
        item_pickups_group.update()
        laser_group.draw(screen)
        item_pickups_group.draw(screen)

        #handle actions for player
        if player.alive:
            if shoot:
                player.shoot()
            player.move(moving_forward, turning_left, turning_right)
        else:
            end_game = True

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            running = False

        #handles key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                moving_forward = True
            if event.key == pygame.K_LEFT:
                turning_left = True
            if event.key == pygame.K_RIGHT:
                turning_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_RETURN:
                start_game = True
                start_time = pygame.time.get_ticks()
            if event.key == pygame.K_m:
                end_game = False
                start_game = False
                death_fade.fade_counter = 0
                reset_game()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                moving_forward = False
            if event.key == pygame.K_LEFT:
                turning_left = False
            if event.key == pygame.K_RIGHT:
                turning_right = False
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                shoot = False

    pygame.display.update()

pygame.quit()