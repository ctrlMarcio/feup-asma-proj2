from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from ants.agents.ant_agent import AntAgent
from ants.agents.home_agent import HomeAgent


class AntsModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        self.num_agents = N
        self.space = ContinuousSpace(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        self._create_agents()

    def get_random_location(self):
        x = self.random.randrange(self.space.width)
        y = self.random.randrange(self.space.height)

        return (x, y)

    def step(self):
        self.schedule.step()

    def _create_agents(self):
        # Create home
        home = HomeAgent(0, self)
        # adding to scheduler because the view go gets the agents at the scheduler
        # alternatively, we could have an array of "drawable agents" in here and we could retrieve it from there
        # but in the future we could be adding new ants or something and the scheduler in the home agent might make
        #   sense
        self.schedule.add(home)
        self.space.place_agent(home, self.get_random_location())

        # Create agents
        for i in range(self.num_agents):
            a = AntAgent(i + 1, self)  # i + 1 because home agent is 0
            self.schedule.add(a)
            # Add the agent to a random grid cell
            self.space.place_agent(a, home.pos)
