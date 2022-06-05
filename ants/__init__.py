from mesa.visualization.ModularVisualization import ModularServer, UserSettableParameter
from numpy import number
from ants.model.ants_model import AntsModel
from ants.view.simple_continuous_canvas import SimpleContinuousCanvas

from mesa.visualization.modules import ChartModule


def main():
    environment = {
        "width": 600,
        "height": 600,
    }

    canvas = SimpleContinuousCanvas(
        environment["width"], environment["height"])

    number_of_ants_option = UserSettableParameter(
        "number", "Number of ants", value=200, max_value=500)
    food_sources_option = UserSettableParameter(
        "number", "Food sources", value=1)
    food_source_amount_option = UserSettableParameter(
        "number", "Food source amount", value=25)
    display_view_distance_option = UserSettableParameter(
        "checkbox", "Display view distance", value=False)
    display_markers_option = UserSettableParameter(
        "checkbox", "Display markers", value=False)

    food_chart = ChartModule([{
        "Label": "Food in Sources",
        "Color": "Green",
    },
        {
        "Label": "Food at Home",
        "Color": "Blue",
    }
    ],
        data_collector_name='datacollector',)

    tracks_chart = ChartModule([{
        "Label": "Mean Distance",
        "Color": "Red",
    }])

    server = ModularServer(AntsModel,
                           [canvas, food_chart, tracks_chart],
                           "Ants Model",
                           {"N": number_of_ants_option, "width": environment["width"], "height": environment["height"],
                            "food_sources": food_sources_option,
                            "food_source_amount": food_source_amount_option,
                            "display_view_distance": display_view_distance_option,
                            "display_markers": display_markers_option})
    server.port = 8521  # The default
    server.launch()
