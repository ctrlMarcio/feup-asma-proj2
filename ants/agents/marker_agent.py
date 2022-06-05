from enum import Enum
from mesa import Agent


class MarkerType(Enum):
    """
    Enum for marker types
    """
    UNKNOWN = "255, 165, 0"
    HOME = "213, 117, 255"
    FOOD = "0, 156, 13"


class MarkerAgent(Agent):

    LIFESPAN = 1000  # in steps

    def __init__(self, unique_id, model, steps, life=LIFESPAN, type=MarkerType.UNKNOWN):
        super().__init__(unique_id, model)
        self.life = life
        self.type = type
        self.steps = steps

    def die(self):
        self.model.schedule.remove(self)
        self.model.space.remove_agent(self)

    def step(self):
        self.life -= 1
        if self.life <= 0:
            self.die()

    def get_portrayal(self):
        if self.model.display_markers:
            return {"Shape": "rect",
                    "Filled": "true",
                    "w": 0.005 * self.life/MarkerAgent.LIFESPAN,
                    "h": 0.005 * self.life/MarkerAgent.LIFESPAN,
                    "Color": f"rgba({self.type.value}, {self.life/MarkerAgent.LIFESPAN})",
                    "Layer": 0}

        return None
