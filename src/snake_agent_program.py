"""
You can import modules if you need
NOTE:
your code must function properly without 
requiring the installation of any additional 
dependencies beyond those already included in 
the Python package une_ai
"""
import math
from une_ai.models import GridMap
from snake_agent import SnakeAgent
import numpy as np
from queue import Queue, LifoQueue, PriorityQueue
from prioritized_item import PrioritizedItem
from une_ai.models import GraphNode

envirnment_map = None #GridMap(64, 48, True)

def isvalid_coord(coord):
    """Checks that a coordinate in the environment is valid i.e. within bounds
    Arguments:
        coord - a tuple if the x and y coordinates to be checked
        return - boolean
    """
    global envirnment_map
    try: 
        value = envirnment_map.get_item_value(coord[0], coord[1])
        return value
    except:
        return False

def adjacent_tiles(node, body, direction):
    """ Retrieves all nodes adjacent to the current node.
    Arguments:
        node - the node whose neighbours we want to retrieve
        body - an array of the coordinates of the snakes body
        direction - the travel direction of the snake
        return - an list containing the adjacent nodes
    """
    global envirnment_map
    tiles = [] # List to add nodes
    node_coordinates = node.get_state()
    x = node_coordinates[0]
    y = node_coordinates[1]
    for offset in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        coord = (x + offset[0], y + offset[1])
        # Ensures this coordinate are not part of the snake's body
        if isvalid_coord(coord) and not coord in body and not coord == get_next_to_tail(body, direction):
            cost = 1
            child_node = GraphNode(coord, node, get_direction(node_coordinates, coord, direction), cost)
            tiles.append(child_node)
    return tiles 
           
	
def get_direction(cur_pos, next_pos, direction):
    """ Selects move action based on current and future coordinates
    Arguments:
        cur_pos - the current coordinats of the snake's head
        next_pos - the future coordinate of the snake's head
        direction - the current travel direction
    """
    if next_pos[0] < cur_pos[0]: 
        return 'move-left'
    if next_pos[0] > cur_pos[0]:
        return 'move-right'
    if next_pos[1] > cur_pos[1]:
        return 'move-down'
    return 'move-up'
    
    return 'move-' + direction
"""
TODO:
You must implement this function with the
agent program for your snake agent.
Please, make sure that the code and implementation 
of your agent program reflects the requirements in
the assignment. Deviating from the requirements
may result to score a 0 mark in the
agent program criterion.

Please, do not change the parameters of this function.
"""

current_food = None # Holds the current food coordinates
path_to_food = []

def snake_agent_program(percepts, actuators):

    actions = []
    global envirnment_map, path_to_food
    body = percepts['body-sensor']
    head = body[0]
    # Initialze a model of the environment, marking obstacles
    if envirnment_map is None:
        obstacles = percepts['obstacles-sensor']
        envirnment_map = GridMap(64, 48, True)
        for obsacle in obstacles:
            envirnment_map.set_item_value(obsacle[0], obsacle[1], False)
    
    food_locations = percepts['food-sensor']
    food_locations.sort(key = lambda x: distance_between_points(x, head))
    #food_locations.sort(key = lambda x: x[2]) 

    if len(food_locations) > 0:
        target = food_locations[0]
        global current_food

        if current_food != target:
            current_food = target
            # Search goal starting from head
            goal_node = breadth_first_search(body[0], body, is_current_food, actuators['head'])

            if goal_node:
                path_to_food, cost = goal_node.get_path()
        if len(path_to_food) == 1: # If food is one tile away
            actions.append('open-mouth')
        else:
            actions.append('close-mouth')

        if len(path_to_food) > 0:
            current_action = path_to_food.pop(0)
            if current_action is not None:
                actions.append(current_action)
    
    return actions

def is_current_food(node_state):
    global current_food
    if node_state[0] == current_food[0] and node_state[1] == current_food[1]:
        return True
    return False

def breadth_first_search(start_coords, body, goal_function, direction):
    """ Adapted from lecture code
    Returns node validate by goal function
    Arguments:
        start_coords - a tuple of coordinates to start from
        goal_function - a funtion to confirm that goal has been reached
        direction - direction of movement of the dnake
        return - a GraphNode representing the coordinates of the goal
    """

    initial_state = GraphNode(start_coords, None, None, 0)

    if goal_function(initial_state.get_state()):
        return initial_state
    
    frontier = Queue() 
    frontier.put(initial_state)
    reached = [initial_state.get_state()]

    while frontier.qsize() > 0:
        cur_node = frontier.get()
        successors = adjacent_tiles(cur_node, body, direction)
        
        for successor in successors:
            if goal_function(successor.get_state()):
                return successor
            
            successor_state = successor.get_state()

            if not successor_state in reached:
                reached.append(successor_state)
                frontier.put(successor)
        
    return False

def get_next_to_tail(body, direction):
    """ Returns the coordinates of the tile behind the tail. Used to eliminate backeard path
    Arguments:
        body - a list of the coordinates that represent the snake's body
        diredtion - the travel direction of the snake
    """
    if len(body) == 1:
        head = body[0]
        x, y = head[0], head[1]
        return (x, y+1) if direction == 'up' else (x, y-1) if direction == 'down' else (x-1, y) if direction == 'right'\
        else (x+1, y)
    
    last, second_last = body[-1], body[-2]

    if last[0] < second_last[0]: # Moving left
        return (last[0] - 1, last[1])
    if last[0] > second_last[0]: # Moving right
        return (last[0] + 1, last[1])
    if last[1] < second_last[1]: # Moving down
        return (last[0], last[1] - 1)
    return (last[0], last[1] + 1) # Moving up

def distance_between_points(point_1, point_2):
    """ Calculates distance between points
    Argument:
        ponts_1 - coordinates of the initial point
        ponts_2 - coordinates of the target point
        return - the calculated distance betwwen the points
    """
    return math.sqrt(pow(point_1[0] - point_2[0], 2) + pow(point_1[1] - point_2[1], 2))

def net_cost(food_items, body, goal_function, direction):
    path = []
    net_cost = -1000
    for food in food_items:
        node = breadth_first_search(body[0], body, lambda x: x[0]==food[0] and x[1]==food[1], direction)
        food_path, cost = node.get_path()
        net = food[2] - cost
        if net > net_cost:
            path = food_path
    return path

def heuristic_cost(current_node, goal_function):
    # Compute the straight distance
    # from the current_node to all goal states
    straight_distances = []
    for x in range(0, w_env):
        for y in range(0, h_env):
            if goal_function((x, y)):
                cur_dist = math.sqrt((current_node[0] - x)**2 + (current_node[1] - y)**2)
                straight_distances.append(cur_dist)
        
    # return the minimum cost among the computed distances
    return np.min(straight_distances)

# Finally, we can implement the A* start search
# In this scenario, the costs are uniform (all 1) so 
# The A* search will return the same solutions as the greedy-best first search
# However, the implementation will be sligthly different
def A_star_search(start_coords, goal_function):
    # You can start from the implementation of the greedy-best first search
    # However, the priority value will not only be the heuristic cost
    # predicted by the heuristic function, but a sum of that cost and
    # the cost of the path to reach the node

    initial_state = GraphNode(start_coords, None, None, 0)
    if goal_function(initial_state.get_state()):
        return initial_state
    frontier = PriorityQueue()
    # THESE LINES CHANGED
    _, g = initial_state.get_path()
    h = heuristic_cost(initial_state.get_state(), goal_function)
    frontier.put(PrioritizedItem(g+h, initial_state))
    # ------
    reached = [initial_state.get_state()]
    while frontier.qsize() > 0:
        cur_item = frontier.get()
        cur_node = cur_item.item
        successors = adjacent_tiles(cur_node)
        for successor in successors:
            if goal_function(successor.get_state()):
                return successor
            successor_state = successor.get_state()
            if successor_state not in reached:
                reached.append(successor_state)
                # THESE LINES CHANGED
                _, g = successor.get_path()
                h = heuristic_cost(successor.get_state(), goal_function)
                frontier.put(PrioritizedItem(g+h, successor))
                # -----
    return False

def total_cost(stgart_cord, destinations):
    total_cost = 0
    start = stgart_cord
    for destination in destinations:
        total_cost += math.sqrt((start[0] - destination[0])**2 + (start[0] - destination[0])**2)
        start = destination
    return total_cost