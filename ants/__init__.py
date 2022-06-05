from mesa.visualization.ModularVisualization import ModularServer, UserSettableParameter
from numpy import number
from ants.model.ants_model import AntsModel
from ants.view.simple_continuous_canvas import SimpleContinuousCanvas


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

    home_x_option = UserSettableParameter(
        "number", "Home x", value=-1)
    home_y_option = UserSettableParameter(
        "number", "Home y", value=-1)

    food_source_scenario_option = UserSettableParameter(
        "choice", "Food source scenario", choices=["no scenario", "scenario 1", "scenario 2"], value="no scenario")

    server = ModularServer(AntsModel,
                           [canvas],
                           "Ants Model",
                           {
                               "placeholder_1": UserSettableParameter('static_text', value="Model settings"),
                               "N": number_of_ants_option, "width": environment["width"], "height": environment["height"],
                               "food_sources": food_sources_option,
                               "food_source_amount": food_source_amount_option,
                               "food_source_scenario": food_source_scenario_option,
                               "home_x": home_x_option,
                               "home_y": home_y_option,
                               "placeholder_2": UserSettableParameter('static_text', value="Display settings"),
                               "display_view_distance": display_view_distance_option,
                               "display_markers": display_markers_option,
                           })
    server.port = 8521  # The default
    server.launch()
