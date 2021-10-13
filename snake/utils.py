from random import randint


def print_text(message, position, color, font):
    '''Puts text on surface and returns it.'''
    
    text_surface = font.render(message, True, color)
    rect = text_surface.get_rect()
    rect.center = position
    return (text_surface, rect)
    

def position_food(exceptions, screen_width, screen_height):
    '''Chooses a random position for food.'''
    while True:
        x = randint(0, screen_width - 1)
        y = randint(0, screen_height - 1)
        if (x,y) not in exceptions:
            return (x, y)
        