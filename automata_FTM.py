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
    

"""State class: This represents a state in the finite state machine. Each state has a name and a dictionary transitions that maps input symbols to the next state.

add_transition: This method adds a transition to the state. It takes an input symbol and the next state as arguments.

get_next_state: This method returns the next state based on the input symbol provided.

FiniteStateMachine class: This represents the finite state machine itself. It maintains a collection of states and keeps track of the current state.

add_state: This method adds a state to the finite state machine.

set_initial_state: This method sets the initial state of the finite state machine.

transition: This method performs a transition based on the input symbol provided. It checks if the current state exists, finds the next state based on the input symbol, and updates the current state accordingly.

Example usage: This section demonstrates how to define states, add transitions between them, create a finite state machine, set the initial state, and perform transitions based on a sequence of input symbols.

In the provided example, three states S0, S1, and S2 are defined, with transitions between them based on input symbols 'a' and 'b'. The initial state is set to S0, and a sequence of inputs ['a', 'b', 'a', 'b'] is used to perform transitions. The output of the transitions is printed, indicating the current state after each transition.
        """