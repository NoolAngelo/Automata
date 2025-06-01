#!/usr/bin/env python3
"""
Interactive examples and experiments with the Enhanced Finite State Machine.
Run this script to try out different FSM configurations and test strings.
"""

from automata_FSM import State, FiniteStateMachine, create_binary_string_fsm, create_even_a_fsm


def create_palindrome_fsm():
    """
    Create an FSM that accepts palindromes of length 3 over alphabet {a, b}.
    Accepts: "aaa", "aba", "bab", "bbb"
    """
    # States for tracking the sequence
    start = State("START")
    a_first = State("A_FIRST") 
    b_first = State("B_FIRST")
    aa_second = State("AA_SECOND")
    ab_second = State("AB_SECOND")
    ba_second = State("BA_SECOND") 
    bb_second = State("BB_SECOND")
    aaa_accept = State("AAA", is_accepting=True)
    aba_accept = State("ABA", is_accepting=True)
    bab_accept = State("BAB", is_accepting=True)
    bbb_accept = State("BBB", is_accepting=True)

    # First character transitions
    start.add_transition('a', a_first)
    start.add_transition('b', b_first)
    
    # Second character transitions
    a_first.add_transition('a', aa_second)
    a_first.add_transition('b', ab_second)
    b_first.add_transition('a', ba_second)
    b_first.add_transition('b', bb_second)
    
    # Third character transitions (must match first for palindrome)
    aa_second.add_transition('a', aaa_accept)  # aaa
    ab_second.add_transition('a', aba_accept)  # aba  
    ba_second.add_transition('b', bab_accept)  # bab
    bb_second.add_transition('b', bbb_accept)  # bbb

    fsm = FiniteStateMachine()
    for state in [start, a_first, b_first, aa_second, ab_second, ba_second, bb_second,
                  aaa_accept, aba_accept, bab_accept, bbb_accept]:
        fsm.add_state(state)
    
    fsm.set_initial_state("START")
    return fsm


def create_divisible_by_3_fsm():
    """
    Create an FSM that accepts binary numbers divisible by 3.
    States represent remainder when divided by 3.
    """
    r0 = State("R0", is_accepting=True)  # remainder 0 (divisible by 3)
    r1 = State("R1")  # remainder 1
    r2 = State("R2")  # remainder 2

    # Binary digit transitions (each bit doubles the number)
    # From remainder 0: 0 -> stay 0, 1 -> go to 1
    r0.add_transition('0', r0)  # 0 * 2 + 0 = 0 mod 3
    r0.add_transition('1', r1)  # 0 * 2 + 1 = 1 mod 3
    
    # From remainder 1: 0 -> go to 2, 1 -> stay 0  
    r1.add_transition('0', r2)  # 1 * 2 + 0 = 2 mod 3
    r1.add_transition('1', r0)  # 1 * 2 + 1 = 3 = 0 mod 3
    
    # From remainder 2: 0 -> go to 1, 1 -> go to 2
    r2.add_transition('0', r1)  # 2 * 2 + 0 = 4 = 1 mod 3
    r2.add_transition('1', r2)  # 2 * 2 + 1 = 5 = 2 mod 3

    fsm = FiniteStateMachine()
    fsm.add_state(r0)
    fsm.add_state(r1) 
    fsm.add_state(r2)
    fsm.set_initial_state("R0")
    
    return fsm


def interactive_string_tester():
    """Interactive string testing for different FSMs."""
    print("\n" + "=" * 60)
    print("🎮 INTERACTIVE FSM STRING TESTER")
    print("=" * 60)
    
    fsms = {
        "1": ("Binary strings ending with '01'", create_binary_string_fsm()),
        "2": ("Even number of 'a's", create_even_a_fsm()),
        "3": ("3-character palindromes {a,b}", create_palindrome_fsm()),
        "4": ("Binary numbers divisible by 3", create_divisible_by_3_fsm())
    }
    
    print("Available FSMs:")
    for key, (description, _) in fsms.items():
        print(f"  {key}. {description}")
    
    while True:
        try:
            choice = input("\nSelect FSM (1-4) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                print("👋 Goodbye!")
                break
                
            if choice not in fsms:
                print("❌ Invalid choice. Please select 1-4 or 'q'.")
                continue
                
            description, fsm = fsms[choice]
            print(f"\n🤖 Selected: {description}")
            fsm.print_fsm_info()
            
            while True:
                test_string = input("\nEnter string to test (or 'back' to choose different FSM): ").strip()
                
                if test_string.lower() == 'back':
                    break
                    
                print(f"\n📝 Testing: '{test_string}'")
                result = fsm.process_string(test_string, verbose=True)
                print(f"🎯 Result: {'ACCEPTED' if result else 'REJECTED'}")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def demonstrate_advanced_features():
    """Demonstrate advanced FSM features."""
    print("\n" + "=" * 60)
    print("🔬 ADVANCED FSM FEATURES DEMONSTRATION")
    print("=" * 60)
    
    # Create a simple FSM for demonstration
    print("\n🔸 Creating a simple FSM: accepts strings ending with 'ab'")
    s0 = State("S0")
    s1 = State("S1")
    s2 = State("S2", is_accepting=True)
    
    s0.add_transition('a', s1)
    s0.add_transition('b', s0)
    s1.add_transition('a', s1)
    s1.add_transition('b', s2)
    s2.add_transition('a', s1)
    s2.add_transition('b', s0)
    
    fsm = FiniteStateMachine()
    fsm.add_state(s0)
    fsm.add_state(s1)
    fsm.add_state(s2)
    fsm.set_initial_state("S0")
    
    fsm.print_fsm_info()
    
    # Demonstrate transition history
    print("\n🔸 Testing string 'aabab' and showing transition history:")
    result = fsm.process_string("aabab", verbose=True)
    
    print(f"\n📊 Transition History:")
    history = fsm.get_transition_history()
    for i, (from_state, symbol, to_state) in enumerate(history, 1):
        print(f"  {i}. {from_state} --{symbol}--> {to_state}")
    
    # Demonstrate step-by-step transitions
    print(f"\n🔸 Manual step-by-step transitions:")
    fsm.reset()
    
    test_sequence = ['b', 'a', 'b']
    for symbol in test_sequence:
        old_state = fsm.get_current_state()
        success = fsm.transition(symbol, verbose=False)
        new_state = fsm.get_current_state()
        accepting = fsm.is_in_accepting_state()
        
        print(f"  Input '{symbol}': {old_state} → {new_state} (Success: {success}, Accepting: {accepting})")
    
    # Demonstrate validation
    print(f"\n🔸 FSM Validation:")
    is_valid = fsm.validate_fsm()
    print(f"  Validation result: {'✅ VALID' if is_valid else '❌ INVALID'}")


def number_theory_examples():
    """Examples of FSMs solving number theory problems."""
    print("\n" + "=" * 60)
    print("🔢 NUMBER THEORY FSM EXAMPLES")
    print("=" * 60)
    
    print("\n🔸 Binary numbers divisible by 3:")
    div3_fsm = create_divisible_by_3_fsm()
    div3_fsm.print_fsm_info()
    
    # Test some binary numbers
    test_numbers = [
        ("0", 0), ("11", 3), ("110", 6), ("1001", 9), 
        ("1100", 12), ("1", 1), ("10", 2), ("100", 4), ("101", 5)
    ]
    
    print("\n📝 Testing binary numbers:")
    for binary, decimal in test_numbers:
        result = div3_fsm.process_string(binary, verbose=False)
        divisible = "✅" if result else "❌"
        print(f"  {binary:>4} (decimal {decimal:>2}) → {divisible} {'divisible' if result else 'not divisible'} by 3")


def demo_mode():
    """Run all demonstrations automatically without user interaction."""
    print("🤖 Enhanced Finite State Machine - Demo Mode")
    print("=" * 70)
    print("🎬 Running all demonstrations automatically...\n")
    
    # Run advanced features demo
    demonstrate_advanced_features()
    
    # Run number theory examples  
    number_theory_examples()
    
    # Run main FSM examples
    print("\n📖 Main FSM Examples:")
    from automata_FSM import demonstrate_fsm_examples
    demonstrate_fsm_examples()
    
    print("\n" + "=" * 70)
    print("✅ Demo completed! Use 'python3 examples.py --interactive' for interactive mode.")
    print("=" * 70)


def main():
    """Main function to run examples."""
    import sys
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo" or sys.argv[1] == "-d":
            demo_mode()
            return
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("🤖 Enhanced Finite State Machine - Examples")
            print("=" * 50)
            print("Usage:")
            print("  python3 examples.py              # Interactive mode (default)")
            print("  python3 examples.py --demo       # Auto-demo mode")
            print("  python3 examples.py --interactive # Interactive mode")
            print("  python3 examples.py --help       # Show this help")
            return
    
    # Default to interactive mode
    print("🤖 Enhanced Finite State Machine - Interactive Examples")
    print("=" * 70)
    print("💡 Tip: Use 'python3 examples.py --demo' for automatic demonstration")
    
    try:
        while True:
            print("\n📋 Available demonstrations:")
            print("  1. 🎮 Interactive String Tester")
            print("  2. 🔬 Advanced Features Demo") 
            print("  3. 🔢 Number Theory Examples")
            print("  4. 📖 View All Example FSMs")
            print("  5. ❌ Exit")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == "1":
                interactive_string_tester()
            elif choice == "2":
                demonstrate_advanced_features()
            elif choice == "3":
                number_theory_examples()
            elif choice == "4":
                print("\n📖 Running all example demonstrations:")
                from automata_FSM import demonstrate_fsm_examples
                demonstrate_fsm_examples()
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-5.")
                
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except EOFError:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
