from ants.agents.food_agent import FoodAgent
from ants.util.state_machine import StateMachine
import ants.util.position as position_utils


class AntStateMachine:

    EXPLORING_STATE = "EXPLORING"
    GOING_TO_FOOD = "GOING_TO_FOOD"
    END_STATE = "END"

    def __init__(self, ant):
        self.state_machine = StateMachine()
        self.ant = ant
        self.food_target = None

        self._config_state_machine()

    def step(self):
        return self.state_machine.step()

    def _config_state_machine(self):
        self.state_machine.add_state(
            AntStateMachine.EXPLORING_STATE, self._exploring_handle)
        self.state_machine.add_state(
            AntStateMachine.GOING_TO_FOOD, self._going_to_food_handle)
        self.state_machine.add_state(
            AntStateMachine.END_STATE, self._end_handle, end_state=1)

        self.state_machine.set_start(AntStateMachine.EXPLORING_STATE)

    def _exploring_handle(self):
        # move ant to right
        self.ant.wander()

        space = self.ant.model.space

        # check if is there food nearby
        neighbours = space.get_neighbors(
            self.ant.pos, 30, include_center=True)  # todo: remove hardcoded lookup radius
        # filter out food agents
        food_neighbours = [n for n in neighbours if isinstance(n, FoodAgent)]

        if len(food_neighbours) > 0:
            # todo: find nearest food source and go to it
            self.food_target = food_neighbours[0]  # search on this
            return AntStateMachine.GOING_TO_FOOD

        return AntStateMachine.EXPLORING_STATE

    def _going_to_food_handle(self):
        if self.food_target is None or self.food_target.amount == 0:
            # check if is there food nearby
            neighbours = self.ant.model.space.get_neighbors(
                self.ant.pos, 30, include_center=True)  # todo: remove hardcoded lookup radius
            # filter out food agents
            food_neighbours = [
                n for n in neighbours if isinstance(n, FoodAgent)]

            if len(food_neighbours) > 0:
                # todo: find nearest food source and go to it
                self.food_target = food_neighbours[0]  # search on this
                return AntStateMachine.GOING_TO_FOOD

            return AntStateMachine.EXPLORING_STATE
        # move ant to food
        self.ant.go_to(self.food_target.pos)

        # check if food is reached
        # todo: replace hardcoded value
        if position_utils.euclidean_distance(self.ant.pos, self.food_target.pos) < 2:
            self.food_target.reduce()
            return AntStateMachine.EXPLORING_STATE

        return AntStateMachine.GOING_TO_FOOD

    def _end_handle(self):
        # TODO
        pass
