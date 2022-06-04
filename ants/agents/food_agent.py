from mesa import Agent


class FoodAgent(Agent):

    DEFAULT_AMOUNT = 10

    def __init__(self, unique_id, model, amount=DEFAULT_AMOUNT):
        super().__init__(unique_id, model)
        self.amount = amount

    def reduce(self):
        self.amount -= 1

        if self.amount <= 0:
            self.model.schedule.remove(self)
            self.model.space.remove_agent(self)

            return None

        return self.amount

    def get_portrayal(self):
        return {"Shape": "circle",
                "Filled": "true",
                "r": 5 * self.amount/FoodAgent.DEFAULT_AMOUNT,
                "Color": "#00ff3c",
                "Layer": 0}
