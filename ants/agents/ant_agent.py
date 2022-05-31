from mesa import Agent

from ants.movement.ant_state_machine import AntStateMachine


class AntAgent(Agent):

    STEP_SIZE = 0.1

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        self.ant_state_machine = AntStateMachine(self)

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
        # get random number between -STEP_SIZE and STEP_SIZE
        x_step = self.STEP_SIZE * (2 * self.random.random() - 1)
        y_step = self.STEP_SIZE * (2 * self.random.random() - 1)
        self.pos = (self.pos[0] + x_step, self.pos[1] + y_step)
