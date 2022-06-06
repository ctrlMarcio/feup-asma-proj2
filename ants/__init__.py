from mesa.visualization.ModularVisualization import ModularServer, UserSettableParameter
from numpy import number
from ants.model.ants_model import AntsModel
from ants.view.simple_continuous_canvas import SimpleContinuousCanvas

from mesa.visualization.modules import ChartModule


def main():
    environment = {
        "width": 500,
        "height": 500,
    }

    canvas = SimpleContinuousCanvas(
        environment["width"], environment["height"])

    number_of_ants_option = UserSettableParameter(
        "slider", "Number of ants", value=100, max_value=500, min_value=1, step=1)
    life_of_ants_option = UserSettableParameter(
        "slider", "Life of ants", value=1000, min_value=100, max_value=10000, step=100)
    ratio_to_go_home_option = UserSettableParameter(
        "slider", "Ratio to go home", value=0.5, min_value=0.1, max_value=1, step=0.01)
    ratio_to_create_ants_option = UserSettableParameter(
        "slider", "Ratio to create ants", value=2, min_value=0.1, max_value=5, step=0.1)
    food_sources_option = UserSettableParameter(
        "slider", "Food sources", value=1, min_value=1, max_value=20, step=1)
    food_source_amount_option = UserSettableParameter(
        "slider", "Food source amount", value=25, min_value=1, max_value=200, step=1)
    ant_freedom_coefficient_option = UserSettableParameter(
        "slider", "Ant freedom coefficient (0-1)", value=0.25, min_value=0, max_value=1, step=0.01)
    ant_direction_noise = UserSettableParameter(
        "slider", "Ant direction noise (degrees)", value=180, min_value=0, max_value=360, step=1)
    display_view_distance_option = UserSettableParameter(
        "checkbox", "Display view distance", value=False)
    display_markers_option = UserSettableParameter(
        "checkbox", "Display markers", value=False)

    home_x_option = UserSettableParameter(
        "number", "Home x", value=-1)
    home_y_option = UserSettableParameter(
        "number", "Home y", value=-1)

    food_source_scenario_option = UserSettableParameter(
        "choice", "Food source scenario", choices=["no scenario", "scenario 1", "scenario 2"], value="no scenario")

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
        "Label": "Min Distance",
        "Color": "Red",
    }, {
        "Label": "Best Distance",
        "Color": "Black",
    }])

    ants_char = ChartModule([
        {
            "Label": "Number of Ants",
            "Color": "Green",
        }
    ])

    server = ModularServer(AntsModel,
                           [canvas, food_chart, tracks_chart, ants_char],
                           "Ants Model",
                           {
                               "placeholder_1": UserSettableParameter('static_text', value="Model settings"),
                               "N": number_of_ants_option, "width": environment["width"], "height": environment["height"],
                               "ants_life": life_of_ants_option,
                               "go_home_ratio": ratio_to_go_home_option,
                               "create_ants_ratio": ratio_to_create_ants_option,
                               "food_sources": food_sources_option,
                               "food_source_amount": food_source_amount_option,
                               "ant_freedom_coefficient": ant_freedom_coefficient_option,
                               "ant_direction_noise": ant_direction_noise,
                               "food_source_scenario": food_source_scenario_option,
                               "home_x": home_x_option,
                               "home_y": home_y_option,
                               "placeholder_2": UserSettableParameter('static_text', value="Display settings"),
                               "display_view_distance": display_view_distance_option,
                               "display_markers": display_markers_option,
                           })
    server.port = 8521  # The default
    server.launch()
