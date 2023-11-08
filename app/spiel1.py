import pygame
from pygame import mixer
import random
import csv
import sys
import main


def play(user, username):
    # Hauptparameter
    global Score_Clock, score_text
    pygame.init()
    pygame.font.init()
    pygame.mixer.pre_init()
    start_time = pygame.time.get_ticks()
    mixer.init(44100, -16, 6, 4096)
    mixer.music.load("VOLCANO/A_little_Bit.mp3")
    mixer.music.play(-1)
    HEIGHT = 900
    WIDTH = 1440
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    clock = pygame.time.Clock()
    pygame.display.set_caption("Volcano")
    game_over = pygame.image.load("VOLCANO/Game_Over_screen.png")

    # Spielerklassen und Instanzen
    class Figure:
        def __init__(self, x, y, speed, jumpVar, direction, screen, stand):
            self.x = x
            self.y = y
            self.speed = speed
            self.jumpVar = jumpVar
            self.direction = direction
            self.screen = screen
            self.stand = stand
            self.stepsL = False
            self.stepsR = False
            self.stepsDie = False
            self.isJump = False
            self.jumpCount = 10
            self.run_right = [
                pygame.image.load("VOLCANO/Run__000.png"),
                pygame.image.load("VOLCANO/Run__001.png"),
                pygame.image.load("VOLCANO/Run__002.png"),
                pygame.image.load("VOLCANO/Run__003.png"),
                pygame.image.load("VOLCANO/Run__004.png"),
                pygame.image.load("VOLCANO/Run__005.png"),
                pygame.image.load("VOLCANO/Run__006.png"),
                pygame.image.load("VOLCANO/Run__007.png"),
                pygame.image.load("VOLCANO/Run__008.png"),
                pygame.image.load("VOLCANO/Run__009.png"),
            ]
            self.run_left = [
                pygame.image.load("VOLCANO/Runleft__000.png"),
                pygame.image.load("VOLCANO/Runleft__001.png"),
                pygame.image.load("VOLCANO/Runleft__002.png"),
                pygame.image.load("VOLCANO/Runleft__003.png"),
                pygame.image.load("VOLCANO/Runleft__004.png"),
                pygame.image.load("VOLCANO/Runleft__005.png"),
                pygame.image.load("VOLCANO/Runleft__006.png"),
                pygame.image.load("VOLCANO/Runleft__007.png"),
                pygame.image.load("VOLCANO/Runleft__008.png"),
                pygame.image.load("VOLCANO/Runleft__009.png"),
            ]
            self.die = [
                pygame.image.load("VOLCANO/Dead__000.png"),
                pygame.image.load("VOLCANO/Dead__001.png"),
                pygame.image.load("VOLCANO/Dead__002.png"),
                pygame.image.load("VOLCANO/Dead__003.png"),
                pygame.image.load("VOLCANO/Dead__004.png"),
                pygame.image.load("VOLCANO/Dead__005.png"),
                pygame.image.load("VOLCANO/Dead__006.png"),
                pygame.image.load("VOLCANO/Dead__007.png"),
                pygame.image.load("VOLCANO/Dead__008.png"),
                pygame.image.load("VOLCANO/Dead__009.png")]

        def walk(self, animations):
            if animations[0]:
                self.x -= self.speed
                self.direction = [True, False, False]
                self.stepsL += 3
            if animations[1]:
                self.x += self.speed
                self.direction = [False, True, False]
                self.stepsR += 3

        def resetSteps(self):
            self.stepsL = 0
            self.stepsR = 0

        def stopMove(self):
            self.direction = [False, False, True]
            self.resetSteps()

        def drawFigure(self):
            if self.stepsR == 63:
                self.stepsR = 0
            if self.stepsL == 63:
                self.stepsL = 0

            if self.direction[0]:
                self.screen.blit(self.run_left[self.stepsL // 9], (self.x, self.y))
            if self.direction[1]:
                self.screen.blit(self.run_right[self.stepsR // 9], (self.x, self.y))
            if self.direction[2]:
                self.screen.blit(self.stand, (self.x, self.y))

        def drawDeath(self):
            self.stepsDie = 9
            self.screen.blit(self.die[self.stepsDie], (self.x, self.y))

    class Lava(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y, width, height, speed):
            super().__init__()
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.speed = speed
            self.width = width
            self.height = height
            self.current_sprite = 0
            self.sprites = [
                pygame.image.load("VOLCANO/Lava_1.png"),
                pygame.image.load("VOLCANO/Lava_2.png"),
                pygame.image.load("VOLCANO/Lava_3.png"),
                pygame.image.load("VOLCANO/Lava_4.png"),
            ]
            self.image = self.sprites[self.current_sprite]
            self.rect = self.image.get_rect()

        def update(self):
            self.current_sprite += 0.2
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
            self.rect.center = [self.pos_x, self.pos_y]

            self.pos_y += self.speed
            if self.pos_y > HEIGHT:
                self.pos_y = 0
                self.pos_x = random.randrange(0, WIDTH, 1)

        def resetSpeed(self):
            self.speed = random.randrange(1, 5)

    # Variablen für Animation, Effekte und Instanzen---------------------------------------------------|

    # Figure1_Variablen
    stand = pygame.image.load("VOLCANO/Idle__000.png")
    # Soundeffects
    jump_sound = pygame.mixer.Sound("VOLCANO/jumppp11.mp3")
    game_over_Sound = pygame.mixer.Sound("VOLCANO/Volcano_gameover.ogg")
    # score
    font = pygame.font.Font("Purple Smile.ttf", 50)
    # invisible_walls
    rightWall = pygame.draw.rect(screen, (0, 0, 0), (1425, 100, 1, 900), 0)
    leftWall = pygame.draw.rect(screen, (0, 0, 0), (10, 100, 1, 900), 0)
    # Instanz: player1
    player1 = Figure(700, 748, 20, -16, [False, False, True], screen, stand)
    # Instanz: fireBalls
    moving_sprites = pygame.sprite.Group()
    fireBalls = [Lava(random.randint(0, WIDTH), 0, 50, 50, random.randrange(1, 5)) for i in range(20)]
    moving_sprites.add(fireBalls)
    playerAlive = True

    # Festhalen des Highsores

    def write_to_csv():
        filename = "scores.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for key, values in user.items():
                row = [key] + values
                writer.writerow(row)

    def score_update():
        if int(time_string) > int(user[username][2]):
            user.update({username: [user[username][0], user[username][1], time_string]})
            write_to_csv()

    # Hauptanwendung des Spiels (Main-loop)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Pygame Steuerungsfunktion
        keys = pygame.key.get_pressed()

        # Playerscore Variablen
        if playerAlive:
            current_time = pygame.time.get_ticks()
            time_passed = current_time - start_time
            time_string = str(time_passed // 1000)
            score_text = font.render('Score: ', True, (139, 0, 0))
            Score_Clock = font.render(time_string, True, (139, 0, 0))

        # PlayerHitbox
        playerHitBox = pygame.Rect(player1.x, player1.y, 40, 80)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Geschwindigkeit und Hitbox der fireBalls
        for fireBall in fireBalls:
            fireBall.speed += 0.01
            fireBall.update()
            if keys[pygame.K_RETURN] and playerAlive is False:
                fireBall.speed = random.randrange(1, 5)
            if playerHitBox.colliderect(pygame.Rect(fireBall.pos_x, fireBall.pos_y, 20, 20)) and playerAlive is True:
                pygame.mixer.Sound.play(game_over_Sound)
                pygame.mixer.fadeout(5000)
                playerAlive = False

        # Zuweisung der Spielersteuerung
        if keys[pygame.K_ESCAPE]:
            main.MAIN(username, user)

        if keys[pygame.K_RETURN] and playerAlive == False:
            player1.x = 700
            player1.y = 748
            playerAlive = True
            start_time = pygame.time.get_ticks()

        if keys[pygame.K_LEFT] and not playerHitBox.colliderect(leftWall) and playerAlive:
            player1.walk([True, False])
        elif keys[pygame.K_RIGHT] and not playerHitBox.colliderect(rightWall) and playerAlive:
            player1.walk([False, True])
        else:
            player1.stopMove()

        # Sprungbewegung
        if not player1.isJump:
            if keys[pygame.K_SPACE]:
                playerAlive = True
                pygame.mixer.Sound.play(jump_sound)
                player1.isJump = True
        else:
            if player1.jumpCount >= -10:
                player1.y -= (player1.jumpCount * abs(player1.jumpCount)) * 0.5
                player1.jumpCount -= 1
            else:
                player1.jumpCount = 10
                player1.isJump = False
        if playerAlive:
            player1.drawFigure()
        else:
            score_update()
            write_to_csv()
            player1.drawDeath()
            screen.blit(game_over, (0, 0))
        pygame.display.update()
        image = pygame.image.load("VOLCANO/Volcano2.png")
        screen.blit(image, (0, 0))
        screen.blit(Score_Clock, (1380, 10))
        screen.blit(score_text, (1200, 10))
        moving_sprites.draw(screen)
        moving_sprites.update()
        clock.tick(60)
