from mesa import Agent


class HomeAgent(Agent):
    def __init__(self, unique_id, model):
        # since there is only 1 home, it's ID is always 0 and unique
        super().__init__(unique_id, model)

    def get_portrayal(self):
        return {"Shape": "circle",
                "Filled": "true",
                "r": 15,
                "Color": "blue",
                "Layer": 0}
