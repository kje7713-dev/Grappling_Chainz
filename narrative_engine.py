"""
Narrative Drill-Through Engine

Decision-tree based engine for drilling through situational BJJ narratives.
Users explore opponent reactions and receive drill prescriptions.
"""

from typing import List, Optional, Tuple
from bjj_domain import BJJGraph, Position, Transition, DrillPrescription
import random


class NarrativeSession:
    """A drill-through training session with narrative continuity"""
    
    def __init__(self, graph: BJJGraph, starting_position: str):
        self.graph = graph
        self.current_position = starting_position
        self.history: List[Tuple[str, str]] = []  # (position_id, action taken)
        self.drills_earned: List[DrillPrescription] = []
    
    def get_current_position(self) -> Optional[Position]:
        """Get the current position in the narrative"""
        return self.graph.get_position(self.current_position)
    
    def get_available_actions(self) -> List[Transition]:
        """Get available transitions from current position"""
        transitions = self.graph.get_transitions_from(self.current_position)
        # Sort by probability (highest first) for better UX
        return sorted(transitions, key=lambda t: t.probability, reverse=True)
    
    def take_action(self, transition: Transition) -> Tuple[Position, DrillPrescription]:
        """
        Execute a transition and receive drill prescription.
        Returns the new position and the drill to practice.
        """
        # Record history
        self.history.append((self.current_position, transition.action))
        
        # Get drill prescription
        drill = self.graph.get_drill_for_transition(transition)
        if drill:
            self.drills_earned.append(drill)
        
        # Move to new position
        self.current_position = transition.to_position
        new_position = self.graph.get_position(self.current_position)
        
        return new_position, drill
    
    def get_session_summary(self) -> dict:
        """Get summary of the training session"""
        return {
            "positions_visited": len(self.history) + 1,
            "actions_taken": [action for _, action in self.history],
            "total_drills": len(self.drills_earned),
            "drills": self.drills_earned
        }


class NarrativeEngine:
    """Main engine for drill-through narrative experience"""
    
    def __init__(self, graph: BJJGraph):
        self.graph = graph
    
    def start_session(self, starting_position: str = "closed_guard") -> NarrativeSession:
        """Start a new narrative drill session"""
        return NarrativeSession(self.graph, starting_position)
    
    def format_position_display(self, position: Position) -> str:
        """Format position information for display"""
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"POSITION: {position.name}")
        lines.append(f"{'='*60}")
        lines.append(f"\n{position.description}")
        lines.append(f"\nAdvantages:")
        for advantage in position.advantages:
            lines.append(f"  • {advantage}")
        lines.append(f"\nCommon Mistakes to Avoid:")
        for mistake in position.common_mistakes:
            lines.append(f"  ⚠ {mistake}")
        return "\n".join(lines)
    
    def format_transitions_display(self, transitions: List[Transition]) -> str:
        """Format available transitions for display"""
        if not transitions:
            return "\nNo transitions available from this position."
        
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append("AVAILABLE ACTIONS:")
        lines.append(f"{'='*60}")
        
        for i, transition in enumerate(transitions, 1):
            lines.append(f"\n[{i}] {transition.action}")
            lines.append(f"    Likely Reaction: {transition.opponent_reaction}")
            lines.append(f"    Success Probability: {transition.probability:.0%}")
            lines.append(f"    Decision Quality: {transition.decision_quality.value.upper()}")
        
        return "\n".join(lines)
    
    def format_drill_display(self, drill: Optional[DrillPrescription]) -> str:
        """Format drill prescription for display"""
        if not drill:
            return "\nNo specific drill prescribed for this transition."
        
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append("DRILL PRESCRIPTION:")
        lines.append(f"{'='*60}")
        lines.append(f"\n📋 {drill.name}")
        lines.append(f"\n{drill.description}")
        lines.append(f"\nRepetitions: {drill.repetitions}")
        lines.append(f"\nFocus Points:")
        for point in drill.focus_points:
            lines.append(f"  ✓ {point}")
        return "\n".join(lines)
    
    def format_session_summary(self, session: NarrativeSession) -> str:
        """Format the session summary"""
        summary = session.get_session_summary()
        
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append("SESSION SUMMARY")
        lines.append(f"{'='*60}")
        lines.append(f"\nPositions Explored: {summary['positions_visited']}")
        lines.append(f"Drills Earned: {summary['total_drills']}")
        
        if summary['drills']:
            lines.append(f"\n{'='*60}")
            lines.append("YOUR DRILL PROGRAM:")
            lines.append(f"{'='*60}")
            for i, drill in enumerate(summary['drills'], 1):
                lines.append(f"\n{i}. {drill.name}")
                lines.append(f"   • {drill.description}")
                lines.append(f"   • {drill.repetitions} repetitions")
        
        return "\n".join(lines)
