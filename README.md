# Enhanced Finite State Machine (FSM) Implementation

A comprehensive and feature-rich finite state machine implementation in Python with support for accepting states, string processing, validation, and detailed logging.

## 🚀 Features

- **Enhanced State Management**: States with accepting/non-accepting designation
- **String Processing**: Complete string validation and acceptance testing
- **Transition History**: Track and review state transition sequences
- **Comprehensive Validation**: FSM configuration validation and error checking
- **Rich Logging**: Detailed logging with configurable levels
- **Type Hints**: Full type annotations for better code clarity
- **Unit Testing**: Comprehensive test suite with multiple test cases
- **Interactive Examples**: Pre-built FSM examples with demonstrations

## 📁 Project Structure

```
/Automata/
├── automata_FSM.py     # Enhanced FSM implementation
├── test_fsm.py         # Comprehensive unit tests
├── examples.py         # Interactive examples and experiments
└── README.md          # This documentation
```

## 🔧 Installation & Usage

### Prerequisites

- Python 3.6 or higher
- No external dependencies required

### Running the Examples

```bash
# Run the main examples and demonstrations
python3 automata_FSM.py

# Run interactive examples and experiments
python3 examples.py              # Interactive mode (default)
python3 examples.py --demo       # Auto-demo mode (no loops)
python3 examples.py --help       # Show usage help

# Run the unit tests
python3 test_fsm.py
```

### Quick Demo (Non-Interactive)

```bash
# Run all demonstrations automatically without user input
python3 examples.py --demo
```

This will show:

- ✨ Advanced FSM features demonstration
- 🔢 Number theory examples (binary divisibility)
- 📖 All built-in FSM examples
- No infinite loops or user input required!

## 📖 Core Classes

### `State`

Represents a single state in the finite state machine.

```python
class State:
    def __init__(self, name: str, is_accepting: bool = False)
    def add_transition(self, input_symbol: str, next_state: 'State') -> None
    def get_next_state(self, input_symbol: str) -> Optional['State']
    def get_valid_inputs(self) -> List[str]
```

### `FiniteStateMachine`

The main FSM class with enhanced functionality.

```python
class FiniteStateMachine:
    def __init__(self)
    def add_state(self, state: State) -> None
    def set_initial_state(self, state_name: str) -> None
    def reset(self) -> None
    def transition(self, input_symbol: str, verbose: bool = True) -> bool
    def process_string(self, input_string: str, verbose: bool = True) -> bool
    def validate_fsm(self) -> bool
```

## 💡 Example Usage

### Basic FSM Creation

```python
from automata_FSM import State, FiniteStateMachine

# Create states
start = State("START")
accept = State("ACCEPT", is_accepting=True)

# Add transitions
start.add_transition('a', accept)
accept.add_transition('b', start)

# Create and configure FSM
fsm = FiniteStateMachine()
fsm.add_state(start)
fsm.add_state(accept)
fsm.set_initial_state("START")

# Process strings
result = fsm.process_string("ab")  # Returns False (ends in START, non-accepting)
result = fsm.process_string("a")   # Returns True (ends in ACCEPT)
```

### String Processing with Detailed Output

```python
# Enable verbose output to see step-by-step transitions
fsm.process_string("aba", verbose=True)

# Output:
# 🔄 Processing string: 'aba'
# 'a': START → ACCEPT
# 'b': ACCEPT → START
# 'a': START → ACCEPT
# ✅ ACCEPTED - Final state: ACCEPT
```

## 🎮 Interactive Examples

The `examples.py` file provides an interactive interface to experiment with different FSMs:

### Available Interactive Features:

1. **String Tester** - Test strings against various pre-built FSMs
2. **Advanced Features Demo** - See transition history, validation, and step-by-step execution
3. **Number Theory Examples** - FSMs that solve mathematical problems
4. **Additional FSM Examples**:
   - 3-character palindrome detector
   - Binary numbers divisible by 3
   - More complex state machines

```bash
python3 examples.py
```

## 🎯 Pre-built Examples

### 1. Binary Strings Ending with '01'

FSM that accepts binary strings ending with the pattern '01'.

```python
fsm = create_binary_string_fsm()

fsm.process_string("101")   # ✅ ACCEPTED
fsm.process_string("001")   # ✅ ACCEPTED
fsm.process_string("110")   # ❌ REJECTED
```

**State Diagram:**

```
START --0--> ZERO --1--> ACCEPT
  |           |           |
  +----1------+     +--0--+
       |             |
       +------1------+
```

### 2. Even Number of 'a's

FSM that accepts strings containing an even number of 'a' characters.

```python
fsm = create_even_a_fsm()

fsm.process_string("aa")     # ✅ ACCEPTED (2 a's)
fsm.process_string("bab")    # ❌ REJECTED (1 a)
fsm.process_string("abab")   # ✅ ACCEPTED (2 a's)
```

**State Diagram:**

```
EVEN_A --a--> ODD_A
  |             |
  +------a------+
  |             |
  +--b---+ +--b-+
         | |
         v v
      (self-loops)
```

## 🧪 Testing

The project includes comprehensive unit tests covering:

- State creation and transitions
- FSM configuration and validation
- String processing and acceptance
- Error handling and edge cases
- Example FSM correctness

```bash
# Run all tests
python3 test_fsm.py

# Expected output:
# 🧪 Running FSM Unit Tests...
# ✅ All tests passed!
# Tests run: 15
```

## 🔍 Advanced Features

### Transition History

Track all state transitions for debugging and analysis:

```python
fsm.process_string("aba")
history = fsm.get_transition_history()
# Returns: [('START', 'a', 'ACCEPT'), ('ACCEPT', 'b', 'START'), ('START', 'a', 'ACCEPT')]
```

### FSM Validation

Validate FSM configuration before use:

```python
is_valid = fsm.validate_fsm()
if not is_valid:
    print("FSM configuration has errors!")
```

### Interactive Information Display

Get detailed FSM information:

```python
fsm.print_fsm_info()

# Output:
# 📋 FSM Information:
#    States: ['START', 'ZERO', 'ACCEPT']
#    Initial state: START
#    Accepting states: ['ACCEPT']
#    Current state: START
#
# 🔗 Transitions:
#    START --0--> ZERO
#    START --1--> START
#    ZERO --0--> ZERO
#    ZERO --1--> ACCEPT
#    ...
```

## 🎨 Key Improvements from Basic Implementation

1. **Accepting States**: Support for final/accepting states
2. **String Processing**: Complete string validation with accept/reject results
3. **Error Handling**: Comprehensive error handling and validation
4. **Type Safety**: Full type hints for better IDE support
5. **Logging**: Configurable logging for debugging
6. **Testing**: Extensive unit test coverage
7. **Documentation**: Rich documentation with examples
8. **Visual Feedback**: Emoji-enhanced output for better UX

## 🤝 Contributing

Feel free to enhance this implementation with:

- Non-deterministic FSM support (NFA)
- Epsilon transitions
- FSM minimization algorithms
- Graphical visualization
- More example automata

## 📝 License

This project is open source and available under the MIT License.
