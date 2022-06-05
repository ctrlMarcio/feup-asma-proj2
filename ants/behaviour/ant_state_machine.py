from ants.agents.marker_agent import MarkerType
from ants.util.state_machine import StateMachine


class AntStateMachine:

    EXPLORING_STATE = "EXPLORING"
    GO_HOME_STATE = "GO_HOME"
    GO_FOOD_STATE = "GO_FOOD"
    END_STATE = "END"

    def __init__(self, ant):
        self.state_machine = StateMachine()
        self.ant = ant
        self.food_target = None

        self._config_state_machine()

    def step(self) -> bool:
        done = self.state_machine.step()
        if done:
            raise RuntimeError("Its over")

    def _config_state_machine(self) -> None:
        self.state_machine.add_state(
            AntStateMachine.EXPLORING_STATE, self._handle_exploring)
        self.state_machine.add_state(
            AntStateMachine.GO_FOOD_STATE, self._handle_going_to_food)
        self.state_machine.add_state(
            AntStateMachine.GO_HOME_STATE, self._handle_go_home)
        self.state_machine.add_state(
            AntStateMachine.END_STATE, self._handle_end, end_state=1)

        self.state_machine.set_start(AntStateMachine.EXPLORING_STATE)

    def _handle_exploring(self) -> str:
        if self.ant.get_home() is not None:
            self.ant.reset_step_counter()

        if self.ant.model.schedule.steps % self.ant.LEAVE_MARKERS_RATE == 0:
            self.ant.drop_marker(MarkerType.HOME)

        # check if ant is near food
        nearest_food_source = self.ant.get_nearest_food_source()

        if nearest_food_source is not None:
            self.food_target = nearest_food_source
            return AntStateMachine.GO_FOOD_STATE

        # if it sees a food marker
        if self.ant.is_near_marker(MarkerType.FOOD):
            self._follow_marker(MarkerType.FOOD)
            return AntStateMachine.EXPLORING_STATE

        self.ant.wander()

        return AntStateMachine.EXPLORING_STATE

    def _handle_going_to_food(self):
        if self.food_target is None or self.food_target.amount == 0:
            # this occurs when an ant selects a food source and then the food source is removed
            return AntStateMachine.EXPLORING_STATE

        # drop marker
        if self.ant.model.schedule.steps % 5 == 0:
            self.ant.drop_marker(MarkerType.HOME)

        # move ant to food
        self.ant.go_to(self.food_target.pos)

        if self.ant.is_at(self.food_target.pos):
            self.ant.take_food()
            self.food_target.reduce()
            return AntStateMachine.GO_HOME_STATE

        return AntStateMachine.GO_FOOD_STATE

    def _handle_go_home(self) -> str:
        # drop marker
        if self.ant.model.schedule.steps % 5 == 0:
            self.ant.drop_marker(MarkerType.FOOD)

        # if at home, end
        if self.ant.get_home():
            home = self.ant.get_home()
            if self.ant.is_at(home.pos):
                if self.ant.has_food:
                    self.ant.drop_food()
                return AntStateMachine.EXPLORING_STATE

            self.ant.go_to(self.ant.get_home().pos)
            return AntStateMachine.GO_HOME_STATE

        self._follow_marker(MarkerType.HOME)

        return AntStateMachine.GO_HOME_STATE

    def _handle_end(self):
        # TODO
        print('fds')
        pass

    def _follow_marker(self, marker_type: MarkerType) -> None:
        # do this only once every FOLLOW_MARKER_RATE steps
        if self.ant.model.schedule.steps % self.ant.FOLLOW_MARKERS_RATE == 0:
            if self.ant.is_near_marker(marker_type):
                marker = self.ant.get_strongest_marker(marker_type)
                self.ant.go_to(marker.pos)
            else:
                self.ant.wander()
        else:
            self.ant.move()
