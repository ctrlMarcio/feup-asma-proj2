from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from ants.agents.ant_agent import AntAgent
from ants.model.ants_model import AntsModel
from ants.view.simple_continuous_canvas import SimpleContinuousCanvas


def main():
    environment = {
        "width": 500,
        "height": 500,
    }

    canvas = SimpleContinuousCanvas(
        environment["width"], environment["height"])

    server = ModularServer(AntsModel,
                           [canvas],
                           "Ants Model",
                           {"N": 10, "width": environment["width"], "height": environment["height"]})
    server.port = 8521  # The default
    server.launch()
