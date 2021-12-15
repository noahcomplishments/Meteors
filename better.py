"""
Noah Parent, Mark Schneider, Gianluca Cafueri
"Meteors"
Creating a video game with inspiration from 'Asteroids'
November 18th 2021
"""

import pygame, math, random, sys, os

from pygame.event import get

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 900
HEIGHT = 900
BACKGROUND = (0, 0, 0)
ROTATE_SPEED = 4

player_radius = 17

def getMeteorSpeed():
    move = random.randint(1,2)

    if move == 1:
        return random.randint(1, 3)
    if move == 2:
        return random.randint(-3, -1)

def isColliding(center1, radius1, center2, radius2):
    """Checks for collision between two circular objects"""
    #Note: attempted to use sprites for collision, interfered with other functions

    # Calculates distance between center of object and second object
    dist1 = (center1[0]-center2[0])**2+(center1[1]-center2[1])**2 
    # Calculates radius of object 1
    dist2 = (radius1 + radius2)**2

    if dist1 <= dist2:
        return True
    else:
        return False 

def angle_to_vector(ang):
    '''Given the angle of rotation of the ship, return the vector in the form [x, y]'''
    return [math.cos(ang), -math.sin(ang)]

def rotate_center(image, angle):
    """Rotate a Surface, maintaining position"""
    # Get rect of original image
    orig_rect = image.get_rect()
    # Rotate the image
    rot_image = pygame.transform.rotate(image, angle)
    # Make a copy of the original image
    rot_rect = orig_rect.copy()
    # Set the center of the rotated image equal to the center of the original rect
    rot_rect.center = rot_image.get_rect().center
    # Subsurface places original image onto rotated image 
    rot_image = rot_image.subsurface(rot_rect).copy()
    # Returns rotated image about center point
    return rot_image

class Player:
    '''This class represents the player'''
    def __init__(self, image, x, y, angle, velocity, thrust, radius):

        # Loads image of ship
        self.image = pygame.image.load(image)
        
        # Sets all variables from given values
        self.radius = radius
        self.x = x
        self.y = y
        self.center = [(self.x + self.radius), (self.y + self.radius)]
        self.angle = angle
        self.thrust = thrust
        self.vel = [velocity[0], velocity[1]]
        
        self.lives = 3

        # Sets intial rotation speed to 
        self.rotate_vel = 0

    def update(self):
        '''Find a new position for the player'''

        acc = 0.25
        fric = acc / 10
        
        self.angle += self.rotate_vel

        self.forward = angle_to_vector(math.radians(self.angle))

        if self.thrust:
            self.vel[0] += self.forward[0] * acc
            self.vel[1] += self.forward[1] * acc

        self.vel[0] *= (1 - fric)
        self.vel[1] *= (1 - fric)

        # update position
        self.x = (self.x + self.vel[0]) % (WIDTH - self.radius)
        self.y = (self.y + self.vel[1]) % (HEIGHT - self.radius)

        # Updates center position *** Must be within update loop to track movement ***
        self.center = [(self.x + self.radius), (self.y + self.radius)]

    def draw(self, screen):
        '''Draws the ship onto the screen'''
        screen.blit(rotate_center(self.image, self.angle), (self.x, self.y))


class Meteor():
    def __init__(self, screen, x, y, vel_x, vel_y, size):
        """This class represents a meteor"""
        self.size = size
        if self.size == "L":
            self.radius = 20
        if self.size == "M":
            self.radius = 10
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.center = [self.x, self.y]
        self.screen = screen

    def update(self):
        self.x = ((self.x + self.vel_x) % (WIDTH + 40))
        self.y = ((self.y + self.vel_y) % (HEIGHT + 40))

        self.center = [self.x, self.y]

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.radius)

class Bullet():
    '''This class represents a bullet'''
    def __init__(self, ship_angle, x, y):

        self.bullet_speed = 20

        self.x = x
        self.y = y

        self.radius = 13
        
        self.angle = ship_angle

        self.image = pygame.image.load('T:/Asteroids/Asteroids/shot4.png')

    def update(self):
        '''Finds new position for bullet'''
        self.x += self.bullet_speed * math.cos(self.angle * math.pi / 180) 
        self.y -= self.bullet_speed * math.sin(self.angle * math.pi / 180)

        self.center = [(self.x + self.radius), (self.y + self.radius)]

    def draw(self, screen):
        '''Draws the bullet onto the screen'''
        screen.blit(self.image, (self.x, self.y))


def gameLoop():
    '''The Main Game Loop'''
    pygame.init()

    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Meteors")

    bullets = []
    tests = []
    meteors = []
    
    player = Player('T:/Asteroids/Asteroids/ship3.png', WIDTH / 2, HEIGHT / 2, 0, (0, 0), False, player_radius)


    for i in range(10):
        
        meteor = Meteor(screen, random.randint(40, WIDTH - 40), random.randint(40, WIDTH - 40), getMeteorSpeed(), getMeteorSpeed(), "L")
        meteors.append(meteor)

    #random.randint(-3, 3), random.randint(-3, 3)

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 50)
    glow = pygame.image.load("T:/Asteroids/Asteroids/glow2.png")

    done = False

    frame_count = 0
    frame_rate = 60
    immunetime = 0

    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                sys.exit()

            #Set the rotation velocity / thrust based on the key pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.rotate_vel = -ROTATE_SPEED
                if event.key == pygame.K_UP:
                    player.thrust = True
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.angle, player.x, player.y))
                if event.key == pygame.K_LEFT:
                    player.rotate_vel = ROTATE_SPEED
                
            #Reset rotation velocity / stop thrust when key goes up
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.rotate_vel = 0
                elif event.key == pygame.K_RIGHT:
                    player.rotate_vel = 0
                elif event.key == pygame.K_UP:
                    player.thrust = False

        screen.fill(BACKGROUND)

        player.update()

        immunetime += 1

        if immunetime / 60 < 5:
            screen.blit(glow, (player.x - 20, player.y - 20))

        for bullet in bullets:
            bullet.update()
            for test in tests:
                if isColliding(bullet.center, bullet.radius, test.center, test.radius) == True:
                    print("hit")
                    bullets.remove(bullet)
            bullet.draw(screen)
        
        for meteor in meteors:
            meteor.update()
            for bullet in bullets:
                if isColliding(bullet.center, bullet.radius, meteor.center, meteor.radius) == True:
                    print("hit")
                    bullets.remove(bullet)
                    if meteor.size == "L":
                        for i in range(2):
                            newmeteors = Meteor(screen, meteor.center[0], meteor.center[1], getMeteorSpeed(), getMeteorSpeed(), "M")
                            meteors.append(newmeteors)
                    meteors.remove(meteor)
                bullet.draw(screen)
            meteor.draw(screen)
        player.draw(screen)

        for meteor in meteors:
            if isColliding(player.center, player.radius, meteor.center, meteor.radius) == True:
                if immunetime / 60 > 5:
                    if meteor.size == "L":
                        for i in range(2):
                            newmeteors = Meteor(screen,meteor.center[0], meteor.center[1], getMeteorSpeed(), getMeteorSpeed(), "M")
                            meteors.append(newmeteors)
                    meteors.remove(meteor)
                    pygame.draw.circle(screen, RED, (HEIGHT-50, WIDTH-50), 30)
                    player.lives -= 1
                    player.x = WIDTH / 2
                    player.y = HEIGHT / 2
                    player.vel = [0, 0]
                    immunetime = 0
                    if player.lives == 0:
                        print("Game Over!")
                        done = True
                    
            meteor.draw(screen)
        player.draw(screen)


        if len(meteors) == 0:
            for i in range(10):
                immunetime = 0
                meteor = Meteor(screen,random.randint(50, WIDTH-50), random.randint(50, WIDTH-50), getMeteorSpeed(), getMeteorSpeed(), "L")
                meteors.append(meteor)

        # FPS counter *** Note: this code must stay here, fps must be reassigned after each loop
        fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
        screen.blit(fps, (20, 20))

        # --- Timer going up ---
    
        # Calculate total seconds
        total_seconds = frame_count // frame_rate
    
        # Divide by 60 to get total minutes
        minutes = total_seconds // 60
    
        # Use modulus (remainder) to get seconds
        seconds = total_seconds % 60
    
        # Use python string formatting to format in leading zeros
        output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
    
        # Blit to the screen
        text = font.render(output_string, True, WHITE)
        screen.blit(text, [WIDTH - 200, 20])

        # Add to frame count every loop for timer
        frame_count += 1

        pygame.display.flip()

        clock.tick(60)

if __name__ == '__main__':
    gameLoop()

