#!/usr/bin/env python3
"""
Simple demonstration script for the Enhanced Finite State Machine.
This script runs automatically without loops or user interaction.
"""

from automata_FSM import State, FiniteStateMachine


def create_simple_demo():
    """Create a simple FSM demo that accepts strings containing 'abc'."""
    print("🎯 Creating FSM that accepts strings containing 'abc' substring")
    
    # States to track progress towards 'abc'
    start = State("START")
    a_found = State("A_FOUND") 
    ab_found = State("AB_FOUND")
    abc_found = State("ABC_FOUND", is_accepting=True)
    
    # Transitions for finding 'abc'
    start.add_transition('a', a_found)
    start.add_transition('b', start)
    start.add_transition('c', start)
    
    a_found.add_transition('a', a_found)  # Stay in a_found if another 'a'
    a_found.add_transition('b', ab_found)
    a_found.add_transition('c', start)
    
    ab_found.add_transition('a', a_found)
    ab_found.add_transition('b', start)  
    ab_found.add_transition('c', abc_found)
    
    abc_found.add_transition('a', a_found)  # Continue looking for more 'abc'
    abc_found.add_transition('b', abc_found)
    abc_found.add_transition('c', abc_found)
    
    # Build FSM
    fsm = FiniteStateMachine()
    for state in [start, a_found, ab_found, abc_found]:
        fsm.add_state(state)
    fsm.set_initial_state("START")
    
    return fsm


def main():
    """Run the simple demonstration."""
    print("🤖 Enhanced Finite State Machine - Simple Demo")
    print("=" * 55)
    print("This demo runs automatically without user interaction.\n")
    
    # Create and test FSM
    fsm = create_simple_demo()
    fsm.print_fsm_info()
    
    # Test various strings
    test_strings = [
        "abc",          # Should accept (contains 'abc')
        "xabcy",        # Should accept (contains 'abc')  
        "aabbcc",       # Should reject (no 'abc' substring)
        "abcabc",       # Should accept (contains 'abc')
        "abab",         # Should reject (incomplete 'abc')
        "cabcab",       # Should accept (contains 'abc')
        "",             # Should reject (empty string)
        "abcdef"        # Should accept (starts with 'abc')
    ]
    
    print(f"\n📝 Testing {len(test_strings)} strings:")
    print("-" * 50)
    
    for test_str in test_strings:
        result = fsm.process_string(test_str, verbose=False)
        status = "✅ ACCEPTED" if result else "❌ REJECTED"
        print(f"  '{test_str:>8}' → {status}")
    
    print("\n" + "=" * 55)
    print("✅ Simple demo completed!")
    print("💡 For more examples, run: python3 examples.py --demo")
    print("🎮 For interactive mode, run: python3 examples.py")
    print("=" * 55)


if __name__ == "__main__":
    main()
