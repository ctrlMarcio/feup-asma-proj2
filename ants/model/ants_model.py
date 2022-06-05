import ants.util.position as position_utils
from ants.agents.ant_agent import AntAgent
from ants.agents.food_agent import FoodAgent
from ants.agents.home_agent import HomeAgent
from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation


class AntsModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, food_sources=1, food_source_amount=25, display_view_distance=False, display_markers=False):
        self.num_agents = N
        self.space = ContinuousSpace(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.current_id = 0

        # configurable parameters
        self.food_sources = food_sources
        self.food_source_amount = food_source_amount
        self.display_view_distance = display_view_distance
        self.display_markers = display_markers

        self._create_agents()

    def get_random_location(self):
        x = self.random.randrange(self.space.width)
        y = self.random.randrange(self.space.height)

        return (x, y)

    def step(self):
        self.schedule.step()

    def _create_food_source(self):
        food_location = self.get_random_location()

        quantity = self.random.randrange(5, 20)

        # add base food source
        last_food_source = FoodAgent(
            self.next_id(), self, amount=self.food_source_amount)
        random_direction = None

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
        self.space.place_agent(home, self.get_random_location())

        # Create food source
        for _ in range(self.food_sources):
            self._create_food_source()

        # Create ants
        self._create_ants(home)
