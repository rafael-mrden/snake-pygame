from utils import *


class SnakeObject:
    def __init__(self, initial_snake_parameters, screen_parameters, color_parameters):
        
        x0, y0 = initial_snake_parameters['initial_position']
        len0 = initial_snake_parameters['initial_length']
        self.body = [(x0 - i, y0) for i in reversed(range(len0))] 
        self.direction = initial_snake_parameters['initial_direction']
        self.speed = initial_snake_parameters['initial_speed']
        self.speed_increment = initial_snake_parameters['speed_increment']
        self.screen_width = screen_parameters['width']
        self.screen_height = screen_parameters['height']
        self.color_parameters = color_parameters
        
        self.food = position_food(self.body, self.screen_width, self.screen_height)
        
        
    def head(self):
        return self.body[-1]
        
    def size(self):
        return len(self.body)

    def move(self):
        head = self.head()
        direction = self.direction
        new_head = modulo(head[0] + direction[0], head[1] + direction[1], self.screen_width, self.screen_height)   
        self.body.append(new_head)
        
        if self.got_food():
            self.food = position_food(self.body, self.screen_width, self.screen_height)
            self.speed += self.speed_increment
            
        else:
            self.body.pop(0) # remove the last element
        

    def change_direction(self, direction):
        self.direction = direction
    
    def change_speed(self, new_speed):
        self.speed = new_speed
        
    def got_food(self):
        return self.food == self.head()
    
    def is_dead(self):
        return self.head() in self.body[:-1]


    def draw(self, surface):
        surface.set_at(self.head(), self.color_parameters['snake_head_color'])
        for point in self.body[:-1]:
            surface.set_at(point, self.color_parameters['snake_color'])

        surface.set_at(self.food, self.color_parameters['food_color'])
