from utils import *


class SnakeObject:
    def __init__(self, initial_position, initial_length, initial_direction, initial_speed, speed_increment, screen_width, screen_height):
        self.body = [(initial_position[0] - i, initial_position[1]) for i in reversed(range(initial_length))] 
        self.direction = initial_direction
        self.speed = initial_speed
        self.speed_increment = speed_increment
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.food = position_food(self.body, self.screen_width, self.screen_height)

    def head(self):
        return self.body[-1]
        
    def size(self):
        return len(self.body)

    def move(self):
        head = self.head()
        direction = self.direction
        new_head = ((head[0] + direction[0]) % self.screen_width, (head[1] + direction[1]) % self.screen_height)   # '%' here makes the snake return 
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
        surface.set_at(self.head(), 'green')
        for point in self.body[:-1]:
            surface.set_at(point, 'dark green')

        surface.set_at(self.food, 'red')
