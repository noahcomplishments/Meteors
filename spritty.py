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

class Player(pygame.sprite.Sprite):
    '''This class represents the player'''
    def __init__(self, image, position, angle, velocity, thrust, radius):

        super().__init__()

        # Loads image of ship
        self.image = pygame.image.load(image)

        self.rect = self.image.get_rect()
        
        # Sets all variables from given values
        self.rect.x = position[0] 
        self.rect.y = position[1]
        self.angle = angle
        self.thrust = thrust
        self.radius = radius
        self.vel = [velocity[0], velocity[1]]

        self.settings = Settings()

        # Sets intial rotation speed to 
        self.rotate_vel = 0

    def update(self):

        '''Find a new position for the player'''

        acc = 0.3
        fric = acc / 20
        
        self.angle += self.rotate_vel

        self.forward = angle_to_vector(math.radians(self.angle))

        if self.thrust:
            self.vel[0] += self.forward[0] * acc
            self.vel[1] += self.forward[1] * acc

        self.vel[0] *= (1 - fric)
        self.vel[1] *= (1 - fric)

        # update position
        self.rect.x = (self.rect.x + self.vel[0]) % (self.settings.WIDTH - self.radius)
        self.rect.y = (self.rect.y + self.vel[1]) % (self.settings.HEIGHT - self.radius)

    def draw(self, screen):
        '''Draws the ship onto the screen'''
        screen.blit(rotate_center(self.image, self.angle), (self.rect.x, self.rect.y))

    def shoot(self):
        print("pew pew")
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, ship_vel):

        super().__init__()

        self.bullet_vel = 0

        # Velocity of ship when bullet is fired
        self.ship_vel = [ship_vel[0], ship_vel[1]]

        self.image = pygame.surface(BLACK, (5, 5))

class Game:
    def __init__(self):

        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode([self.settings.WIDTH, self.settings.HEIGHT])
        pygame.display.set_caption("Meteors")
        
        self.player = Player('D:\Meteors\star.png', (100, 100), 0, (0, 0), False, 20)
    
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 50)
        

    def run_game(self):

        while True:
            self._check_events()
            self._update_screen()
            
    def _check_events(self):

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                sys.exit()

            #Set the rotation velocity / thrust based on the key pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.rotate_vel = 3
                elif event.key == pygame.K_RIGHT:
                    self.player.rotate_vel = -3
                elif event.key == pygame.K_UP:
                    self.player.thrust = True
                elif event.key == pygame.K_SPACE:
                    self.player.shoot()
                
    
            #Reset rotation velocity / stop thrust when key goes up
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.rotate_vel = 0
                elif event.key == pygame.K_RIGHT:
                    self.player.rotate_vel = 0
                elif event.key == pygame.K_UP:
                    self.player.thrust = False

    def _update_screen(self):

        self.screen.fill(self.settings.BACKGROUND)

        self.player.update()
    
        self.player.draw(self.screen)

        # FPS counter *** Note: this code must stay here, fps must be reassigned after each loop
        fps = self.font.render(str(int(self.clock.get_fps())), True, pygame.Color('white'))
        self.screen.blit(fps, (20, 20))

        pygame.display.flip()

        self.clock.tick(60)
        
        

class Settings:
    def __init__(self):
        self.WIDTH = 900
        self.HEIGHT = 900
        self.BACKGROUND = (100, 100, 100)

if __name__ == '__main__':
    game = Game()
    game.run_game()