from mesa import Agent


class HomeAgent(Agent):
    def __init__(self, unique_id, model):
        # since there is only 1 home, it's ID is always 0 and unique
        super().__init__(unique_id, model)

    @staticmethod
    def get_portrayal():
        return {"Shape": "circle",
                "Filled": "true",
                "r": 5,
                "Color": "blue",
                "Layer": 0}
