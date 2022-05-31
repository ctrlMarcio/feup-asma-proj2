from ants.util.state_machine import StateMachine


class AntStateMachine:

    EXPLORING_STATE = "EXPLORING"
    END_STATE = "END"

    def __init__(self, ant):
        self.state_machine = StateMachine()
        self.ant = ant

        self._config_state_machine()

    def step(self):
        return self.state_machine.step()

    def _config_state_machine(self):
        self.state_machine.add_state(
            AntStateMachine.EXPLORING_STATE, self._exploring_handle)
        self.state_machine.add_state(
            AntStateMachine.END_STATE, self._end_handle, end_state=1)

        self.state_machine.set_start(AntStateMachine.EXPLORING_STATE)

    def _exploring_handle(self):
        # move ant to right
        self.ant.wander()
        return AntStateMachine.EXPLORING_STATE

    def _end_handle(self):
        # TODO
        pass
