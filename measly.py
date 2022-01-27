"""
Noah Parent, Mark Schneider, Gianluca Cafueri
"Meteors"
Creating a video game with inspiration from 'Asteroids'
November 18th 2021
"""

import pygame, math, random, sys
import player as pl
import rotate as rt
import vector as vc

# CONSTANTS #

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
instructionsValue = 0

# Create variable to hold score
playerScore = 0

# Create a variable to hold current screen
currentScreen = 0

# Create a variable to hold game difficulty
gameDifficulty = 1

# Make a variable to hold the value of the current selection on the menu screen

currentMenuSelection = 1

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

class Meteor():
    def __init__(self, screen, x, y, vel_x, vel_y, size):
        """This class represents a meteor"""
        self.size = size
        if self.size == "L":
            self.radius = 40
            self.image = pygame.image.load('largerasteroid.png')
        if self.size == "M":
            self.radius = 20
            self.image = pygame.image.load('largeasteroid.png')
        if self.size == "S":
            self.radius = 10
            self.image = pygame.image.load('mediumasteroid.png')

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
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))

class Bullet():
    '''This class represents a bullet'''
    def __init__(self, ship_angle, x, y):

        self.bullet_speed = 20

        self.x = x
        self.y = y

        self.radius = 13

        self.angle = ship_angle

        self.image = pygame.image.load('shot4.png')

    def update(self):
        '''Finds new position for bullet'''
        self.x += self.bullet_speed * math.cos(self.angle * math.pi / 180)
        self.y -= self.bullet_speed * math.sin(self.angle * math.pi / 180)

        self.center = [(self.x + self.radius), (self.y + self.radius)]

    def draw(self, screen):
        '''Draws the bullet onto the screen'''
        screen.blit(self.image, (self.x, self.y))

# Initialize pygame mixer the load and play background music
pygame.mixer.init()
pygame.mixer.music.load("backgroundmusic.ogg")
pygame.mixer.music.play(loops = -1)


collisionSound = pygame.mixer.Sound("explosionSound.ogg")
healthLossSound = pygame.mixer.Sound("healthLoss.mp3")
gameOverSound = pygame.mixer.Sound("gameOver.mp3")

#Set position of graphic
backgroundPosition = [0, 0]

# Load and set up graphic
backgroundImage = pygame.image.load("background1.jpg")

#Set position of graphic
menuPosition = [0, 0]

# Load and set up graphic
menuImage = pygame.image.load("background2.jpg")

# Instructions image
instructions = pygame.image.load("instructo (1).png")

# Credits image

credits = pygame.image.load("creddits.png")

# Load and set up graphic
blueGlowImage = pygame.image.load("blueglow.png")

def gameLoop():
    '''The Main Game Loop'''
    pygame.init()

    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Meteors")

    # Create global Variables
    global instructionsValue
    global currentScreen

    # If the instructions page has not been opened before then open it.
    # Makes sure the first page is the instructions page.
    if instructionsValue == 0:
        currentScreen = 4
    
    # Create Page 4 - Instructions
    while currentScreen == 4 and instructionsValue == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:

                # If the person hits space or escape continue on to the menu
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    
                    instructionsValue += 1
                    currentScreen = 0
                    
        # Draw the menu background
        screen.blit(menuImage, menuPosition)

        # Set up the font
        menuFont = pygame.font.Font("OCRAEXT.TTF", 100)
        instructionsText = menuFont.render("Instructions", True, WHITE)
        screen.blit(instructionsText, [100, 160])

        # Paste the image on the screen
        screen.blit(instructions, (0,0))

        # Display Screen
        pygame.display.flip()

    # Create Page 0 - Menu
    while currentScreen == 0:

        menuDone = False

        currentMenuSelection = 1
        
        # Set up user inputs
        while not menuDone:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:

                    # If they hit space on play go to difficulty select screen
                    if event.key == pygame.K_SPACE and currentMenuSelection == 1:
                        currentScreen = 1
                        menuDone = True
                        global playerLives
                        currentMenuSelection = 1

                        # Create Page 1 - Difficulty Select
                        while currentScreen == 1:

                            # Add menu selection 
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    sys.exit()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        currentScreen = 0
                                    if event.key == pygame.K_UP and not currentMenuSelection == 1:
                                        currentMenuSelection = currentMenuSelection - 1
                                    if event.key == pygame.K_DOWN and not currentMenuSelection == 3:
                                        currentMenuSelection = currentMenuSelection + 1
                                    if event.key == pygame.K_SPACE and currentMenuSelection == 1:
                                        gameDifficulty = 1
                                        playerLives = 5
                                        currentScreen = 2
                                    if event.key == pygame.K_SPACE and currentMenuSelection == 2:
                                        gameDifficulty = 2
                                        playerLives = 3
                                        currentScreen = 2
                                    if event.key == pygame.K_SPACE and currentMenuSelection == 3:
                                        gameDifficulty = 3
                                        playerLives = 1
                                        currentScreen = 2

                            # Paste menu background on screen
                            screen.blit(menuImage, menuPosition)
                            
                            # Set up font for the difficulty screen
                            menuFont = pygame.font.Font("OCRAEXT.TTF", 100)

                            # Code for the easy button
                            easyText = menuFont.render("Easy", True, WHITE)
                            if currentMenuSelection == 1:
                                screen.blit(blueGlowImage, [70, 160])  
                            screen.blit(easyText, [200, 200])

                            # Code for the normal button
                            normalText = menuFont.render("Normal", True, WHITE)
                            if currentMenuSelection == 2:
                                screen.blit(blueGlowImage, [290, 360])
                            screen.blit(normalText, [380, 400])

                            # Code for the hard button
                            hardText = menuFont.render("Hard", True, WHITE)
                            if currentMenuSelection == 3:
                                screen.blit(blueGlowImage, [70, 560])
                            screen.blit(hardText, [200, 600])

                            # Display the screen
                            pygame.display.flip()

                    # If they hit space (Select) on credits open the credits                    
                    if not menuDone:
                        if event.key == pygame.K_SPACE and currentMenuSelection == 2:
                            currentScreen = 3
                            menuDone = True
                            currentMenuSelection = 1

                            # Create Page 3 - Credits
                            while currentScreen == 3:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        sys.exit()
                                    if event.type == pygame.KEYDOWN:

                                        if event.key == pygame.K_ESCAPE:
                                            currentScreen = 0

                                # Paste menu background on screen
                                screen.blit(menuImage, menuPosition)

                                # Setup menu font
                                menuFont = pygame.font.Font("OCRAEXT.TTF", 100)
                                creditsText = menuFont.render("Credits", True, WHITE)
                                screen.blit(creditsText, [240, 160])

                                # Paste credits image
                                screen.blit(credits, (0,0))

                                # Display screen
                                pygame.display.flip()

                    # If instructions is selected in the menu then open instructions 
                    if not menuDone:
                        if event.key == pygame.K_SPACE and currentMenuSelection == 3:
                            currentScreen = 4
                            menuDone = True
                            currentMenuSelection = 1
                            
                            # Reopen Page 4 - Instructions
                            while currentScreen == 4:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        sys.exit()
                                    if event.type == pygame.KEYDOWN:

                                        # If they hit escape or space go back to menu
                                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                                            currentScreen = 0
                                
                                # Paste background
                                screen.blit(menuImage, menuPosition)

                                # Setup font
                                menuFont = pygame.font.Font("OCRAEXT.TTF", 100)
                                instructionsText = menuFont.render("Instructions", True, WHITE)
                                screen.blit(instructionsText, [100, 160])

                                # Paste instructions on screen
                                screen.blit(instructions, (0,0))

                                # display screen
                                pygame.display.flip()

                    # Controls to go up and down on menu screen
                    if not menuDone:
                        if event.key == pygame.K_UP and currentMenuSelection >= 1:
                            currentMenuSelection -= 1
                        if event.key == pygame.K_DOWN and currentMenuSelection <= 3:
                            currentMenuSelection += 1

            # Paste background on screen
            screen.blit(menuImage, menuPosition)

            
            # Font used for the title
            meteorNameFont = pygame.font.Font("OCRAEXT.TTF", 120)
            meteorNameText = meteorNameFont.render("Meteors", True, RED)
            screen.blit(meteorNameText, [200, 200])

            # Font used for the menu screen
            menuFont = pygame.font.Font("OCRAEXT.TTF", 100)

            # Code for the word Play on the main screen
            playText = menuFont.render("Play", True, WHITE)

            # If button 1 is selected make button 1 glow
            if currentMenuSelection == 1:
                screen.blit(blueGlowImage, [200, 360])

            # Paste play text
            screen.blit(playText, [330, 400])

             # Code for the word Credits on the main screen
            creditsText = menuFont.render("Credits", True, WHITE)

            # If button 2 is selected make button 2 glow
            if currentMenuSelection == 2:
                screen.blit(blueGlowImage, [200, 480])

            # Paste credits text
            screen.blit(creditsText, [240, 520])

            # Code for the word Instructions on the main screen
            instructionsText = menuFont.render("Instructions", True, WHITE)

            # If button 3 is selected make button 3 glow        
            if currentMenuSelection == 3:
                screen.blit(blueGlowImage, [200, 600])

            # Paste credits text
            screen.blit(instructionsText, [100, 640])

            # Display screen
            pygame.display.flip()

    #Game screen
    while currentScreen == 2:

        # Make variable playerLevel global
        global playerLevel
        
        # Set it to a starting value of one
        playerLevel = 1
        
        bullets = []
        meteors = []

        #Image for the ship
        player = pl.Player('ship3.png', WIDTH / 2, HEIGHT / 2, 0, (0, 0), False, player_radius)
        #Setting the amount of meteors to 10 to appear on the screen
        for i in range(10):
            meteor = Meteor(screen,random.randint(50, WIDTH-50), random.randint(50, WIDTH-50), getMeteorSpeed(), getMeteorSpeed(), "L")
            meteors.append(meteor)
        #Adding a clock to keep track of time
        clock = pygame.time.Clock()
        #Creating a font variable for size
        font = pygame.font.Font(None, 50)
        #The image for Immunity
        glow = pygame.image.load("glow2.png")
        #Adding a framerate to keep track of lag
        frame_count = 0
        frame_rate = 60
        #Setting an immune time
        immunetime = 0
        #Setting game done to false so the game can run
        gameDone = False
        #When gamedone is true the game ends
        while not gameDone:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # Set the rotation velocity / thrust based on the key pressed
                if event.type == pygame.KEYDOWN:    
                    if event.key == pygame.K_RIGHT:
                        player.rotate_vel = -ROTATE_SPEED
                    if event.key == pygame.K_UP:
                        player.thrust = True
                    if event.key == pygame.K_SPACE:
                        bullets.append(Bullet(player.angle, player.x, player.y))
                    if event.key == pygame.K_LEFT:
                        player.rotate_vel = ROTATE_SPEED

                # Reset rotation velocity / stop thrust when key goes up
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.rotate_vel = 0
                    elif event.key == pygame.K_RIGHT:
                        player.rotate_vel = 0
                    elif event.key == pygame.K_UP:
                        player.thrust = False
                    #
                    if event.key == pygame.K_ESCAPE:
                        currentScreen = 5
                        currentMenuSelection = 1
                    
                        while currentScreen == 5:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    sys.exit()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        currentScreen = 0
                                        global playerScore
                                        playerScore = 0
                                        gameDone = True
                                    if event.key == pygame.K_UP and not currentMenuSelection == 1:
                                        currentMenuSelection = currentMenuSelection - 1
                                    if event.key == pygame.K_DOWN and not currentMenuSelection == 3:
                                        currentMenuSelection = currentMenuSelection + 1
                                    if event.key == pygame.K_SPACE and currentMenuSelection == 1:
                                        currentScreen = 2
                                    if event.key == pygame.K_SPACE and currentMenuSelection == 2:
                                        currentScreen = 4

                            screen.blit(backgroundImage, backgroundPosition)

                            menuFont = pygame.font.Font("OCRAEXT.TTF", 100)

                            pauseText = menuFont.render("Pause", True, WHITE)

                            if currentMenuSelection == 1:
                                screen.blit(blueGlowImage, [200, 160])
                                
                            screen.blit(pauseText, [300, 200])

                            normalText = menuFont.render("Normal", True, WHITE)

                            pygame.display.flip()

            # Copy background image to screen:
            screen.blit(backgroundImage, backgroundPosition)

            player.update()

            immunetime += 1

            # Blits glow for immunity
            if immunetime / 60 < 5:
                screen.blit(glow, (player.x - 20, player.y - 20))

            # Blits hearts 
            for i in range (0, playerLives * 40, 40):
                screen.blit(player.heartImage, (WIDTH - 200 + i, 60))

            ### --------- Collision --------- ###
            
            # Check for collision between bullets & meteors

            for bullet in bullets:
                bullet.update()

            for meteor in meteors:
                meteor.update()
                for bullet in bullets:
                    if isColliding(bullet.center, bullet.radius, meteor.center, meteor.radius) == True:
                        playerScore += 1 * gameDifficulty
                        collisionSound.play()
                        bullets.remove(bullet)
                        if meteor.size == "L" and gameDifficulty >= 2  : 
                              for i in range(2):
                                newmeteors = Meteor(screen, meteor.center[0], meteor.center[1], getMeteorSpeed(), getMeteorSpeed(), "M")
                                meteors.append(newmeteors)
                        if meteor.size == "M" and gameDifficulty == 3:
                            for i in range(2):
                                newmeteors = Meteor(screen, meteor.center[0], meteor.center[1], getMeteorSpeed(), getMeteorSpeed(), "S")
                                meteors.append(newmeteors)

                        meteors.remove(meteor)
                    bullet.draw(screen)
                meteor.draw(screen)
            player.draw(screen)
            
            # Check for collision between player & meteors
            for meteor in meteors:
                if isColliding(player.center, player.radius, meteor.center, meteor.radius) == True:
                    # If player isn't immune:
                    if immunetime / 60 > 5:
                        playerLives -= 1
                        (healthLossSound).play()
                        player.x = WIDTH / 2
                        player.y = HEIGHT / 2
                        player.vel = [0, 0]
                        immunetime = 0
                        if playerLives == 0:
                            (gameOverSound).play()
                            playerScore = 0
                            currentScreen = 6
                            gameDone = True

                meteor.draw(screen)
            player.draw(screen)

            if len(meteors) == 0:
                playerLevel += 1
                for i in range(8 + (playerLevel * gameDifficulty)):
                    immunetime = 0
                    meteor = Meteor(screen,random.randint(50, WIDTH-50), random.randint(50, WIDTH-50), getMeteorSpeed(), getMeteorSpeed(), "L")
                    meteors.append(meteor)

            # FPS counter *** Note: this code must stay here, fps must be reassigned after each loop
            fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
            screen.blit(fps, (20, HEIGHT - 60))

            # --- Timer going up --- #

            # Calculate total seconds
            total_seconds = frame_count // frame_rate

            # Divide by 60 to get total minutes
            minutes = total_seconds // 60

            # Use modulus (remainder) to get seconds
            seconds = total_seconds % 60

            # Use python string formatting to format in leading zeros
            output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)

            # Blit to the screen
            timeText = font.render(output_string, True, WHITE)
            screen.blit(timeText, [WIDTH - 200, 20])

            scoreText = font.render("Score: " + str(int(playerScore)), True, WHITE)
            screen.blit(scoreText, [40, 20])

            # Add to frame count every loop for timer
            frame_count += 1

            pygame.display.flip()

            clock.tick(60)

    while currentScreen == 6:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:    
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        currentScreen = 0
                        gameDone = True
        
        screen.blit(menuImage, menuPosition)

        gameOverFont = pygame.font.Font("game_over.ttf", 250)

        gameOverText = gameOverFont.render("GAME OVER", True, WHITE)

        screen.blit(gameOverText, [165, 200])

        pygame.display.flip()

while __name__ == '__main__':
    gameLoop()
