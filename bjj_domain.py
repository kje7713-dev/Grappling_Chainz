"""
BJJ Domain Models and Graph Engine

Core domain models for Brazilian Jiu-Jitsu position ontology,
transitions, and drill prescriptions.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import networkx as nx


class DecisionQuality(Enum):
    """Quality assessment of a decision made during training"""
    EXCELLENT = "excellent"
    GOOD = "good"
    POOR = "poor"
    FAILURE = "failure"


@dataclass
class DrillPrescription:
    """Drill recommendation based on position and decision quality"""
    name: str
    description: str
    repetitions: int
    focus_points: List[str]
    
    def __str__(self):
        return f"{self.name} ({self.repetitions} reps): {self.description}"


@dataclass
class Position:
    """BJJ position/game state in the position ontology"""
    id: str
    name: str
    description: str
    advantages: List[str]
    common_mistakes: List[str]
    default_drills: List[DrillPrescription] = field(default_factory=list)
    
    def __str__(self):
        return f"{self.name}: {self.description}"


@dataclass
class Transition:
    """Probability-weighted transition between positions"""
    from_position: str
    to_position: str
    action: str
    opponent_reaction: str
    probability: float  # 0.0 to 1.0
    decision_quality: DecisionQuality
    drill_prescription: Optional[DrillPrescription] = None
    
    def __str__(self):
        return f"{self.action} -> {self.opponent_reaction} ({self.probability:.0%})"


class BJJGraph:
    """Graph-based domain engine for BJJ positions and transitions"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.positions: Dict[str, Position] = {}
        self.transitions: List[Transition] = []
    
    def add_position(self, position: Position):
        """Add a position to the ontology"""
        self.positions[position.id] = position
        self.graph.add_node(position.id, data=position)
    
    def add_transition(self, transition: Transition):
        """Add a probability-weighted transition"""
        self.transitions.append(transition)
        self.graph.add_edge(
            transition.from_position,
            transition.to_position,
            data=transition
        )
    
    def get_position(self, position_id: str) -> Optional[Position]:
        """Get position by ID"""
        return self.positions.get(position_id)
    
    def get_transitions_from(self, position_id: str) -> List[Transition]:
        """Get all possible transitions from a position"""
        transitions = []
        if position_id in self.graph:
            for _, to_pos, edge_data in self.graph.edges(position_id, data=True):
                transitions.append(edge_data['data'])
        return transitions
    
    def get_drill_for_transition(self, transition: Transition) -> Optional[DrillPrescription]:
        """Get drill prescription for a specific transition and decision quality"""
        return transition.drill_prescription
    
    def get_position_drills(self, position_id: str) -> List[DrillPrescription]:
        """Get default drills for a position"""
        position = self.get_position(position_id)
        return position.default_drills if position else []


def create_sample_graph() -> BJJGraph:
    """Create a sample BJJ position graph with common positions and transitions"""
    graph = BJJGraph()
    
    # Define positions
    closed_guard = Position(
        id="closed_guard",
        name="Closed Guard",
        description="Bottom player has legs locked around opponent's waist",
        advantages=["Control opponent's posture", "Can break posture", "Multiple attack options"],
        common_mistakes=["Flat back", "Not breaking posture", "Passive play"],
        default_drills=[
            DrillPrescription(
                name="Posture Break Drill",
                description="Practice breaking opponent's posture from closed guard",
                repetitions=10,
                focus_points=["Pull down on neck", "Extend hips", "Control sleeves"]
            )
        ]
    )
    
    broken_posture = Position(
        id="broken_posture",
        name="Broken Posture in Guard",
        description="Opponent's posture is broken, chest close to guard player",
        advantages=["Can setup submissions", "Can setup sweeps", "Opponent limited movement"],
        common_mistakes=["Letting posture recover", "Not transitioning to attack"],
        default_drills=[
            DrillPrescription(
                name="Kimura Setup Drill",
                description="Practice kimura grip and control from broken posture",
                repetitions=8,
                focus_points=["Figure-4 grip", "Control wrist", "Hip out"]
            )
        ]
    )
    
    kimura_position = Position(
        id="kimura_position",
        name="Kimura Position",
        description="Figure-4 grip secured on opponent's arm",
        advantages=["Submission threat", "Can sweep", "Strong control"],
        common_mistakes=["Losing grip", "Not using hips", "Poor angle"],
        default_drills=[
            DrillPrescription(
                name="Kimura Finish Drill",
                description="Practice finishing kimura from guard",
                repetitions=10,
                focus_points=["Maintain grip", "Walk legs up", "Apply pressure slowly"]
            )
        ]
    )
    
    sweep_position = Position(
        id="sweep_position",
        name="Sweep Transition",
        description="In process of off-balancing opponent for sweep",
        advantages=["Momentum on your side", "Can reverse position", "Score points"],
        common_mistakes=["Half-committed", "Poor timing", "Losing grips"],
        default_drills=[
            DrillPrescription(
                name="Kimura Sweep Drill",
                description="Practice sweep using kimura grip",
                repetitions=10,
                focus_points=["Drive with legs", "Pull with arms", "Follow through"]
            )
        ]
    )
    
    mount = Position(
        id="mount",
        name="Mount",
        description="Top position with knees on ground, sitting on opponent's torso",
        advantages=["Dominant position", "Many submission options", "Point scoring position"],
        common_mistakes=["Too high", "Poor base", "Not controlling arms"],
        default_drills=[
            DrillPrescription(
                name="Mount Maintenance Drill",
                description="Practice maintaining mount against escape attempts",
                repetitions=5,
                focus_points=["Wide base", "Heavy hips", "Control head"]
            )
        ]
    )
    
    # Add positions to graph
    for position in [closed_guard, broken_posture, kimura_position, sweep_position, mount]:
        graph.add_position(position)
    
    # Define transitions with probability weights and drills
    
    # From closed guard: break posture
    graph.add_transition(Transition(
        from_position="closed_guard",
        to_position="broken_posture",
        action="Pull down on opponent's head while extending hips",
        opponent_reaction="Opponent's posture breaks forward",
        probability=0.7,
        decision_quality=DecisionQuality.GOOD,
        drill_prescription=DrillPrescription(
            name="Posture Break Repetition Drill",
            description="Rapid fire posture breaks",
            repetitions=15,
            focus_points=["Timing", "Hip extension", "Grip strength"]
        )
    ))
    
    # Failed posture break
    graph.add_transition(Transition(
        from_position="closed_guard",
        to_position="closed_guard",
        action="Weak posture break attempt",
        opponent_reaction="Opponent maintains posture",
        probability=0.3,
        decision_quality=DecisionQuality.POOR,
        drill_prescription=DrillPrescription(
            name="Posture Break Fundamentals",
            description="Focus on proper mechanics of posture breaking",
            repetitions=20,
            focus_points=["Full extension", "Strong grips", "Core engagement"]
        )
    ))
    
    # From broken posture: go for kimura
    graph.add_transition(Transition(
        from_position="broken_posture",
        to_position="kimura_position",
        action="Trap arm and secure figure-4 grip",
        opponent_reaction="Opponent's arm gets trapped",
        probability=0.6,
        decision_quality=DecisionQuality.EXCELLENT,
        drill_prescription=DrillPrescription(
            name="Kimura Entry Drill",
            description="Practice smooth entry to kimura grip",
            repetitions=12,
            focus_points=["Hand placement", "Quick entry", "Maintain chest control"]
        )
    ))
    
    # From kimura: go for sweep
    graph.add_transition(Transition(
        from_position="kimura_position",
        to_position="sweep_position",
        action="Use kimura grip to off-balance and sweep",
        opponent_reaction="Opponent gets swept",
        probability=0.5,
        decision_quality=DecisionQuality.EXCELLENT,
        drill_prescription=DrillPrescription(
            name="Kimura Sweep Chain",
            description="Practice kimura sweep with proper momentum",
            repetitions=10,
            focus_points=["Hip bump", "Pull with grip", "Come up on top"]
        )
    ))
    
    # Successful sweep to mount
    graph.add_transition(Transition(
        from_position="sweep_position",
        to_position="mount",
        action="Complete the sweep and establish mount",
        opponent_reaction="You achieve mount position",
        probability=0.8,
        decision_quality=DecisionQuality.EXCELLENT,
        drill_prescription=DrillPrescription(
            name="Sweep to Mount Transition",
            description="Practice smooth transition from sweep to mount",
            repetitions=8,
            focus_points=["Stay tight", "Control head", "Establish hooks"]
        )
    ))
    
    return graph
