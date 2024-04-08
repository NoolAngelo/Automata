#automata finite state machine
class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}

    def add_transition(self, input_symbol, next_state):
        self.transitions[input_symbol] = next_state

    def get_next_state(self, input_symbol):
        return self.transitions.get(input_symbol)


class FiniteStateMachine:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_state(self, state):
        self.states[state.name] = state

    def set_initial_state(self, state_name):
        self.current_state = self.states[state_name]

    def transition(self, input_symbol):
        if self.current_state:
            next_state = self.current_state.get_next_state(input_symbol)
            if next_state:
                self.current_state = next_state
                print(f"Transitioned to state: {self.current_state.name}")
            else:
                print("Invalid input for current state.")
        else:
            print("No initial state set.")

# Example usage:
# Define states
s0 = State("S0")
s1 = State("S1")
s2 = State("S2")

# Add transitions
s0.add_transition('a', s1)
s0.add_transition('b', s2)
s1.add_transition('a', s0)
s1.add_transition('b', s2)
s2.add_transition('a', s2)
s2.add_transition('b', s1)

# Create finite state machine
fsm = FiniteStateMachine()
fsm.add_state(s0)
fsm.add_state(s1)
fsm.add_state(s2)

# Set initial state
fsm.set_initial_state("S0")

# Perform transitions
inputs = ['a', 'b', 'a', 'b']
for inp in inputs:
    fsm.transition(inp)
