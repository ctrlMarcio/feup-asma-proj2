import math
from typing import Tuple
from mesa import Agent
from ants.agents.marker_agent import MarkerAgent, MarkerType
from ants.agents.home_agent import HomeAgent
from ants.agents.food_agent import FoodAgent

from ants.behaviour.ant_state_machine import AntStateMachine


class AntAgent(Agent):

    STEP_SIZE = 2.5
    WANDER_ANGLE_FREEDOM = 15

    # The rate at which the ant leaves markers in the environment, in frames.
    LEAVE_MARKERS_RATE = 5
    # The rate at which the ant looks for new markers
    FOLLOW_MARKERS_RATE = 5

    # The radius of the agent's vision for markers.
    VIEW_DISTANCE = 20
    # The position in which the agent can be considered **in** a position.
    # Basically the VIEW_DISTANCE for legs.
    POSITION_THRESHOLD = 20

    # Steps without getting food
    LIFE = 1000

    def __init__(self, unique_id, model, life=LIFE):
        super().__init__(unique_id, model)

        self.ant_state_machine = AntStateMachine(self)
        # random number between 0 and 360
        self.direction = self.random.random() * 360

        self.life = life
        self.max_life = life

        self.has_food = False
        self.seen_markers = set()

        self.step_count = 0
        self.distance_food_home = -1
        self.commit_distance_food_home = self.distance_food_home

        self.freedom_coefficient = model.ant_freedom_coefficient
        self.ant_direction_noise = model.ant_direction_noise

    def get_portrayal(self):
        ant_shape = {
            "Shape": "circle",
            "Filled": True,
            "r": 2,
            "Color": "red" if not self.has_food else "black",
            "Layer": 1
        }

        view_distance_shape = {
            "Shape": "circle",
            "Filled": False,
            "r": AntAgent.VIEW_DISTANCE,
            "Color": "red",
            "Layer": 1
        }

        food_shape = {
            "Shape": "circle",
            "Filled": True,
            "r": 0.5,
            "Color": "green",
            "Layer": 1
        }

        shapes = [ant_shape]

        if self.model.display_view_distance:
            shapes.append(view_distance_shape)

        if self.has_food:
            shapes.append(food_shape)

        return shapes

    def get_neighbours(self):
        neighbours = self.model.space.get_neighbors(
            self.pos, AntAgent.VIEW_DISTANCE)

        return neighbours

    def die(self):
        self.model.schedule.remove(self)
        self.model.space.remove_agent(self)

    def life_left(self):
        return self.life / self.max_life

    def reset_life(self):
        if self.model.food_in_home_amount > 0:
            self.life = self.max_life
            self.model.food_in_home_amount -= 0.5

        if self.model.food_in_home_amount >= self.model.num_agents * self.model.create_ants_ratio:
            self.model._create_ant(self.model.home_location)
            self.model.num_agents += 1
            self.model.food_in_home_amount -= 1

    def step(self):
        self.ant_state_machine.step()

        self.life -= 1
        self.distance_food_home += 1

        if self.life <= 0:
            self.die()
            self.model.num_agents -= 1

    def take_food(self):
        self.model.food_in_sources_amount -= 1
        self.has_food = True
        self.reset_step_counter()

    def drop_food(self):
        self.commit_distance_food_home = self.distance_food_home * \
            AntAgent.STEP_SIZE + 2*AntAgent.POSITION_THRESHOLD
        self.distance_food_home = 0
        self.model.food_in_home_amount += 1
        self.has_food = False
        self.reset_step_counter()

    def get_nearest_food_source(self, neighbours=None):
        if neighbours is None:
            neighbours = self.get_neighbours()

        # filter out food agents
        food_neighbours = [n for n in neighbours if isinstance(n, FoodAgent)]

        if len(food_neighbours) == 0:
            return None

        # an optimization could be done to return the nearest food source
        return food_neighbours[0]

    def drop_marker(self, type: MarkerType):
        marker = MarkerAgent(self.model.next_id(),
                             self.model, self.step_count, type=type)
        self.model.schedule.add(marker)
        self.model.space.place_agent(marker, self.pos)
        self.step_count += 1
        pass

    def go_to(self, position):
        # do this with 75% percentage
        if self.random.random() < self.freedom_coefficient:
            self.wander()
            return

        # moves the agent towards a position
        myradians = math.atan2(
            position[1]-self.pos[1], position[0]-self.pos[0])

        direction = math.degrees(myradians)
        self.direction = direction

        self.move()

    def wander(self):
        # moves the agent in a random direction
        self.direction += self.random.random() * AntAgent.WANDER_ANGLE_FREEDOM - \
            AntAgent.WANDER_ANGLE_FREEDOM/2
        self.direction %= 360

        self.move()

    def is_near_marker(self, marker_type: MarkerType = None, neighbours=None) -> bool:
        if neighbours is None:
            neighbours = self.get_neighbours()

        # returns true if the agent is near a marker
        for agent in neighbours:
            if isinstance(agent, MarkerAgent):
                if (marker_type is None or agent.type == marker_type) and agent.unique_id not in self.seen_markers:
                    return True

        return False

    def get_strongest_marker(self, marker_type: MarkerType = None, neighbours=None) -> MarkerAgent:
        if neighbours is None:
            neighbours = self.get_neighbours()

        # returns the strongest marker in the agent's view
        best_marker = None
        # best life is the lowest possible
        best_steps = float("inf")
        for agent in neighbours:
            if isinstance(agent, MarkerAgent):

                if (marker_type is None or agent.type == marker_type) \
                        and agent.steps < best_steps \
                        and agent.unique_id not in self.seen_markers:
                    best_marker = agent
                    best_steps = agent.steps

                self.seen_markers.add(agent.unique_id)

        return best_marker

    def get_home(self, neighbours=None) -> HomeAgent:
        if neighbours is None:
            neighbours = self.get_neighbours()

        # returns the home agent of the agent
        for agent in neighbours:
            if isinstance(agent, HomeAgent):
                return agent

        return None

    def move(self) -> None:
        # moves the agent in the direction it is facing
        try:
            pos = self._calculate_new_pos(self.direction + self.random.random(
            ) * self.ant_direction_noise - self.ant_direction_noise / 2)
            pos = self.model.space.torus_adj(pos)
            self.pos = pos
        except:
            self.direction += self.random.random() * 180 + 180
            self.direction %= 360

    def is_at(self, pos: Tuple[float, float]) -> bool:
        # returns true if the agent is at a position
        return self.model.space.get_distance(self.pos, pos) <= AntAgent.POSITION_THRESHOLD

    def reset_step_counter(self) -> None:
        self.step_count = 0
        self.seen_markers = set()

    def _calculate_new_pos(self, direction: float = None) -> Tuple[float, float]:
        # calculates the new position of the agent
        if direction is None:
            direction = self.direction

        return (self.pos[0] + math.cos(math.radians(direction)) * AntAgent.STEP_SIZE,
                self.pos[1] + math.sin(math.radians(direction)) * AntAgent.STEP_SIZE)
