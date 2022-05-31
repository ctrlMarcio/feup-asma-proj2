class StateMachine:

    def __init__(self):
        self.handlers = {}
        self.start_state = None
        self.current_state = None
        self.end_states = []

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.end_states.append(name)

    def set_start(self, name):
        self.start_state = name.upper()
        self.current_state = self.start_state

    def step(self):
        try:
            handler = self.handlers[self.current_state]
        except:
            raise RuntimeError("unhandled state: " + self.current_state +
                               ". should call .set_start() before .step(), and all handlers should return a valid state")
        if not self.end_states:
            raise RuntimeError("at least one state must be an end_state")

        self.current_state = handler().upper()
        if self.current_state in self.end_states:
            return True
        else:
            return False
