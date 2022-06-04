from enum import Enum
from mesa import Agent


class MarkerType(Enum):
    """
    Enum for marker types
    """
    UNKNOWN = "orange"
    HOME = "blue"
    FOOD = "green"


class MarkerAgent(Agent):

    LIFESPAN = 1000  # in steps

    def __init__(self, unique_id, model, life=LIFESPAN, type=MarkerType.UNKNOWN):
        super().__init__(unique_id, model)
        self.life = life
        self.type = type

    def step(self):
        self.life -= 1
        if self.life <= 0:
            self.model.schedule.remove(self)
            self.model.space.remove_agent(self)

    def get_portrayal(self):
        return {"Shape": "rect",
                "Filled": "true",
                "w": 0.005 * self.life/MarkerAgent.LIFESPAN,
                "h": 0.005 * self.life/MarkerAgent.LIFESPAN,
                "Color": self.type.value,
                "Layer": 0}
