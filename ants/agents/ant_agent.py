import math
from mesa import Agent

from ants.movement.ant_state_machine import AntStateMachine


class AntAgent(Agent):

    STEP_SIZE = 0.1
    MAX_ANGLE_CHANGE = 1

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        self.ant_state_machine = AntStateMachine(self)
        # random number between 0 and 360
        self.direction = self.random.random() * 360

    @staticmethod
    def get_portrayal():
        return {"Shape": "circle",
                "Filled": "true",
                "r": 1,
                "Color": "red",
                "Layer": 0}

    def step(self):
        self.ant_state_machine.step()

    def wander(self):
        # moves the agent in a random direction
        self.direction += self.random.random() * (AntAgent.MAX_ANGLE_CHANGE * 2) - \
            AntAgent.MAX_ANGLE_CHANGE
        self.direction %= 360
        self.pos = self._calculate_new_pos()

    def _calculate_new_pos(self):
        # calculates the new position of the agent
        new_x = self.pos[0] + AntAgent.STEP_SIZE * math.cos(self.direction)
        new_y = self.pos[1] + AntAgent.STEP_SIZE * math.sin(self.direction)
        return (new_x, new_y)
