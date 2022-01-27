"By Noah Parent"

import pygame, math
import vector as v
import rotate as r
pygame.init()

WIDTH = 900
HEIGHT = 900


class Player:
    '''This class represents the player'''
    def __init__(self, image, x, y, angle, velocity, thrust, radius):

        # Loads image of ship
        self.image = pygame.image.load(image)

        # Loads image of hearts
        self.heartImage = pygame.image.load('heart.png')

        # Sets all variables from given values
        self.radius = radius
        self.x = x
        self.y = y
        self.center = [(self.x + self.radius), (self.y + self.radius)]
        self.angle = angle
        self.thrust = thrust
        self.vel = [velocity[0], velocity[1]]

        # Sets intial rotation speed to
        self.rotate_vel = 0
        
    def update(self):
        '''Find a new position for the player'''

        acc = 0.25
        fric = acc / 10

        self.angle += self.rotate_vel

        self.forward = v.angle_to_vector(math.radians(self.angle))

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
        screen.blit(r.rotate_center(self.image, self.angle), (self.x, self.y))