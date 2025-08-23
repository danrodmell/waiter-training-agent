#!/usr/bin/env python3
"""
Main entry point for the Waiter Training Agent
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.agent import WaiterTrainingAgent
from src.utils.helpers import ensure_directories, validate_config


async def main():
    """Main application function"""
    print("🍽️  Waiter Training Agent")
    print("=" * 50)
    
    # Ensure directories exist
    ensure_directories({})
    
    try:
        # Initialize the agent
        print("Initializing Waiter Training Agent...")
        agent = WaiterTrainingAgent()
        
        # Validate configuration
        if not validate_config(agent.config):
            print("❌ Configuration validation failed. Please check your config.yaml file.")
            return
        
        print("✅ Agent initialized successfully!")
        print(f"Available training categories: {', '.join(agent.get_available_categories())}")
        print(f"Difficulty levels: {', '.join(agent.get_difficulty_levels())}")
        
        # Interactive demo mode
        await interactive_demo(agent)
        
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        print("Please check your configuration and dependencies.")


async def interactive_demo(agent: WaiterTrainingAgent):
    """Run an interactive demo of the training agent"""
    print("\n🎯 Interactive Training Demo")
    print("=" * 50)
    
    # Get waiter name
    waiter_name = input("Enter waiter name: ").strip() or "Demo Waiter"
    
    # Get difficulty level
    difficulty_levels = agent.get_difficulty_levels()
    print(f"\nSelect difficulty level: {', '.join(difficulty_levels)}")
    difficulty = input("Difficulty (default: beginner): ").strip().lower() or "beginner"
    
    if difficulty not in difficulty_levels:
        difficulty = "beginner"
        print(f"Invalid difficulty level. Using {difficulty}.")
    
    # Start training session
    print(f"\n🚀 Starting training session for {waiter_name} ({difficulty} level)")
    session_id = await agent.start_training_session(waiter_name, difficulty)
    print(f"Session ID: {session_id}")
    
    # Training loop
    while True:
        print("\n" + "=" * 50)
        
        # Get current session status
        status = agent.get_session_status(session_id)
        if not status:
            print("❌ Session not found!")
            break
        
        print(f"Current Score: {status['current_score']:.1f}")
        print(f"Scenarios Completed: {len(status['scenarios_completed'])}")
        
        # Get next scenario
        scenario = await agent.get_training_scenario(session_id)
        print(f"\n📋 Training Scenario: {scenario['category'].replace('_', ' ').title()}")
        print(f"Difficulty: {scenario['difficulty']}")
        print("\n" + scenario['prompt'])
        
        # Get waiter response
        print("\n💬 Enter your response (or 'quit' to end session):")
        waiter_response = input("> ").strip()
        
        if waiter_response.lower() in ['quit', 'exit', 'end']:
            break
        
        if not waiter_response:
            print("Please provide a response to continue training.")
            continue
        
        # Process response
        print("\n🔄 Processing response...")
        result = await agent.process_waiter_response(session_id, scenario['category'], waiter_response)
        
        print(f"\n📝 Feedback: {result['feedback']}")
        print(f"New Score: {result['score']:.1f}")
        print(f"Next Scenario: {result['next_scenario']}")
        
        # Ask if they want to continue
        continue_training = input("\nContinue training? (y/n): ").strip().lower()
        if continue_training not in ['y', 'yes']:
            break
    
    # End session
    print("\n🏁 Ending training session...")
    summary = await agent.end_training_session(session_id)
    
    print("\n📊 Training Session Summary")
    print("=" * 50)
    print(f"Waiter: {summary['waiter_name']}")
    print(f"Duration: {summary['duration_minutes']:.1f} minutes")
    print(f"Final Score: {summary['final_score']:.1f}")
    print(f"Scenarios Completed: {len(summary['scenarios_completed'])}")
    print(f"Completion Rate: {summary['completion_rate']:.1f}%")
    print(f"Total Feedback: {summary['total_feedback']}")
    
    print("\n🎉 Training session completed! Thank you for using the Waiter Training Agent.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Training session interrupted.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 