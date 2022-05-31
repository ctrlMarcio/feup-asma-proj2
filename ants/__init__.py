from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from ants.model.ants_model import AntsModel

def main():
    
    def agent_portrayal(agent):
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "r": 0.5}

        if agent.wealth > 0:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "grey"
            portrayal["Layer"] = 1
            portrayal["r"] = 0.2
        return portrayal


    grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

    server = ModularServer(AntsModel,
                        [grid],
                        "Ants Model",
                        {"N": 10, "width": 10, "height": 10})
    server.port = 8521  # The default
    server.launch()
