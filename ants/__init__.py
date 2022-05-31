from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from ants.agents.ant_agent import AntAgent
from ants.model.ants_model import AntsModel
from ants.view.simple_continuous_canvas import SimpleContinuousCanvas


def main():
    environment = {
        "width": 50,
        "height": 50,
    }

    canvas = SimpleContinuousCanvas(environment["width"] * 10, environment["height"] * 10)

    server = ModularServer(AntsModel,
                           [canvas],
                           "Ants Model",
                           {"N": 1, "width": environment["width"], "height": environment["height"]})
    server.port = 8521  # The default
    server.launch()
