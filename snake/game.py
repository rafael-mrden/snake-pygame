import pygame
from pygame.locals import *
from pygame.math import Vector2

from models import SnakeObject
from utils import *

class SnakeGame:
    def __init__(self):
        
        # Game parameters
        self.screen_parameters = {
            'width'  : 30,
            'height' : 30,
            'scaling_factor' : 20 ,
            'game_over_pause' : 3, # seconds
        }
        
        self.color_parameters = {
            'background_color' : 'black',
            'snake_color' : 'dark green',
            'snake_head_color' : 'green',
            'food_color' : 'red',
            'text_color' : 'green',
        }

        self.initial_snake_parameters = {
            'initial_position' : (
                int(self.screen_parameters['width'] / 2),
                int(self.screen_parameters['height'] / 2)
            ),
            'initial_length' : 7,
            'initial_direction' : (1, 0),
            'initial_speed' : 7, # Pixel per seconds
            'speed_increment' : 0.25,
        } 
        
        pygame.init()
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode(
            (self.screen_parameters['width'] * self.screen_parameters['scaling_factor'],
            self.screen_parameters['height'] * self.screen_parameters['scaling_factor'])
        )
        self.clock = pygame.time.Clock()
        
        self.snake = SnakeObject(
            self.initial_snake_parameters,
            self.screen_parameters,
            self.color_parameters
        )

        self.state = 'welcome'
        self.auto = False # True = Self-driving snake - experimental
        self.score = 0 # Updates only on game_over
        

    def main_loop(self):
        if self.state == 'welcome':
            self.welcome()

        while self.state == 'game':
            
            if self.auto:
                self._self_drive()
            else:
                self._handle_input()
            
            self._process_game_logic()
            self._draw()
            
        if self.state == 'game_over':
            self.game_over()    
            

    def welcome(self):
        self.screen.fill(self.color_parameters['background_color'])

        x_max, y_max = Vector2(self.screen.get_size())
        position1 = Vector2(x_max / 2, y_max / 4)
        position2 = Vector2(x_max / 2, y_max / 4 + 40)
        position3 = Vector2(x_max / 2, y_max / 2)
        position4 = Vector2(x_max / 2, 3 * y_max / 4)
        position5 = Vector2(x_max / 2, 3 * y_max / 4 + 30)
        position6 = Vector2(x_max / 2, 3 * y_max / 4 + 60)
        color = self.color_parameters['text_color']
        
        self.screen.blit( *print_text("SNAKE", position1, color, self.font(80)) )
        self.screen.blit( *print_text("by RM", position2, color, self.font(15)) )
        self.screen.blit( *print_text("Play: 'Enter'", position4, color, self.font(25)) )
        self.screen.blit( *print_text("Exit: 'Esc'", position5, color, self.font(25)) )
        self.screen.blit( *print_text("Auto: 'A'", position6, color, self.font(25)) )
        
        pygame.display.flip()
        
        input = self.wait([K_KP_ENTER, K_RETURN, K_a]) # Wait for enter
        if input == K_a:
            self.auto = True

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
                pygame.time.wait(1000 * self.screen_parameters['game_over_pause'])
                self.score = self.snake.size() - self.initial_snake_parameters['initial_length']
                
                self.state = 'game_over'
                self.snake = None
            
        
    def _draw(self):
        self.screen.fill(self.color_parameters['background_color'])

        if self.snake:
            self.snake_screen = pygame.Surface(
                (self.screen_parameters['width'],
                self.screen_parameters['height']),
                pygame.SRCALPHA, 32)
                
            self.snake.draw(self.snake_screen)
            self.screen.blit(pygame.transform.scale(self.snake_screen, self.screen.get_rect().size), (0, 0))
        
        pygame.display.flip()
        
        if self.snake:
            self.clock.tick( self.snake.speed )


    def game_over(self):
        self.screen.fill(self.color_parameters['background_color'])

        x_max, y_max = Vector2(self.screen.get_size())
        position1 = Vector2(x_max / 2, y_max / 4)
        position3 = Vector2(x_max / 2, y_max / 2)
        position4 = Vector2(x_max / 2, 3 * y_max / 4)
        position5 = Vector2(x_max / 2, 3 * y_max / 4 + 30)
        color = self.color_parameters['text_color']
        
        self.screen.blit( *print_text("GAME OVER!", position1, color, self.font(40)) )
        self.screen.blit( *print_text(f"Score: {self.score}", position3, color, self.font(30)) )
        self.screen.blit( *print_text("Play: 'Enter'", position4, color, self.font(25)) )
        self.screen.blit( *print_text("Exit: 'Esc'", position5, color, self.font(25)) )
        
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
                    return event.key


    def font(self, size):
        '''Produces pygame font, to be used by utils.print_text.'''
    
        return pygame.font.Font(None, size)


    def _self_drive(self):
        '''Idea for now: locally minimize the distance (in the torus metric).'''
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                quit()
        
        head = self.snake.head()
        body = self.snake.body
        direction = self.snake.direction
        food = self.snake.food
        
        new_direction = make_decision(
            head, body, direction, food,
            self.screen_parameters['width'], self.screen_parameters['height']
        )
        
        self.snake.change_direction(new_direction)
        return

