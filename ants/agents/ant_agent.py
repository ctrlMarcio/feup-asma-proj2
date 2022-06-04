import math
from typing import Tuple
from mesa import Agent
from ants.agents.marker_agent import MarkerAgent, MarkerType
from ants.agents.home_agent import HomeAgent

from ants.behaviour.ant_state_machine import AntStateMachine


class AntAgent(Agent):

    STEP_SIZE = 1
    MAX_ANGLE_CHANGE = 1

    # The rate at which the ant leaves markers in the environment, in frames.
    LEAVE_MARKERS_RATE = 5
    # The rate at which the ant looks for new markers
    FOLLOW_MARKERS_RATE = 3

    # The radius of the agent's vision for markers.
    VIEW_DISTANCE = 10

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        self.ant_state_machine = AntStateMachine(self)
        # random number between 0 and 360
        self.direction = self.random.random() * 360

    def get_portrayal(self):
        return [
            {
                "Shape": "circle",
                "Filled": True,
                "r": 1.5,
                "Color": "red",
                "Layer": 1
            },
            {
                "Shape": "circle",
                "Filled": False,
                "r": AntAgent.VIEW_DISTANCE,
                "Color": "red",
                "Layer": 1
            }]

    def step(self):
        self.ant_state_machine.step()

    def wander(self):
        # moves the agent in a random direction
        self.direction += self.random.random() * (AntAgent.MAX_ANGLE_CHANGE * 2) - \
            AntAgent.MAX_ANGLE_CHANGE
        self.direction %= 360

        self.move()

    def leave_marker(self) -> None:
        marker = MarkerAgent(self.model.next_id(), self.model)
        self.model.schedule.add(marker)
        self.model.space.place_agent(marker, self.pos)

    def is_near_marker(self, marker_type: MarkerType = None) -> bool:
        # returns true if the agent is near a marker
        for agent in self.model.space.get_neighbors(self.pos, AntAgent.VIEW_DISTANCE):
            if isinstance(agent, MarkerAgent):
                if marker_type is None or agent.type == marker_type:
                    return True

        return False

    def get_strongest_marker(self, marker_type: MarkerType = None) -> MarkerAgent:
        # returns the strongest marker in the agent's view
        best_marker = None
        # best life is the lowest possible
        best_life = float("inf")
        for agent in self.model.space.get_neighbors(self.pos, AntAgent.VIEW_DISTANCE):
            if isinstance(agent, MarkerAgent) \
                    and (marker_type is None or agent.type == marker_type) \
                    and agent.life < best_life:
                best_marker = agent
                best_life = agent.life

        return best_marker

    def get_home(self) -> HomeAgent:
        # returns the home agent of the agent
        for agent in self.model.space.get_neighbors(self.pos, AntAgent.VIEW_DISTANCE):
            if isinstance(agent, HomeAgent):
                return agent

        return None

    def move_in_direction(self, pos: Tuple[float, float]) -> None:
        # calculates the direction to the given position
        x = pos[0] - self.pos[0]
        y = pos[1] - self.pos[1]
        self.direction = math.atan2(y, x)

        self.move()

    def move(self) -> None:
        # moves the agent in the direction it is facing
        try:
            pos = self._calculate_new_pos()
            pos = self.model.space.torus_adj(pos)
            self.pos = pos
        except:
            self.direction += 180
            self.direction %= 360

    def _calculate_new_pos(self) -> Tuple[float, float]:
        # calculates the new position of the agent
        new_x = self.pos[0] + AntAgent.STEP_SIZE * math.cos(self.direction)
        new_y = self.pos[1] + AntAgent.STEP_SIZE * math.sin(self.direction)
        return (new_x, new_y)
