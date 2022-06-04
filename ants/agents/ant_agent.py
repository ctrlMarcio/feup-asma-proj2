import math
from mesa import Agent
from ants.agents.food_agent import FoodAgent
from ants.agents.marker_agent import MarkerAgent, MarkerType

from ants.behaviour.ant_state_machine import AntStateMachine


class AntAgent(Agent):

    STEP_SIZE = 0.1
    MAX_ANGLE_CHANGE = 1

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        self.ant_state_machine = AntStateMachine(self)
        # random number between 0 and 360
        self.direction = self.random.random() * 360

        self.has_food = False

    def _calculate_new_pos(self):
        # calculates the new position of the agent
        new_x = self.pos[0] + AntAgent.STEP_SIZE * math.cos(self.direction)
        new_y = self.pos[1] + AntAgent.STEP_SIZE * math.sin(self.direction)
        return (new_x, new_y)

    def _move(self):
        try:
            pos = self._calculate_new_pos()
            pos = self.model.space.torus_adj(pos)
            self.pos = pos
        except:
            self.direction += 180
            self.direction %= 360

    def step(self):
        self.ant_state_machine.step()

    def take_food(self):
        self.has_food = True

    def drop_food(self):
        self.has_food = False

    def get_nearest_food_source(self):
        space = self.model.space

        # check if is there food nearby
        neighbours = space.get_neighbors(
            self.pos, 5, include_center=True)  # todo: remove hardcoded lookup radius
        # filter out food agents
        food_neighbours = [n for n in neighbours if isinstance(n, FoodAgent)]

        if len(food_neighbours) == 0:
            return None

        # an optimization could be done to return the nearest food source
        return food_neighbours[0]

    def drop_marker(self, type: MarkerType):
        marker = MarkerAgent(self.model.next_id(),
                             self.model, type=type)
        self.model.schedule.add(marker)
        self.model.space.place_agent(marker, self.pos)

    def go_to(self, position):
        # moves the agent towards a position
        myradians = math.atan2(
            position[1]-self.pos[1], position[0]-self.pos[0])

        direction = math.degrees(myradians)
        self.direction = direction

        self._move()

    def wander(self):
        # moves the agent in a random direction
        self.direction += self.random.random() * (AntAgent.MAX_ANGLE_CHANGE * 2) - \
            AntAgent.MAX_ANGLE_CHANGE
        self.direction %= 360

        self._move()

    def get_portrayal(self):
        return {"Shape": "circle",
                "Filled": "true",
                "r": 1.5,
                "Color": "red",
                "Layer": 1}
