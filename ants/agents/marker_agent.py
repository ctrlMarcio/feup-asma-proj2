from enum import Enum
from mesa import Agent


class MarkerType(Enum):
    """
    Enum for marker types
    """
    UNKNOWN = "255, 165, 0"
    HOME = "135, 206, 250"
    FOOD = "60, 179, 113"


class MarkerAgent(Agent):

    LIFESPAN = 1000  # in steps

    def __init__(self, unique_id, model, steps, life=LIFESPAN, type=MarkerType.UNKNOWN):
        super().__init__(unique_id, model)
        self.life = life
        self.type = type
        self.steps = steps

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
                "Color": f"rgba({self.type.value}, {self.life/MarkerAgent.LIFESPAN})",
                "Layer": 0,
                "Alpha": 0}
