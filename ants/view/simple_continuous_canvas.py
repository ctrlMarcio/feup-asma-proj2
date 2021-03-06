from mesa.visualization.ModularVisualization import VisualizationElement


class SimpleContinuousCanvas(VisualizationElement):
    local_includes = ["ants/view/simple_continuous_canvas.js"]
    canvas_height = 500
    canvas_width = 500

    def __init__(self, canvas_height=500, canvas_width=500):
        """
        Instantiate a new SimpleCanvas
        """
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = "new Simple_Continuous_Module({}, {})".format(
            self.canvas_width, self.canvas_height
        )
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        space_state = []
        for obj in model.schedule.agents:
            portrayal = obj.get_portrayal()

            if portrayal is None:
                continue

            x, y = self._get_x_y(model, obj)
            # portrayal is a list, then is a list of portrayal dicts
            if isinstance(portrayal, list):
                for portrayal_dict in portrayal:
                    portrayal_dict["x"] = x
                    portrayal_dict["y"] = y
                    space_state.append(portrayal_dict)
            else:
                portrayal["x"] = x
                portrayal["y"] = y
                space_state.append(portrayal)

        return space_state

    def _get_x_y(self, model, obj):
        x, y = obj.pos
        x = (x - model.space.x_min) / \
            (model.space.x_max - model.space.x_min)
        y = (y - model.space.y_min) / \
            (model.space.y_max - model.space.y_min)
        return x, y
