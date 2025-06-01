#!/usr/bin/env python3
"""
Unit tests for the Enhanced Finite State Machine implementation.
"""

import unittest
import sys
from io import StringIO
from automata_FSM import State, FiniteStateMachine, create_binary_string_fsm, create_even_a_fsm


class TestState(unittest.TestCase):
    """Test cases for the State class."""
    
    def setUp(self):
        self.state = State("TestState")
        self.accepting_state = State("AcceptState", is_accepting=True)
    
    def test_state_creation(self):
        """Test state creation with different parameters."""
        self.assertEqual(self.state.name, "TestState")
        self.assertFalse(self.state.is_accepting)
        self.assertTrue(self.accepting_state.is_accepting)
        self.assertEqual(len(self.state.transitions), 0)
    
    def test_add_transition(self):
        """Test adding transitions to a state."""
        next_state = State("NextState")
        self.state.add_transition('a', next_state)
        
        self.assertIn('a', self.state.transitions)
        self.assertEqual(self.state.transitions['a'], next_state)
    
    def test_get_next_state(self):
        """Test getting next state for input symbols."""
        next_state = State("NextState")
        self.state.add_transition('a', next_state)
        
        self.assertEqual(self.state.get_next_state('a'), next_state)
        self.assertIsNone(self.state.get_next_state('b'))
    
    def test_get_valid_inputs(self):
        """Test getting valid input symbols."""
        state1 = State("State1")
        state2 = State("State2")
        
        self.state.add_transition('a', state1)
        self.state.add_transition('b', state2)
        
        valid_inputs = self.state.get_valid_inputs()
        self.assertIn('a', valid_inputs)
        self.assertIn('b', valid_inputs)
        self.assertEqual(len(valid_inputs), 2)


class TestFiniteStateMachine(unittest.TestCase):
    """Test cases for the FiniteStateMachine class."""
    
    def setUp(self):
        self.fsm = FiniteStateMachine()
        self.state1 = State("S1")
        self.state2 = State("S2", is_accepting=True)
        
    def test_add_state(self):
        """Test adding states to FSM."""
        self.fsm.add_state(self.state1)
        self.fsm.add_state(self.state2)
        
        self.assertIn("S1", self.fsm.states)
        self.assertIn("S2", self.fsm.states)
        self.assertIn("S2", self.fsm.accepting_states)
        self.assertNotIn("S1", self.fsm.accepting_states)
    
    def test_set_initial_state(self):
        """Test setting initial state."""
        self.fsm.add_state(self.state1)
        self.fsm.set_initial_state("S1")
        
        self.assertEqual(self.fsm.initial_state, "S1")
        self.assertEqual(self.fsm.current_state, self.state1)
    
    def test_set_invalid_initial_state(self):
        """Test setting non-existent initial state raises error."""
        with self.assertRaises(ValueError):
            self.fsm.set_initial_state("NonExistent")
    
    def test_reset(self):
        """Test resetting FSM to initial state."""
        self.fsm.add_state(self.state1)
        self.fsm.add_state(self.state2)
        self.fsm.set_initial_state("S1")
        
        # Move to different state
        self.fsm.current_state = self.state2
        
        # Reset should bring back to initial state
        self.fsm.reset()
        self.assertEqual(self.fsm.current_state, self.state1)
        self.assertEqual(len(self.fsm.transition_history), 0)
    
    def test_transition(self):
        """Test state transitions."""
        self.state1.add_transition('a', self.state2)
        self.fsm.add_state(self.state1)
        self.fsm.add_state(self.state2)
        self.fsm.set_initial_state("S1")
        
        # Valid transition
        result = self.fsm.transition('a', verbose=False)
        self.assertTrue(result)
        self.assertEqual(self.fsm.current_state, self.state2)
        
        # Invalid transition
        result = self.fsm.transition('b', verbose=False)
        self.assertFalse(result)
        self.assertEqual(self.fsm.current_state, self.state2)  # Should stay in same state
    
    def test_process_string(self):
        """Test processing complete strings."""
        # Create simple FSM: S1 --a--> S2(accepting)
        self.state1.add_transition('a', self.state2)
        self.state2.add_transition('b', self.state1)
        
        self.fsm.add_state(self.state1)
        self.fsm.add_state(self.state2)
        self.fsm.set_initial_state("S1")
        
        # Test accepted string
        result = self.fsm.process_string("a", verbose=False)
        self.assertTrue(result)
        
        # Test rejected string (ends in non-accepting state)
        result = self.fsm.process_string("ab", verbose=False)
        self.assertFalse(result)
        
        # Test invalid character
        result = self.fsm.process_string("x", verbose=False)
        self.assertFalse(result)
    
    def test_validation(self):
        """Test FSM validation."""
        # Empty FSM should fail validation
        self.assertFalse(self.fsm.validate_fsm())
        
        # FSM with states but no initial state should fail
        self.fsm.add_state(self.state1)
        self.assertFalse(self.fsm.validate_fsm())
        
        # Valid FSM should pass
        self.fsm.set_initial_state("S1")
        self.assertTrue(self.fsm.validate_fsm())


class TestFSMExamples(unittest.TestCase):
    """Test cases for the example FSMs."""
    
    def test_binary_string_fsm(self):
        """Test the binary string FSM that accepts strings ending with '01'."""
        fsm = create_binary_string_fsm()
        
        # Should accept strings ending with '01'
        self.assertTrue(fsm.process_string("01", verbose=False))
        self.assertTrue(fsm.process_string("101", verbose=False))
        self.assertTrue(fsm.process_string("001", verbose=False))
        self.assertTrue(fsm.process_string("1101", verbose=False))
        
        # Should reject other strings
        self.assertFalse(fsm.process_string("10", verbose=False))
        self.assertFalse(fsm.process_string("11", verbose=False))
        self.assertFalse(fsm.process_string("000", verbose=False))
        self.assertFalse(fsm.process_string("", verbose=False))
    
    def test_even_a_fsm(self):
        """Test the FSM that accepts strings with even number of 'a's."""
        fsm = create_even_a_fsm()
        
        # Should accept strings with even number of 'a's
        self.assertTrue(fsm.process_string("", verbose=False))  # 0 a's (even)
        self.assertTrue(fsm.process_string("aa", verbose=False))  # 2 a's
        self.assertTrue(fsm.process_string("abab", verbose=False))  # 2 a's
        self.assertTrue(fsm.process_string("bbbb", verbose=False))  # 0 a's
        self.assertTrue(fsm.process_string("aabb", verbose=False))  # 2 a's
        
        # Should reject strings with odd number of 'a's
        self.assertFalse(fsm.process_string("a", verbose=False))  # 1 a
        self.assertFalse(fsm.process_string("bab", verbose=False))  # 1 a (this was wrong in original test)
        self.assertFalse(fsm.process_string("aaa", verbose=False))  # 3 a's
        self.assertFalse(fsm.process_string("aaabbb", verbose=False))  # 3 a's

if __name__ == "__main__":
    # Run the tests
    print("🧪 Running FSM Unit Tests...")
    print("=" * 50)
    
    # Capture test output
    test_suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    test_runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = test_runner.run(test_suite)
    
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        
    print(f"Tests run: {result.testsRun}")
    print("=" * 50)
