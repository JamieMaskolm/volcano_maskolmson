import pygame, sys, random
from pygame.math import Vector2
from pygame import mixer
import csv
import main




def play(user, username):
    class SNAKE():
        def __init__(self):
            self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
            self.direction = Vector2(0, 0)
            self.new_block = False

            self.head_up = pygame.image.load("SNAKE/Snake_head_U.png").convert_alpha()
            self.head_down = pygame.image.load("SNAKE/Snake_head_D.png").convert_alpha()
            self.head_left = pygame.image.load("SNAKE/Snake_head_L.png").convert_alpha()
            self.head_right = pygame.image.load("SNAKE/Snake_head_R.png").convert_alpha()

            self.tail_up = pygame.image.load("SNAKE/Snake_tail_U.png").convert_alpha()
            self.tail_down = pygame.image.load("SNAKE/Snake_tail_D.png").convert_alpha()
            self.tail_left = pygame.image.load("SNAKE/Snake_tail_L.png").convert_alpha()
            self.tail_right = pygame.image.load("SNAKE/Snake_tail_R.png").convert_alpha()

            self.body_vert = pygame.image.load("SNAKE/Body_Vert.png").convert_alpha()
            self.body_hor = pygame.image.load("SNAKE/Body_Horiz.png").convert_alpha()

            self.curve_up = pygame.image.load("SNAKE/Snake_Curve_U.png").convert_alpha()
            self.curve_down = pygame.image.load("SNAKE/Snake_Curve_D.png").convert_alpha()
            self.curve_left = pygame.image.load("SNAKE/Snake_Curve_L.png").convert_alpha()
            self.curve_right = pygame.image.load("SNAKE/Snake_Curve_R.png").convert_alpha()

            self.crunch_sound = pygame.mixer.Sound("SNAKE/snack_sound.wav")

        def draw_snake(self):
            self.update_head_graphics()
            self.update_tail_graphics()

            for index, block in enumerate(self.body):
                # 1. we still need a rect for the positioning
                x_pos = int(block.x * cell_size)
                y_pos = int(block.y * cell_size)
                block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

                # 2. what direction is the face heading
                if index == 0:
                    SCREEN.blit(self.head, block_rect)
                elif index == len(self.body) - 1:
                    SCREEN.blit(self.tail, block_rect)
                else:
                    previous_block = self.body[index + 1] - block
                    next_block = self.body[index - 1] - block
                    if previous_block.x == next_block.x:
                        SCREEN.blit(self.body_vert, block_rect)
                    elif previous_block.y == next_block.y:
                        SCREEN.blit(self.body_hor, block_rect)
                    else:
                        if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                            SCREEN.blit(self.curve_left, block_rect)
                        if previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                            SCREEN.blit(self.curve_down, block_rect)
                        if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                            SCREEN.blit(self.curve_up, block_rect)
                        if previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                            SCREEN.blit(self.curve_right, block_rect)

        def update_head_graphics(self):
            head_relation = self.body[1] - self.body[0]
            if head_relation == Vector2(1, 0):
                self.head = self.head_left
            elif head_relation == Vector2(-1, 0):
                self.head = self.head_right
            elif head_relation == Vector2(0, 1):
                self.head = self.head_up
            elif head_relation == Vector2(0, -1):
                self.head = self.head_down

        def update_tail_graphics(self):
            tail_relation = self.body[-2] - self.body[-1]
            if tail_relation == Vector2(1, 0):
                self.tail = self.tail_left
            elif tail_relation == Vector2(-1, 0):
                self.tail = self.tail_right
            elif tail_relation == Vector2(0, 1):
                self.tail = self.tail_up
            elif tail_relation == Vector2(0, -1):
                self.tail = self.tail_down

        def move_snake(self):
            if self.new_block == True:

                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]
                self.new_block = False

            else:
                body_copy = self.body[:-1]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]

        def add_block(self):
            self.new_block = True

        def play_crunch_sound(self):
            self.crunch_sound.play()

        def reset(self):
            self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
            self.direction = Vector2(0, 0)

    class FRUIT:
        def __init__(self):
            self.randomize()

        def draw_fruit(self):
            fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
            SCREEN.blit(apple, fruit_rect)

        def randomize(self):
            self.x = random.randint(0, cell_number - 1)
            self.y = random.randint(0, cell_number - 1)
            self.pos = Vector2(self.x, self.y)

    class MAIN:
        def __init__(self):
            self.snake = SNAKE()
            self.fruit = FRUIT()

        def update(self):
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

        def draw_elements(self):
            self.draw_grass()
            self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.draw_score()

        def check_collision(self):
            if self.fruit.pos == self.snake.body[0]:
                self.fruit.randomize()
                self.snake.add_block()
                self.snake.play_crunch_sound()

            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()

        def check_fail(self):
            if not 0 <= self.snake.body[0].x < cell_number:
                self.game_over(user,username)
            if not 0 <= self.snake.body[0].y < cell_number:
                self.game_over(user,username)

            for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    self.game_over(user,username)

        def game_over(self,user,username):
            if int(self.score_text) > int(user[username][1]):
                user.update({username: [user[username][0], str(self.score_text), user[username][2]]})
                self.write_to_csv()
            self.snake.reset()

        def draw_grass(self):
            grass_color = (180, 235, 80)
            for row in range(cell_number):
                if row % 2 == 0:
                    for col in range(cell_number):
                        if col % 2 == 0:
                            grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                            pygame.draw.rect(SCREEN, grass_color, grass_rect)
                else:
                    for col in range(cell_number):
                        if col % 2 != 0:
                            grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                            pygame.draw.rect(SCREEN, grass_color, grass_rect)

        def draw_score(self):


            self.score_text = str(len(self.snake.body) - 3)
            score_surface = game_font.render(self.score_text, True, (56, 74, 12))
            score_x = int(cell_size * cell_number - 750)
            score_y = int(cell_size * cell_number - 40)
            score_rect = score_surface.get_rect(center=(score_x, score_y))



            SCREEN.blit(score_surface, score_rect)


        def write_to_csv(self):

            filename = "scores.csv"
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                for key, values in user.items():
                    row = [key] + values
                    writer.writerow(row)



    # Initalisierung des Spiels
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    mixer.music.load("SNAKE/8_Bit_Surf.mp3")
    mixer.music.play(-1)
    cell_size = 40
    cell_number = 20
    SCREEN = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    clock = pygame.time.Clock()
    apple = pygame.image.load("SNAKE/Apple_snake.png").convert_alpha()
    game_font = pygame.font.Font("Purple Smile.ttf", 25)

    # New Event
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 120)
    main_game = MAIN()

    #CSV Score Writing



    # mainloop des Spiels
    def Snake_play():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == SCREEN_UPDATE:
                    main_game.update()


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main.MAIN(username, user)

                    if event.key == pygame.K_UP:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(1, 0)



            SCREEN.fill(("#B2FF66"))
            main_game.draw_elements()
            pygame.display.update()
            clock.tick(60)

    Snake_play()



