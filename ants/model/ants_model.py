import math
import ants.util.position as position_utils
from ants.agents.ant_agent import AntAgent
from ants.agents.food_agent import FoodAgent
from ants.agents.home_agent import HomeAgent
from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


class AntsModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, food_sources=1, food_source_amount=25, display_view_distance=False, display_markers=False, home_x=-1, home_y=-1, food_source_scenario="no scenario", ant_freedom_coefficient=0.25, ant_direction_noise=90):
        self.num_agents = N
        self.space = ContinuousSpace(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.current_id = 0

        # configurable parameters
        self.home_location = (home_x, home_y)
        self.food_source_scenario = food_source_scenario
        self.food_sources = food_sources if self.food_source_scenario == "no scenario" else 1
        self.food_source_amount = food_source_amount
        self.display_view_distance = display_view_distance
        self.display_markers = display_markers
        self.ant_freedom_coefficient = ant_freedom_coefficient
        self.ant_direction_noise = ant_direction_noise

        self._config_collector()
        self._create_agents()
        self.datacollector.collect(self)

    def get_random_location(self):
        x = self.random.randrange(self.space.width)
        y = self.random.randrange(self.space.height)

        return (x, y)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def _create_food_source(self):
        if self.food_source_scenario == "no scenario":
            food_location = self.get_random_location()
            quantity = self.random.randrange(5, 20)
        elif self.food_source_scenario == "scenario 1":
            food_location = (10, 10)
            quantity = 5
        elif self.food_source_scenario == "scenario 2":
            food_location = (300, 300)
            quantity = 10

        # add base food source
        last_food_source = FoodAgent(
            self.next_id(), self, amount=self.food_source_amount)
        random_direction = None

        self.food_in_sources_amount += (self.food_source_amount * quantity)

        self.schedule.add(last_food_source)
        self.space.place_agent(last_food_source, food_location)

        for i in range(1, quantity):
            # calculate next food source based on a an adjacent direction
            _, random_direction = position_utils.get_random_direction(
                [random_direction] if random_direction else [])
            food_location = position_utils.add_to_position(
                last_food_source.pos, position_utils.scale_position(random_direction, 2))

            if (self.space.out_of_bounds(food_location)):
                i -= 1
                continue

            last_food_source = FoodAgent(
                self.next_id(), self, amount=self.food_source_amount)

            self.schedule.add(last_food_source)
            self.space.place_agent(last_food_source, food_location)

            # calculate distance to home
            if self.best_distance < 0:
                self.best_distance = 2 * math.dist(
                    food_location, self.home_location)

    def _create_ants(self, home):
        for _ in range(self.num_agents):
            a = AntAgent(self.next_id(), self)  # i + 1 because home agent is 0
            self.schedule.add(a)
            # Add the agent to a random grid cell
            self.space.place_agent(a, home.pos)

    def _create_agents(self):
        # Create home
        home = HomeAgent(self.next_id(), self)
        # adding to scheduler because the view go gets the agents at the scheduler
        # alternatively, we could have an array of "drawable agents" in here and we could retrieve it from there
        # but in the future we could be adding new ants or something and the scheduler in the home agent might make
        #   sense
        self.schedule.add(home)

        if self.home_location[0] == -1 and self.home_location[1] == -1:
            self.home_location = self.get_random_location()
            self.space.place_agent(home, self.home_location)
        else:
            self.space.place_agent(home, self.home_location)

        # Create food source
        for _ in range(self.food_sources):
            self._create_food_source()

        # Create ants
        self._create_ants(home)

    def _config_collector(self):
        self.food_in_sources_amount = 0
        self.food_in_home_amount = 0

        self.best_distance = -1

        self.datacollector = DataCollector(
            model_reporters={
                "Food in Sources": lambda m: m.food_in_sources_amount,
                "Food at Home": lambda m: m.food_in_home_amount,
                "Min Distance": lambda m: m._get_min_distance(),
                "Best Distance": lambda m: m.best_distance,
            },)

    def _get_mean_distance(self):
        total_distance = 0
        amount = 0
        for agent in self.schedule.agents:
            if isinstance(agent, AntAgent) \
                    and not agent.has_food \
                    and agent.commit_distance_food_home > 0:
                total_distance += agent.commit_distance_food_home
                amount += 1

        if amount > 0:
            return total_distance / amount
        else:
            return 0

    def _get_min_distance(self):
        min_distance = 0
        for agent in self.schedule.agents:
            if isinstance(agent, AntAgent) \
                    and agent.commit_distance_food_home > 0:
                if min_distance == 0 or agent.commit_distance_food_home < min_distance:
                    min_distance = agent.commit_distance_food_home

        return min_distance
