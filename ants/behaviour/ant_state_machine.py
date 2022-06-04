from ants.agents.marker_agent import MarkerType
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
            if self.ant.model.schedule.steps > 1000:
                return AntStateMachine.GO_HOME_STATE

        return AntStateMachine.EXPLORING_STATE

    def _handle_go_home(self) -> str:
        # if at home, end
        if self.ant.get_home():
            home = self.ant.get_home()
            if self.ant.pos == home.pos:
                return AntStateMachine.END_STATE

            self.ant.move_to_position(self.ant.get_home().pos)
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
                go_to_pos = self.ant.get_strongest_marker(marker_type).pos
                self.ant.move_to_position(go_to_pos)
            else:
                self.ant.wander()
        else:
            self.ant.move()
