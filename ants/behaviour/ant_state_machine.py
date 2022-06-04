from ants.agents.marker_agent import MarkerAgent, MarkerType
from ants.util.state_machine import StateMachine


class AntStateMachine:

    EXPLORING_STATE = "EXPLORING"
    GOING_TO_FOOD = "GOING_TO_FOOD"
    GOING_TO_HOME = "GOING_TO_HOME"
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
            AntStateMachine.GOING_TO_HOME, self._going_to_home_handle)
        self.state_machine.add_state(
            AntStateMachine.END_STATE, self._end_handle, end_state=1)

        self.state_machine.set_start(AntStateMachine.EXPLORING_STATE)

    def _exploring_handle(self):
        self.ant.wander()

        # drop marker
        if self.ant.model.schedule.steps % 5 == 0:
            self.ant.drop_marker(MarkerType.HOME)

        # check if ant is near food
        nearest_food_source = self.ant.get_nearest_food_source()

        if nearest_food_source is not None:
            self.food_target = nearest_food_source
            return AntStateMachine.GOING_TO_FOOD

        return AntStateMachine.EXPLORING_STATE

    def _going_to_food_handle(self):
        if self.food_target is None or self.food_target.amount == 0:
            # this occurs when an ant selects a food source and then the food source is removed
            return AntStateMachine.EXPLORING_STATE

        # drop marker
        if self.ant.model.schedule.steps % 5 == 0:
            self.ant.drop_marker(MarkerType.HOME)

        # move ant to food
        self.ant.go_to(self.food_target.pos)

        space = self.ant.model.space

        # todo: replace hardcoded value
        if space.get_distance(self.ant.pos, self.food_target.pos) <= 2:
            self.ant.take_food()
            self.food_target.reduce()
            return AntStateMachine.GOING_TO_HOME

        return AntStateMachine.GOING_TO_FOOD

    def _going_to_home_handle(self):
        self.ant.wander()

        # drop marker
        if self.ant.model.schedule.steps % 5 == 0:
            self.ant.drop_marker(MarkerType.FOOD)

        # implement follow markers
        return AntStateMachine.GOING_TO_HOME

    def _end_handle(self):
        # TODO
        pass
