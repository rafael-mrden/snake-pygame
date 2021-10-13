import pygame
from pygame.math import Vector2
from pygame.locals import *

from models import SnakeObject
from utils import *

class SnakeGame:
    def __init__(self):
        
        # Game parameters
        self.background_color = 'white'
        self.screen_width  = 20
        self.screen_height = 20
        self.scaling_factor = 20

        self.game_over_pause = 3 # seconds
        
        # Initial snake parameters
        self.initial_position = ( int(self.screen_width / 2), int(self.screen_height / 2) )
        self.initial_length = 5
        self.initial_direction = (1, 0)
        self.initial_speed = 5 # Pixel per seconds
        self.speed_increment = 0.5
        #################
        
        pygame.init()
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode((self.screen_width * self.scaling_factor, self.screen_height * self.scaling_factor))
        self.clock = pygame.time.Clock()
        
        self.snake = SnakeObject( self.initial_position, self.initial_length, self.initial_direction, self.initial_speed, self.speed_increment, self.screen_width, self.screen_height)

        self.state = 'welcome' 
        self.score = 0 # Updates only on game_over
        

    def main_loop(self):
        if self.state == 'welcome':
            self.welcome()

        while self.state == 'game':
            self._handle_input()
            self._process_game_logic()
            self._draw()
            
        if self.state == 'game_over':
            self.game_over()    
            

    def welcome(self):
        self.screen.fill(self.background_color)

        x_max, y_max = Vector2(self.screen.get_size())
        position1 = Vector2(x_max / 2, y_max / 4)
        position2 = Vector2(x_max / 2, y_max / 2)
        position3 = Vector2(x_max / 2, 3 * y_max / 4)
        position4 = Vector2(x_max / 2, 3 * y_max / 4 + 30)
        position5 = Vector2(x_max / 2, y_max / 4 + 40)
        
        self.screen.blit( *print_text("SNAKE", position1, "dark green", self.font(80)) )
        self.screen.blit( *print_text("Play: 'Enter'", position3, "dark green", self.font(25)) )
        self.screen.blit( *print_text("Exit: 'Esc'", position4, "dark green", self.font(25)) )
        self.screen.blit( *print_text("by RM", position5, "dark green", self.font(15)) )
        
        pygame.display.flip()
        
        self.wait([K_KP_ENTER, K_RETURN]) # Wait for enter

        self.state = 'game'
        

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                quit()
                
        is_key_pressed = pygame.key.get_pressed()

        if self.snake:
            if is_key_pressed[K_LEFT] and self.snake.direction != (1, 0):
                self.snake.change_direction((-1, 0))
            elif is_key_pressed[K_RIGHT] and self.snake.direction != (-1, 0):
                self.snake.change_direction((1, 0))
            elif is_key_pressed[K_UP] and self.snake.direction != (0, 1):
                self.snake.change_direction((0, -1))                    
            elif is_key_pressed[K_DOWN] and self.snake.direction != (0, -1):
                self.snake.change_direction((0, 1))                 


    def _process_game_logic(self):
        if self.snake:
            self.snake.move()
            
            if self.snake.is_dead():
                pygame.time.wait(1000 * self.game_over_pause)
                self.score = self.snake.size() - self.initial_length
                
                self.state = 'game_over'
                self.snake = None
            
        
    def _draw(self):
        self.screen.fill(self.background_color)

        if self.snake:
            self.snake_screen = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA, 32)
            self.snake.draw(self.snake_screen)
            self.screen.blit(pygame.transform.scale(self.snake_screen, self.screen.get_rect().size), (0, 0))
        
        pygame.display.flip()
        
        if self.snake:
            self.clock.tick( self.snake.speed )


    def game_over(self):
        self.screen.fill(self.background_color)

        x_max, y_max = Vector2(self.screen.get_size())
        position1 = Vector2(x_max / 2, y_max / 4)
        position2 = Vector2(x_max / 2, y_max / 2)
        position3 = Vector2(x_max / 2, 3 * y_max / 4)
        position4 = Vector2(x_max / 2, 3 * y_max / 4 + 30)
        
        self.screen.blit( *print_text("GAME OVER!", position1, "dark green", self.font(40)) )
        self.screen.blit( *print_text(f"Score: {self.score}", position2, "dark green", self.font(30)) )
        self.screen.blit( *print_text("Play: 'Enter'", position3, "dark green", self.font(25)) )
        self.screen.blit( *print_text("Exit: 'Esc'", position4, "dark green", self.font(25)) )
        
        pygame.display.flip()
        
        self.wait([K_KP_ENTER, K_RETURN])
        
        # Start new game
        snake = SnakeGame()
        snake.main_loop()


    def wait(self, list_of_keys):
        '''Waits for keyboard input'''
    
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    quit()
                if event.type == KEYDOWN and event.key in list_of_keys:
                    return


    def font(self, size):
        '''Produces pygame font, to be used by utils.print_text.'''
    
        return pygame.font.Font(None, size)
