from random import randint, shuffle
from pygame.math import Vector2

def print_text(message, position, color, font):
    '''Puts text on surface and returns it.'''
    
    text_surface = font.render(message, True, color)
    rect = text_surface.get_rect()
    rect.center = position
    return (text_surface, rect)
    

def position_food(exceptions, sw, sh):
    '''Chooses a random position for food.'''
    
    while True:
        x = randint(0, sw - 1)
        y = randint(0, sh - 1)
        if (x,y) not in exceptions:
            return (x, y)
 
 
def modulo(point, sw, sh):
    '''Makes coordinates small enough to appear on screen.'''
    
    x, y = point
    return (int(x) % sw, int(y) % sh)


def inverse_modulo(point, sw, sh):
    '''Returns the list of different neighbour coordinate representations of the same point on the torus.'''
    
    translations = [Vector2(t) for t in  [(sw, 0), (-sw, 0), (sw, sh), (-sw, -sh), (0, sh), (0, -sh), (sw, -sh), (-sw, sh)]]
    return [point] + [point + t for t in translations]
    
    
def torus_distance(point, food, sw, sh):
    
    return min([point.distance_squared_to(food_) for food_ in inverse_modulo(food, sw, sh)])


def make_decision(head, body, direction, food, sw, sh):
    
    head = Vector2(head)
    direction = Vector2(direction)
    food = Vector2(food)
    
    directions = [v for v in [Vector2(v_) for v_ in [(1, 0), (-1, 0), (0, 1), (0, -1)]] \
                        if (v != -direction) and (modulo(head + v, sw, sh) not in body)]
    
    if directions == []: # Game over in the next step
        return direction
    
    if len(directions) == 1: # No choice
        return directions[0]
    
    current_distance = torus_distance(head, food, sw, sh)
    
    # shuffle(directions) To many edges with this option.
    for v in directions:
        if torus_distance(head + v, food, sw, sh) < current_distance:
            return v
    
    # TODO: Make better decisions by observing the connected components
    # of the graph obtained from the complement of the snake's body.
    
    return directions[randint(0, len(directions) - 1)]

    