"""
Tests for BJJ Drill-Through Narrative App

Test core functionality of the domain models, graph engine, and narrative engine.
"""

import unittest
from bjj_domain import (
    Position, Transition, DrillPrescription, DecisionQuality,
    BJJGraph, create_sample_graph
)
from narrative_engine import NarrativeEngine, NarrativeSession


class TestDomainModels(unittest.TestCase):
    """Test domain model classes"""
    
    def test_position_creation(self):
        """Test creating a Position"""
        pos = Position(
            id="test_pos",
            name="Test Position",
            description="A test position",
            advantages=["Adv1", "Adv2"],
            common_mistakes=["Mistake1"]
        )
        self.assertEqual(pos.id, "test_pos")
        self.assertEqual(pos.name, "Test Position")
        self.assertEqual(len(pos.advantages), 2)
    
    def test_drill_prescription_creation(self):
        """Test creating a DrillPrescription"""
        drill = DrillPrescription(
            name="Test Drill",
            description="A test drill",
            repetitions=10,
            focus_points=["Focus1", "Focus2"]
        )
        self.assertEqual(drill.name, "Test Drill")
        self.assertEqual(drill.repetitions, 10)
        self.assertEqual(len(drill.focus_points), 2)
    
    def test_transition_creation(self):
        """Test creating a Transition"""
        transition = Transition(
            from_position="pos1",
            to_position="pos2",
            action="Do something",
            opponent_reaction="React somehow",
            probability=0.7,
            decision_quality=DecisionQuality.GOOD
        )
        self.assertEqual(transition.from_position, "pos1")
        self.assertEqual(transition.probability, 0.7)
        self.assertEqual(transition.decision_quality, DecisionQuality.GOOD)


class TestBJJGraph(unittest.TestCase):
    """Test BJJ Graph engine"""
    
    def setUp(self):
        """Set up test graph"""
        self.graph = BJJGraph()
        
        self.pos1 = Position(
            id="pos1",
            name="Position 1",
            description="First position",
            advantages=["Adv1"],
            common_mistakes=["Mistake1"]
        )
        
        self.pos2 = Position(
            id="pos2",
            name="Position 2",
            description="Second position",
            advantages=["Adv2"],
            common_mistakes=["Mistake2"]
        )
    
    def test_add_position(self):
        """Test adding positions to graph"""
        self.graph.add_position(self.pos1)
        self.assertEqual(len(self.graph.positions), 1)
        self.assertIn("pos1", self.graph.positions)
    
    def test_get_position(self):
        """Test retrieving positions from graph"""
        self.graph.add_position(self.pos1)
        retrieved = self.graph.get_position("pos1")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Position 1")
    
    def test_add_transition(self):
        """Test adding transitions to graph"""
        self.graph.add_position(self.pos1)
        self.graph.add_position(self.pos2)
        
        transition = Transition(
            from_position="pos1",
            to_position="pos2",
            action="Test action",
            opponent_reaction="Test reaction",
            probability=0.8,
            decision_quality=DecisionQuality.EXCELLENT
        )
        
        self.graph.add_transition(transition)
        self.assertEqual(len(self.graph.transitions), 1)
    
    def test_get_transitions_from(self):
        """Test getting transitions from a position"""
        self.graph.add_position(self.pos1)
        self.graph.add_position(self.pos2)
        
        transition = Transition(
            from_position="pos1",
            to_position="pos2",
            action="Test action",
            opponent_reaction="Test reaction",
            probability=0.8,
            decision_quality=DecisionQuality.EXCELLENT
        )
        
        self.graph.add_transition(transition)
        transitions = self.graph.get_transitions_from("pos1")
        self.assertEqual(len(transitions), 1)
        self.assertEqual(transitions[0].action, "Test action")


class TestSampleGraph(unittest.TestCase):
    """Test the sample BJJ graph"""
    
    def setUp(self):
        """Set up sample graph"""
        self.graph = create_sample_graph()
    
    def test_sample_graph_has_positions(self):
        """Test that sample graph has positions"""
        self.assertGreater(len(self.graph.positions), 0)
        self.assertIn("closed_guard", self.graph.positions)
    
    def test_sample_graph_has_transitions(self):
        """Test that sample graph has transitions"""
        transitions = self.graph.get_transitions_from("closed_guard")
        self.assertGreater(len(transitions), 0)
    
    def test_closed_guard_position(self):
        """Test closed guard position details"""
        pos = self.graph.get_position("closed_guard")
        self.assertIsNotNone(pos)
        self.assertEqual(pos.name, "Closed Guard")
        self.assertGreater(len(pos.advantages), 0)
        self.assertGreater(len(pos.common_mistakes), 0)


class TestNarrativeEngine(unittest.TestCase):
    """Test narrative engine"""
    
    def setUp(self):
        """Set up engine with sample graph"""
        self.graph = create_sample_graph()
        self.engine = NarrativeEngine(self.graph)
    
    def test_start_session(self):
        """Test starting a narrative session"""
        session = self.engine.start_session("closed_guard")
        self.assertIsNotNone(session)
        self.assertEqual(session.current_position, "closed_guard")
    
    def test_get_current_position(self):
        """Test getting current position in session"""
        session = self.engine.start_session("closed_guard")
        pos = session.get_current_position()
        self.assertIsNotNone(pos)
        self.assertEqual(pos.id, "closed_guard")
    
    def test_get_available_actions(self):
        """Test getting available actions"""
        session = self.engine.start_session("closed_guard")
        actions = session.get_available_actions()
        self.assertGreater(len(actions), 0)
    
    def test_take_action(self):
        """Test taking an action in the narrative"""
        session = self.engine.start_session("closed_guard")
        transitions = session.get_available_actions()
        
        if transitions:
            initial_pos = session.current_position
            new_pos, drill = session.take_action(transitions[0])
            self.assertIsNotNone(new_pos)
            # Position should change (unless it loops back)
            self.assertIn(new_pos.id, self.graph.positions)
    
    def test_session_history(self):
        """Test that session tracks history"""
        session = self.engine.start_session("closed_guard")
        transitions = session.get_available_actions()
        
        if transitions:
            session.take_action(transitions[0])
            self.assertGreater(len(session.history), 0)
    
    def test_session_summary(self):
        """Test session summary generation"""
        session = self.engine.start_session("closed_guard")
        summary = session.get_session_summary()
        
        self.assertIn("positions_visited", summary)
        self.assertIn("total_drills", summary)
        self.assertIn("drills", summary)


class TestNarrativeFormatting(unittest.TestCase):
    """Test narrative display formatting"""
    
    def setUp(self):
        """Set up engine"""
        self.graph = create_sample_graph()
        self.engine = NarrativeEngine(self.graph)
    
    def test_format_position_display(self):
        """Test position formatting"""
        pos = self.graph.get_position("closed_guard")
        display = self.engine.format_position_display(pos)
        self.assertIn("Closed Guard", display)
        self.assertIn("POSITION:", display)
    
    def test_format_transitions_display(self):
        """Test transitions formatting"""
        transitions = self.graph.get_transitions_from("closed_guard")
        display = self.engine.format_transitions_display(transitions)
        self.assertIn("AVAILABLE ACTIONS:", display)
    
    def test_format_drill_display(self):
        """Test drill formatting"""
        drill = DrillPrescription(
            name="Test Drill",
            description="Test description",
            repetitions=10,
            focus_points=["Point 1", "Point 2"]
        )
        display = self.engine.format_drill_display(drill)
        self.assertIn("DRILL PRESCRIPTION:", display)
        self.assertIn("Test Drill", display)


if __name__ == "__main__":
    unittest.main()
