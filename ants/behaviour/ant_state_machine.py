from ants.util.state_machine import StateMachine


class AntStateMachine:

    EXPLORING_STATE = "EXPLORING"
    GO_HOME_STATE = "GO_HOME"
    END_STATE = "END"

    def __init__(self, ant):
        self.state_machine = StateMachine()
        self.ant = ant

        self._config_state_machine()

    def step(self) -> bool:
        return self.state_machine.step()

    def _config_state_machine(self) -> None:
        self.state_machine.add_state(
            AntStateMachine.EXPLORING_STATE, self._handle_exploring)
        self.state_machine.add_state(
            AntStateMachine.GO_HOME_STATE, self._handle_go_home)
        self.state_machine.add_state(
            AntStateMachine.END_STATE, self._handle_end, end_state=1)

        self.state_machine.set_start(AntStateMachine.EXPLORING_STATE)

    def _handle_exploring(self) -> str:
        if self.ant.model.schedule.steps % self.ant.LEAVE_MARKERS_RATE == 0:
            self.ant.leave_marker()

        self.ant.wander()

        # TEST temporary while no food
        if self.ant.is_near_marker():
            if self.ant.model.schedule.steps > 2000:
                return AntStateMachine.GO_HOME_STATE

        return AntStateMachine.EXPLORING_STATE

    def _handle_go_home(self) -> str:
        # if at home, end
        if self.ant.get_home():
            home = self.ant.get_home()
            if self.ant.pos == home.pos:
                return AntStateMachine.END_STATE

            self.ant.move_in_direction(self.ant.get_home().pos)
            return AntStateMachine.GO_HOME_STATE

        if self.ant.is_near_marker():
            go_to_pos = self.ant.get_strongest_marker().pos
            self.ant.move_in_direction(go_to_pos)
        else:
            self.ant.wander()

        return AntStateMachine.GO_HOME_STATE

    def _handle_end(self):
        # TODO
        print('fds')
        pass
