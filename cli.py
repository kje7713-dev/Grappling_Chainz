#!/usr/bin/env python3
"""
BJJ Drill-Through Narrative App - CLI Interface

Interactive command-line interface for drilling through BJJ situational narratives.
"""

import sys
from bjj_domain import create_sample_graph
from narrative_engine import NarrativeEngine


def print_welcome():
    """Print welcome message"""
    print("\n" + "="*60)
    print("BJJ DRILL-THROUGH NARRATIVE APP")
    print("="*60)
    print("\nWelcome to the Brazilian Jiu-Jitsu training decision tree!")
    print("Navigate through positions, explore opponent reactions,")
    print("and earn drill prescriptions to improve your game.")
    print("\nType 'quit' or 'exit' at any time to end the session.")
    print("="*60)


def get_user_choice(max_choice: int) -> int:
    """Get and validate user's action choice"""
    while True:
        try:
            choice = input(f"\nSelect an action (1-{max_choice}), or 'quit' to end: ").strip().lower()
            
            if choice in ['quit', 'exit', 'q']:
                return -1
            
            choice_num = int(choice)
            if 1 <= choice_num <= max_choice:
                return choice_num
            else:
                print(f"Please enter a number between 1 and {max_choice}.")
        except ValueError:
            print("Please enter a valid number or 'quit'.")


def run_interactive_session():
    """Run an interactive drill-through session"""
    print_welcome()
    
    # Initialize the graph and engine
    graph = create_sample_graph()
    engine = NarrativeEngine(graph)
    
    # Start session
    print("\nStarting position: Closed Guard")
    session = engine.start_session("closed_guard")
    
    # Main interaction loop
    while True:
        # Display current position
        current_pos = session.get_current_position()
        if not current_pos:
            print("\nError: Invalid position state.")
            break
        
        print(engine.format_position_display(current_pos))
        
        # Get available actions
        transitions = session.get_available_actions()
        
        if not transitions:
            print("\nYou've reached a terminal position in this narrative.")
            break
        
        # Display transitions
        print(engine.format_transitions_display(transitions))
        
        # Get user choice
        choice = get_user_choice(len(transitions))
        
        if choice == -1:
            print("\nEnding session...")
            break
        
        # Execute chosen transition
        selected_transition = transitions[choice - 1]
        new_position, drill = session.take_action(selected_transition)
        
        # Show result
        print(f"\n{'='*60}")
        print(f"RESULT: {selected_transition.opponent_reaction}")
        print(f"{'='*60}")
        
        # Display drill prescription
        print(engine.format_drill_display(drill))
        
        # Check if new position is valid
        if not new_position:
            print("\nError: Unable to transition to new position.")
            break
        
        # Ask if user wants to continue
        print(f"\nYou are now in: {new_position.name}")
        continue_choice = input("\nPress Enter to continue, or type 'quit' to end: ").strip().lower()
        
        if continue_choice in ['quit', 'exit', 'q']:
            print("\nEnding session...")
            break
    
    # Show session summary
    print(engine.format_session_summary(session))
    print("\n" + "="*60)
    print("Thank you for training! Practice your drills! 🥋")
    print("="*60 + "\n")


def main():
    """Main entry point"""
    try:
        run_interactive_session()
    except KeyboardInterrupt:
        print("\n\nSession interrupted. Thank you for training! 🥋\n")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
