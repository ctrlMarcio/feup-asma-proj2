from mesa.visualization.ModularVisualization import VisualizationElement
import numpy as np

from ants.agents.ant_agent import AntAgent


class HistogramModule(VisualizationElement):
    local_includes = ["ants/view/histogram_module.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = "new HistogramModule({}, {}, {})"
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        all_agents = model.schedule.agents
        # get all agents that are Ants
        ants = [a for a in all_agents if isinstance(a, AntAgent)]
        life_vals = [agent.life_left() * 100 for agent in ants]
        hist = np.histogram(life_vals, bins=self.bins)[0]
        return [int(x) for x in hist]
