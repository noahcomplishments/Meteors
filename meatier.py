"""
Noah Parent, Mark Schneider, Gianluca Cafueri
"Meteors"
Creating a video game based on 'Asteroids'
November 18th 2021
"""

import pygame, math, random, sys, os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
        self.x = x
        self.y = y
        self.angle = angle
        self.thrust = thrust
        self.radius = radius
        self.vel = [velocity[0], velocity[1]]

        self.settings = Settings()

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
        self.x = (self.x + self.vel[0]) % (self.settings.WIDTH - self.radius)
        self.y = (self.y + self.vel[1]) % (self.settings.HEIGHT - self.radius)

    def draw(self, screen):
        '''Draws the ship onto the screen'''
        screen.blit(rotate_center(self.image, self.angle), (self.x, self.y))


class Bullet():
    def __init__(self, ship_angle, x, y):

        self.bullet_speed = 20

        self.x = x
        self.y = y

        self.angle = ship_angle

        self.image = pygame.image.load('D:\Meteors\star.png')

    def update(self):

        self.x += self.bullet_speed * math.cos(self.angle * math.pi / 180)
        self.y -= self.bullet_speed * math.sin(self.angle * math.pi / 180)

    def draw(self, screen):
        '''Draws the ship onto the screen'''
        screen.blit(self.image, (self.x, self.y))

def gameLoop():

    pygame.init()

    settings = Settings()

    screen = pygame.display.set_mode([settings.WIDTH, settings.HEIGHT])
    pygame.display.set_caption("Meteors")
    
    player = Player('D:\Meteors\star.png', 100, 100, 0, (0, 0), False, 20)

    bullets = []

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 50)

    done = False

    while not done:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                sys.exit()

            #Set the rotation velocity / thrust based on the key pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.rotate_vel = 3
                elif event.key == pygame.K_RIGHT:
                    player.rotate_vel = -3
                elif event.key == pygame.K_UP:
                    player.thrust = True
                elif event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.angle, player.x, player.y))
                
            #Reset rotation velocity / stop thrust when key goes up
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.rotate_vel = 0
                elif event.key == pygame.K_RIGHT:
                    player.rotate_vel = 0
                elif event.key == pygame.K_UP:
                    player.thrust = False


        screen.fill(settings.BACKGROUND)

        player.update()

        for bullet in bullets:
            bullet.update()
            bullet.draw(screen)

        player.draw(screen)

        # FPS counter *** Note: this code must stay here, fps must be reassigned after each loop
        fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
        screen.blit(fps, (20, 20))

        pygame.display.flip()

        clock.tick(60)
        

class Settings:
    def __init__(self):
        self.WIDTH = 900
        self.HEIGHT = 900
        self.BACKGROUND = (100, 100, 100)

if __name__ == '__main__':
    gameLoop()
