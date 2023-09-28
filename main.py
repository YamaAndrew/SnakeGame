# importing pygame cause duh
# importing sys for system funtionality (ex. sys.exit())
# importing random for random number generation for fruit spawning
import pygame, sys, random

# for all data stored in vectors (fruit, snake, etc.)
from pygame.math import Vector2

class SNAKE:
    # initialize snake's body and direction
    def __init__(self): 
        self.body = [Vector2(5,10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up = pygame.image.load('resources/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('resources/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('resources/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('resources/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('resources/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('resources/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('resources/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('resources/tail_left.png').convert_alpha()

        self.body_horizontal = pygame.image.load('resources/body_horizontal.png').convert_alpha()
        self.body_vertical = pygame.image.load('resources/body_vertical.png').convert_alpha()

        self.body_tr = pygame.image.load('resources/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('resources/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('resources/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('resources/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('resources/crunch.wav')
    
    # draw the snake
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        # iterate through each block of snake's body 
        for index, block in enumerate(self.body):
            # access current block's position
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            # display head if its the first block
            if index == 0: 
                screen.blit(self.head, block_rect)

            # display tail if its the last block
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)

            # display body for all other blocks
            else:
                # store the values of the blocks ahead and behind the current block
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                # if the block ahead and the block behind are on the same x-axis, snake body is vertical
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)

                # if the block ahead and block behind are on the same y-axis, snake body is horizontal
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)

                # otherwise, the snake body is turning
                else:

                    # snake is moving down and turning left
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)

                    # snake is moving up and turning left
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)

                    # snake is moving down and turning right
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)

                    # snake is moving up and turing right
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    # update snake's head to look in correct direction based on relation between head block and the block that follows
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]  
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    # update snake's tail to trail in correct direction based on relation between tail block and the block ahead of it
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    # move and potentially extend the snake's body
    def move_snake(self):
        # if snake ate a fruit
        if self.new_block == True:
            body_copy = self.body[:]                                # copy the blocks of snake's orignal body
            body_copy.insert(0, body_copy[0] + self.direction)      # insert new block to act as snake's new head block
            self.body = body_copy[:]                                # updated body = old body + head
            self.new_block = False
        # if snake is just moving normally
        else:
            body_copy = self.body[:-1]                              # copy the blocks of snake's orignal body (exept for tail block)
            body_copy.insert(0, body_copy[0] + self.direction)      # insert new block to act as snake's new head block
            self.body = body_copy[:]                                # updated body = old body + new head - old tail

    # update new_block variable to true (snake body grows bigger in move_snake())
    def add_block(self):
        self.new_block = True

    # play's the crunch sound of snake eating apple
    def play_crunch_sound(self):
        self.crunch_sound.play()

    # reset snake's direction and vector back to original size and position 
    def reset(self):
        self.body = [Vector2(5,10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0,0)

class FRUIT:
    # call randomize function
    def __init__(self):
        self.randomize()
    
    # draw the fruit square
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size,self.pos.y * cell_size,cell_size,cell_size) # postion = pixels moved * cell size
        screen.blit(apple,fruit_rect) # display apple at correct spot
        #pygame.draw.rect(screen,(126,166,114),fruit_rect)

    # create random position for fruit square
    def randomize(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)

class MAIN:
    # create both snake and fruit object when object for this class is created
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.high_score = 0

    # move snake's body 
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    # draw fruit and snake objects
    def draw_elements(self):
        self.draw_grass()           # draw checkered pattern in grass
        self.fruit.draw_fruit()     # draw fruit 
        self.snake.draw_snake()     # draw snake
        self.draw_score()           # display scoreboard 

    # function calls for when the snake eats an apple
    def check_collision(self):
        # if snake eats apple...
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()          # ...update fruit to new position and...
            self.snake.add_block()          # ...increase the snake's body length and...
            self.snake.play_crunch_sound()  # ...play crunch sound

        # if apple spawns where snake body is already positioned...
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()      # ...update fruit to new position

    # end game if snake hits itself or wall
    def check_fail(self):

        # if head of snake is not within wall bounds of game, terminate game
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        # check if any part of the snake's body is at the same position as the snake's head, and terminate game if so
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    # terminate game
    def game_over(self):
        self.snake.reset()

    # draw checkered grass pattern 
    def draw_grass(self):

        grass_color = (167,209,61) # darker green that is diplayed

        # loops for checkered pattern
        for row in range(cell_number):
            # if current row cell number is even...
            if row % 2 == 0:
                # ...display darker green on even blocks
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            # if current row cell is odd...
            else:
                for col in range(cell_number):
                    # ... display darker green on odd blocks
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    # draw score with image at bottom right corner of screen
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)                              # store current score as length of snake (minus starting  3 blocks)
        self.high_score = max(self.high_score, int(score_text))                 # update high_score 
        high_score_text = str(self.high_score)                                  # hold high_score as a string
        score_surface = game_font.render(score_text,True,(56,74,12))            # surface for current score scoreboard
        high_score_surface = game_font.render(high_score_text,True,(50,50,200)) # surface for high score scoreboard

        # current score scoreboard position
        score_x = cell_size * cell_number - 60
        score_y = cell_size * cell_number - 60
        score_rect = score_surface.get_rect(center = (score_x,score_y))     # score is in middle center of scoreboard
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))       # image is in left center of scoreboard
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

        # high score scoreboard position
        high_score_x = cell_size * cell_number // 2
        high_score_y = 40
        high_score_rect = high_score_surface.get_rect(center = (high_score_x,high_score_y)) #high score is in middle center of scoreboard
        trophy_rect = trophy.get_rect(midright = (high_score_rect.left, high_score_rect.centery))   # image is in the left center of high score scoreboard
        

        # display scoreboard
        # pygame.draw.rect(screen,(167,209,61), bg_rect)  # draw green background rect onto screen surface
        screen.blit(score_surface,score_rect)           # display score  surface
        screen.blit(apple,apple_rect)                   # display apple image
        # pygame.draw.rect(screen,(56,74,12),bg_rect,2)   # draw black outline around scoreboard
        screen.blit(high_score_surface,high_score_rect) # display high score surface
        screen.blit(trophy,trophy_rect)                 # display trophy image
        # pygame.font.Font.render


pygame.mixer.pre_init(44100,-16,2,512)  # play crunch sound sooner (right when snake head meets apple)
pygame.init()       # starts enitre pygame (all modules within pygame)

cell_size = 40      # size of each square within 'grid'
cell_number = 20    # max amount of cells per column/r

screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))         # create and display game window

clock = pygame.time.Clock()         # manage time in pygame (allows consistent gameplay speed)

apple = pygame.image.load('resources/apple.png').convert_alpha()    # use apple.png as image for fruit
apple = pygame.transform.scale(apple, (cell_size, cell_size))       # scale apple.png to correct size
trophy = pygame.image.load('resources/trophy.png').convert_alpha()  # use trophy.png for high score image
trophy = pygame.transform.scale(trophy, (cell_size, cell_size))     # scale trophy.png to correct size

game_font = pygame.font.Font('resources/Super Comic.ttf', 25)

main_game = MAIN()      # create game objects

SCREEN_UPDATE = pygame.USEREVENT            # custom event to trigger with timer
pygame.time.set_timer(SCREEN_UPDATE,150)    # trigger SCREEN_UPDATE every 150 milliseconds 

# game loop
while True:
    # iterate for every event (pressing buttons, clicking mouse, timer, etc.)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:   # closing the window by pressing the x button 
            pygame.quit()               # opposite of pygame.init()
            sys.exit()                  # ends any kind of code being run on

        if event.type == SCREEN_UPDATE: # if SCREEN_UPDATE is triggered (every 150 ms)
            main_game.update()          # call move_snake function to move snake's body

        # if arrow key is pressed, change snake's direction to corresponding arrow direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:            # if snake is not currently moving down...
                    main_game.snake.direction = Vector2(0,-1)   # allow snake to move up
            if event.key == pygame.K_LEFT:                          
                if main_game.snake.direction.x != 1:            # if snake is not currently moving right...
                    main_game.snake.direction = Vector2(-1,0)   # allow snake to move left
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:           # if snake is not currently moving up...
                    main_game.snake.direction = Vector2(0,1)    # allow snake to move down
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:           # if snake is not currenly moving left...
                    main_game.snake.direction = Vector2(1,0)    # allow snake to move right


    screen.fill((175,210,70))           # give screen surface a green color
    main_game.draw_elements()           # draw game elements
    pygame.display.update()             # update game window
    clock.tick(60)                      # game runs at most 60fps