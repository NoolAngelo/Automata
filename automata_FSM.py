# Enhanced Finite State Machine Implementation
from typing import Dict, Set, Optional, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class State:
    """Represents a state in the finite state machine."""
    
    def __init__(self, name: str, is_accepting: bool = False):
        self.name = name
        self.transitions: Dict[str, 'State'] = {}
        self.is_accepting = is_accepting

    def add_transition(self, input_symbol: str, next_state: 'State') -> None:
        """Add a transition from this state to another state."""
        self.transitions[input_symbol] = next_state
        logger.debug(f"Added transition: {self.name} --{input_symbol}--> {next_state.name}")

    def get_next_state(self, input_symbol: str) -> Optional['State']:
        """Get the next state for a given input symbol."""
        return self.transitions.get(input_symbol)

    def get_valid_inputs(self) -> List[str]:
        """Get all valid input symbols from this state."""
        return list(self.transitions.keys())

    def __str__(self) -> str:
        return f"State({self.name}, accepting={self.is_accepting})"

    def __repr__(self) -> str:
        return self.__str__()


class FiniteStateMachine:
    """Enhanced Finite State Machine with accepting states and string processing."""
    
    def __init__(self):
        self.states: Dict[str, State] = {}
        self.current_state: Optional[State] = None
        self.initial_state: Optional[str] = None
        self.accepting_states: Set[str] = set()
        self.transition_history: List[tuple] = []

    def add_state(self, state: State) -> None:
        """Add a state to the finite state machine."""
        self.states[state.name] = state
        if state.is_accepting:
            self.accepting_states.add(state.name)
        logger.info(f"Added state: {state}")

    def set_initial_state(self, state_name: str) -> None:
        """Set the initial state of the finite state machine."""
        if state_name not in self.states:
            raise ValueError(f"State '{state_name}' does not exist")
        
        self.initial_state = state_name
        self.current_state = self.states[state_name]
        logger.info(f"Set initial state to: {state_name}")

    def reset(self) -> None:
        """Reset the FSM to its initial state."""
        if self.initial_state:
            self.current_state = self.states[self.initial_state]
            self.transition_history.clear()
            logger.debug("FSM reset to initial state")
        else:
            raise RuntimeError("No initial state set")

    def transition(self, input_symbol: str, verbose: bool = True) -> bool:
        """Perform a transition based on the input symbol."""
        if not self.current_state:
            raise RuntimeError("No current state set")

        old_state = self.current_state.name
        next_state = self.current_state.get_next_state(input_symbol)
        
        if next_state:
            self.current_state = next_state
            self.transition_history.append((old_state, input_symbol, next_state.name))
            
            if verbose:
                print(f"'{input_symbol}': {old_state} → {next_state.name}")
            
            logger.debug(f"Transition successful: {old_state} --{input_symbol}--> {next_state.name}")
            return True
        else:
            if verbose:
                valid_inputs = self.states[old_state].get_valid_inputs()
                print(f"❌ Invalid input '{input_symbol}' for state {old_state}")
                print(f"   Valid inputs: {valid_inputs}")
            
            logger.warning(f"Invalid transition from {old_state} with input '{input_symbol}'")
            return False

    def process_string(self, input_string: str, verbose: bool = True) -> bool:
        """Process a complete input string and return if it's accepted."""
        if verbose:
            print(f"\n🔄 Processing string: '{input_string}'")
        
        self.reset()
        
        for i, symbol in enumerate(input_string):
            if not self.transition(symbol, verbose):
                if verbose:
                    print(f"❌ String rejected at position {i}")
                return False
        
        is_accepted = self.current_state.name in self.accepting_states
        
        if verbose:
            status = "✅ ACCEPTED" if is_accepted else "❌ REJECTED"
            print(f"{status} - Final state: {self.current_state.name}")
        
        return is_accepted

    def get_current_state(self) -> Optional[str]:
        """Get the name of the current state."""
        return self.current_state.name if self.current_state else None

    def is_in_accepting_state(self) -> bool:
        """Check if the current state is an accepting state."""
        return self.current_state and self.current_state.name in self.accepting_states

    def get_transition_history(self) -> List[tuple]:
        """Get the history of transitions."""
        return self.transition_history.copy()

    def print_fsm_info(self) -> None:
        """Print information about the FSM."""
        print("\n📋 FSM Information:")
        print(f"   States: {list(self.states.keys())}")
        print(f"   Initial state: {self.initial_state}")
        print(f"   Accepting states: {list(self.accepting_states)}")
        print(f"   Current state: {self.get_current_state()}")
        
        print("\n🔗 Transitions:")
        for state_name, state in self.states.items():
            for input_sym, next_state in state.transitions.items():
                print(f"   {state_name} --{input_sym}--> {next_state.name}")

    def validate_fsm(self) -> bool:
        """Validate the FSM configuration."""
        if not self.states:
            logger.error("FSM has no states")
            return False
        
        if not self.initial_state:
            logger.error("FSM has no initial state")
            return False
        
        # Check if all transitions point to existing states
        for state_name, state in self.states.items():
            for input_sym, next_state in state.transitions.items():
                if next_state.name not in self.states:
                    logger.error(f"State {state_name} has transition to non-existent state {next_state.name}")
                    return False
        
        logger.info("FSM validation passed")
        return True



def create_binary_string_fsm() -> FiniteStateMachine:
    """
    Create an FSM that accepts binary strings ending with '01'.
    States: START, ZERO, ACCEPT
    """
    # Define states
    start = State("START")
    zero = State("ZERO") 
    accept = State("ACCEPT", is_accepting=True)

    # Add transitions
    start.add_transition('0', zero)
    start.add_transition('1', start)
    
    zero.add_transition('0', zero)
    zero.add_transition('1', accept)
    
    accept.add_transition('0', zero)
    accept.add_transition('1', start)

    # Create and configure FSM
    fsm = FiniteStateMachine()
    fsm.add_state(start)
    fsm.add_state(zero)
    fsm.add_state(accept)
    fsm.set_initial_state("START")
    
    return fsm


def create_even_a_fsm() -> FiniteStateMachine:
    """
    Create an FSM that accepts strings with an even number of 'a's.
    States: EVEN_A (accepting), ODD_A
    """
    even_a = State("EVEN_A", is_accepting=True)
    odd_a = State("ODD_A")

    # Transitions for 'a'
    even_a.add_transition('a', odd_a)
    odd_a.add_transition('a', even_a)
    
    # Transitions for 'b' (stay in same state)
    even_a.add_transition('b', even_a)
    odd_a.add_transition('b', odd_a)

    fsm = FiniteStateMachine()
    fsm.add_state(even_a)
    fsm.add_state(odd_a)
    fsm.set_initial_state("EVEN_A")
    
    return fsm


def demonstrate_fsm_examples():
    """Demonstrate various FSM examples."""
    print("=" * 60)
    print("🤖 ENHANCED FINITE STATE MACHINE DEMONSTRATIONS")
    print("=" * 60)
    
    # Example 1: Binary strings ending with '01'
    print("\n🔸 Example 1: Binary strings ending with '01'")
    print("   Accepts: strings that end with '01'")
    
    fsm1 = create_binary_string_fsm()
    fsm1.print_fsm_info()
    
    test_strings = ["01", "101", "001", "1101", "10", "11", "000"]
    for test_str in test_strings:
        fsm1.process_string(test_str)
    
    # Example 2: Even number of 'a's
    print("\n" + "=" * 60)
    print("🔸 Example 2: Strings with even number of 'a's")
    print("   Accepts: strings containing an even count of 'a's")
    
    fsm2 = create_even_a_fsm()
    fsm2.print_fsm_info()
    
    test_strings = ["", "aa", "aaa", "bab", "abab", "bbbb", "aaabbb"]
    for test_str in test_strings:
        fsm2.process_string(test_str)
    
    # Example 3: Interactive mode demonstration
    print("\n" + "=" * 60)
    print("🔸 Example 3: Step-by-step transition demonstration")
    
    fsm3 = create_binary_string_fsm()
    fsm3.reset()
    
    print(f"Current state: {fsm3.get_current_state()}")
    print("Manual transitions:")
    
    transitions = [('1', 'Should stay in START'), 
                  ('0', 'Should go to ZERO'),
                  ('1', 'Should go to ACCEPT'), 
                  ('0', 'Should go to ZERO')]
    
    for symbol, description in transitions:
        print(f"\nInput: '{symbol}' ({description})")
        success = fsm3.transition(symbol)
        print(f"Success: {success}, Current state: {fsm3.get_current_state()}")
        print(f"In accepting state: {fsm3.is_in_accepting_state()}")


if __name__ == "__main__":
    demonstrate_fsm_examples()
    
    print("\n" + "=" * 60)
    print("🎯 Try creating your own FSM!")
    print("=" * 60)
    print("""
Example usage:
    
# Create states
state1 = State("Q0", is_accepting=True)
state2 = State("Q1")

# Add transitions
state1.add_transition('x', state2)
state2.add_transition('y', state1)

# Create FSM
my_fsm = FiniteStateMachine()
my_fsm.add_state(state1)
my_fsm.add_state(state2)
my_fsm.set_initial_state("Q0")

# Process strings
result = my_fsm.process_string("xy")  # Should return True
    """)
