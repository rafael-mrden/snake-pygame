from random import randint, shuffle
from pygame.math import Vector2
import networkx as nx

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


def make_graph(body, sw, sh):
    '''Makes graph from the complement of the body of the snake.'''
    
    vertices = [(i,j) for i in range(sw) for j in range(sh) if (i,j) not in body]
    
    edges = { v : [ modulo(Vector2(v) + Vector2(d), sw, sh) for d in [(1, 0), (-1, 0), (0, 1), (0, -1)] \
                if modulo(Vector2(v) + Vector2(d), sw, sh) not in body] \
                    for v in vertices }
    
    G = nx.Graph(edges)
    return G


def make_decision(head, body, direction, food, sw, sh):
    '''Where should snake make the next step.
    Many small optimizations are possible.'''
    
    #return an_obvious_boring_solution(head, body, direction, food, sw, sh)
    
    head = Vector2(head)
    direction = Vector2(direction)
    food = Vector2(food)
    
    directions = [v for v in [Vector2(v_) for v_ in [(1, 0), (-1, 0), (0, 1), (0, -1)]] \
                        if (v != -direction) and (modulo(head + v, sw, sh) not in body)]
    
    if directions == []: # Too bad. Game over in the next step
        return direction
    
    if len(directions) == 1: # No choice
        return directions[0]
    
    current_distance = torus_distance(head, food, sw, sh)
    complement_graph = make_graph(body, sw, sh)
    
    directions_open_path = {} # Here we will record whether it is possible
                              # to reach food by moving in the directions.
    
    for i in range(len(directions)):
        v = directions[i]
        new_head = Vector2(modulo(head + v, sw, sh))
        
        # Do we get closer to food?
        shorter_path = (torus_distance(new_head, food, sw, sh) < current_distance)
        
        # Is it even possible to reach food this way?
        open_path = nx.has_path(complement_graph, modulo(new_head, sw, sh), modulo(food, sw, sh))
        if open_path and shorter_path:
            return v
        
        directions_open_path[i] = open_path
    
    restricted_directions = [v for v in directions if directions_open_path[directions.index(v)] == True]

    if restricted_directions != []:
        return restricted_directions[0]
    
    # Here we know that none of the directions will lead to the food's connected component.
    # So we choose a directions which leads to the largest connected component.
    directions_length_component = {}
    
    for i in range(len(directions)):
        v = directions[i]
        new_head = Vector2(modulo(head + v, sw, sh))

        directions_length_component[i] = len(nx.node_connected_component(complement_graph, modulo(new_head, sw, sh)))   
        print(f'calculated component: {directions_length_component[i]}')
        
    max_length = max(directions_length_component.values())
    indices_with_max_length = [i for i in range(len(directions)) if directions_length_component[i] == max_length]
    
    return directions[indices_with_max_length[0]]
    

def an_obvious_boring_solution(head, body, direction, food, sw, sh):
    # Assumes that initial_direction is (1, 0)
    
    initial_direction = (1, 0)
    othogonal_direction = initial_direction[::-1]
    
    if direction == othogonal_direction:
        return initial_direction
    
    if direction == initial_direction:
        new_head = modulo(Vector2(head) + Vector2(initial_direction), sw, sh)
        if new_head in body or \
            (len(body) < sw and head[0] == 0):
            return othogonal_direction
        
        else:
            return initial_direction


