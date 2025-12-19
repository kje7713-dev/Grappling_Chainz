# BJJ Drill-Through Narrative App

A decision-tree–based Brazilian Jiu-Jitsu training app that allows users to drill through situational narratives, explore likely opponent reactions, and receive drill prescriptions tied to decision quality.

## Core Concepts

### Position Ontology (Game States)
- **Graph-based representation** of BJJ positions
- Each position includes: name, description, advantages, and common mistakes
- Positions form nodes in the decision tree

### Probability-Weighted Transitions
- Transitions between positions have success probabilities
- Each transition represents an action and likely opponent reaction
- Probability reflects real-world likelihood of successful execution

### Narrative Continuity
- Interactive drill-through sessions maintain continuity
- Users progress through a story of position changes
- Session history tracks the path taken

### Drill Prescriptions
- Each transition generates specific drill recommendations
- Drills are tied to decision quality (excellent, good, poor, failure)
- Focus points guide practice for technique improvement

## Architecture

### Graph-Based Domain Engine
The app uses NetworkX to create a directed graph where:
- **Nodes** = BJJ positions (game states)
- **Edges** = Transitions with probability weights and drill prescriptions
- **Queries** = Fast lookup of positions and available transitions

### Components

1. **`bjj_domain.py`** - Core domain models
   - `Position`: BJJ position/game state
   - `Transition`: Probability-weighted edge between positions
   - `DrillPrescription`: Drill recommendation
   - `BJJGraph`: Graph engine managing positions and transitions

2. **`narrative_engine.py`** - Decision tree logic
   - `NarrativeSession`: Manages user drill-through session
   - `NarrativeEngine`: Formats and presents narrative elements

3. **`cli.py`** - Command-line interface
   - Interactive drill-through experience
   - User-friendly display of positions and choices

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kje7713-dev/Grappling_Chainz.git
cd Grappling_Chainz
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the interactive CLI:
```bash
python cli.py
```

### Example Session Flow

1. Start in **Closed Guard** position
2. View advantages, common mistakes, and available actions
3. Choose an action (e.g., "Break opponent's posture")
4. See opponent reaction and success probability
5. Receive drill prescription based on decision quality
6. Move to next position and repeat

## Running Tests

Run the test suite:
```bash
python -m unittest test_bjj_app.py
```

Or run tests with verbose output:
```bash
python -m unittest test_bjj_app.py -v
```

## Sample Positions Included

- **Closed Guard**: Bottom player controls with legs locked
- **Broken Posture**: Opponent's posture compromised
- **Kimura Position**: Figure-4 grip secured on arm
- **Sweep Transition**: Off-balancing opponent
- **Mount**: Dominant top position

## Extending the App

To add new positions and transitions:

1. Create new `Position` objects with attributes
2. Define `Transition` objects with probabilities
3. Add `DrillPrescription` objects for training
4. Register in the graph using `add_position()` and `add_transition()`

Example:
```python
from bjj_domain import Position, Transition, DrillPrescription, DecisionQuality

# Create a new position
side_control = Position(
    id="side_control",
    name="Side Control",
    description="Dominant side position",
    advantages=["Heavy pressure", "Multiple submissions"],
    common_mistakes=["Leaving space", "Poor weight distribution"]
)

# Add to graph
graph.add_position(side_control)

# Create transition
transition = Transition(
    from_position="mount",
    to_position="side_control",
    action="Step over to side control",
    opponent_reaction="Opponent escapes to side",
    probability=0.4,
    decision_quality=DecisionQuality.POOR,
    drill_prescription=DrillPrescription(...)
)

graph.add_transition(transition)
```

## Status

🚧 Early design + prototyping

The app currently includes:
- ✅ Graph-based position ontology
- ✅ Probability-weighted transitions
- ✅ Narrative continuity engine
- ✅ Drill prescription system
- ✅ Interactive CLI
- ✅ Sample BJJ positions and transitions
- ✅ Unit tests

## Tech Stack

- **Python 3.7+**
- **NetworkX** - Graph data structure and algorithms
- **Standard Library** - dataclasses, enum, typing

## Future Enhancements

- Add more positions and transitions
- Implement web interface
- Add user progress tracking
- Create drill video database
- Add machine learning for personalized recommendations
- Support for different skill levels
- Position visualization

## Contributing

Contributions are welcome! Areas for contribution:
- Additional positions and transitions
- More drill prescriptions
- UI improvements
- Test coverage expansion
- Documentation improvements

## License

MIT License - See LICENSE file for details