from une_ai.models import Agent

class SnakeAgent(Agent):

    DIRECTIONS = ['up', 'down', 'left', 'right']

    # DO NOT CHANGE THE PARAMETERS OF THIS METHOD
    def __init__(self, agent_program):
        # DO NOT CHANGE THE FOLLOWING LINES OF CODE
        super().__init__("Snake Agent", agent_program)

        """
        If you need to add more instructions
        in the constructor, you can add them here
        """

    """
    TODO:
    In order for the agent to gain access to all 
    the sensors specified in the assignment's 
    requirements, it is essential to implement 
    this method.
    You can add a single sensor with the method:
    self.add_sensor(sensor_name, initial_value, validation_function)
    """
    def add_all_sensors(self):
        self.add_sensor('body-sensor', [], lambda v: isinstance(v, list) and all(isinstance(t, tuple) and len(t) == 2 and all(isinstance(ti, int) and ti >= 0 for ti in t) for t in v))
        self.add_sensor('food-sensor', [], lambda v: isinstance(v, list) and all(isinstance(t, tuple)
            and len(t) == 3 for t in v)  and all((isinstance(ti, int) for ti in t) for t in v))
        self.add_sensor('obstacles-sensor', [], lambda v: isinstance(v, list) and all(isinstance(t, tuple) and len(t) == 2 and all(isinstance(ti, int) and ti >= 0 for ti in t) for t in v))
        self.add_sensor('clock', 0, lambda v: isinstance(v, int) and v >= 0)


    """
    TODO:
    In order for the agent to gain access to all 
    the actuators specified in the assignment's 
    requirements, it is essential to implement 
    this method.
    You can add a single actuator with the method:
    self.add_actuator(actuator_name, initial_value, validation_function)
    """
    def add_all_actuators(self):
        self.add_actuator('head', None, lambda v: v in SnakeAgent.DIRECTIONS or v is None)
        self.add_actuator('mouth', 'open', lambda v: v in ['open', 'close'])

    """
    TODO:
    In order for the agent to gain access to all 
    the actions specified in the assignment's 
    requirements, it is essential to implement 
    this method.
    You can add a single action with the method:
    self.add_action(action_name, action_function)
    """
    def add_all_actions(self):
        self.add_action('move-up', lambda: {'head': 'up'} if not self.get_head_direction() == 'down' else {})
        self.add_action('move-down', lambda: {'head': 'down'} if not self.get_head_direction() == 'up' else {})
        self.add_action('move-left', lambda: {'head': 'left'} if not self.get_head_direction() == 'right' else {})
        self.add_action('move-right', lambda: {'head': 'right'} if not self.get_head_direction() == 'left' else {})
        self.add_action('open-mouth', lambda: {'mouth': 'open'})
        self.add_action('close-mouth', lambda: {'mouth': 'close'})

    def get_head_direction(self):
        return self.read_actuator_value('head')
    
    def get_mouth_status(self):
        return self.read_actuator_value('mouth')
    
    def get_head_coord(self):
        return self.read_sensor_value('body-sensor')[0]
    
