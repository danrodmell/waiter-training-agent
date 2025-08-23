"""
Waiter Training Agent - Main AI agent for training restaurant waiters
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

import openai
from pydantic import BaseModel

from .training_scenarios import TrainingScenario
from ..utils.helpers import load_config, setup_logging


@dataclass
class TrainingSession:
    """Represents a training session for a waiter"""
    session_id: str
    waiter_name: str
    difficulty_level: str
    start_time: datetime
    scenarios_completed: List[str]
    score: float
    feedback: List[str]


class WaiterTrainingAgent:
    """
    AI-powered agent for training restaurant waiters
    """
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = load_config(config_path)
        self.logger = setup_logging(self.config.get("logging", {}))
        
        # Initialize OpenAI client
        openai.api_key = self.config.get("ai", {}).get("openai_api_key")
        self.model = self.config.get("ai", {}).get("model", "gpt-4")
        self.temperature = self.config.get("ai", {}).get("temperature", 0.7)
        
        # Initialize training scenarios
        self.scenarios = self._load_training_scenarios()
        self.active_sessions: Dict[str, TrainingSession] = {}
        
        self.logger.info("Waiter Training Agent initialized successfully")
    
    def _load_training_scenarios(self) -> Dict[str, TrainingScenario]:
        """Load training scenarios from configuration"""
        scenarios = {}
        scenario_categories = self.config.get("training", {}).get("scenario_categories", [])
        
        for category in scenario_categories:
            scenarios[category] = TrainingScenario(
                category=category,
                difficulty_levels=self.config.get("training", {}).get("difficulty_levels", [])
            )
        
        return scenarios
    
    async def start_training_session(self, waiter_name: str, difficulty_level: str = "beginner") -> str:
        """Start a new training session for a waiter"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{waiter_name}"
        
        session = TrainingSession(
            session_id=session_id,
            waiter_name=waiter_name,
            difficulty_level=difficulty_level,
            start_time=datetime.now(),
            scenarios_completed=[],
            score=0.0,
            feedback=[]
        )
        
        self.active_sessions[session_id] = session
        self.logger.info(f"Started training session {session_id} for {waiter_name}")
        
        return session_id
    
    async def get_training_scenario(self, session_id: str, category: str = None) -> Dict[str, Any]:
        """Get a training scenario for the current session"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        
        if category is None:
            # Select a random category
            import random
            available_categories = list(self.scenarios.keys())
            category = random.choice(available_categories)
        
        if category not in self.scenarios:
            raise ValueError(f"Category {category} not found")
        
        scenario = self.scenarios[category]
        training_prompt = scenario.generate_prompt(session.difficulty_level)
        
        return {
            "category": category,
            "prompt": training_prompt,
            "difficulty": session.difficulty_level,
            "session_id": session_id
        }
    
    async def process_waiter_response(self, session_id: str, scenario_category: str, 
                                    waiter_response: str) -> Dict[str, Any]:
        """Process a waiter's response to a training scenario"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        
        # Generate AI feedback
        feedback = await self._generate_feedback(scenario_category, waiter_response, session.difficulty_level)
        
        # Update session
        if scenario_category not in session.scenarios_completed:
            session.scenarios_completed.append(scenario_category)
        
        session.feedback.append(feedback)
        
        # Calculate score (simplified scoring system)
        session.score = min(100.0, session.score + 10.0)
        
        return {
            "feedback": feedback,
            "score": session.score,
            "scenarios_completed": len(session.scenarios_completed),
            "next_scenario": await self._suggest_next_scenario(session)
        }
    
    async def _generate_feedback(self, category: str, response: str, difficulty: str) -> str:
        """Generate AI feedback for a waiter's response"""
        prompt = f"""
        You are an expert restaurant trainer evaluating a waiter's response to a training scenario.
        
        Category: {category}
        Difficulty Level: {difficulty}
        Waiter's Response: {response}
        
        Please provide constructive feedback that:
        1. Acknowledges what was done well
        2. Suggests specific improvements
        3. Provides actionable advice
        4. Maintains a positive, encouraging tone
        
        Keep the feedback concise but helpful (2-3 sentences).
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            self.logger.error(f"Error generating feedback: {e}")
            return "Thank you for your response. I'm having trouble processing feedback right now, but please continue with the training."
    
    async def _suggest_next_scenario(self, session: TrainingSession) -> str:
        """Suggest the next training scenario based on progress"""
        completed = set(session.scenarios_completed)
        all_categories = set(self.scenarios.keys())
        
        # Find uncompleted categories
        remaining = all_categories - completed
        
        if not remaining:
            return "Congratulations! You've completed all training scenarios."
        
        # Suggest a category that hasn't been completed
        import random
        return random.choice(list(remaining))
    
    async def end_training_session(self, session_id: str) -> Dict[str, Any]:
        """End a training session and provide summary"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.active_sessions[session_id]
        end_time = datetime.now()
        duration = (end_time - session.start_time).total_seconds() / 60  # minutes
        
        summary = {
            "session_id": session_id,
            "waiter_name": session.waiter_name,
            "duration_minutes": round(duration, 2),
            "final_score": session.score,
            "scenarios_completed": session.scenarios_completed,
            "total_feedback": len(session.feedback),
            "completion_rate": len(session.scenarios_completed) / len(self.scenarios) * 100
        }
        
        # Remove from active sessions
        del self.active_sessions[session_id]
        
        self.logger.info(f"Ended training session {session_id} for {session.waiter_name}")
        
        return summary
    
    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a training session"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        return {
            "session_id": session_id,
            "waiter_name": session.waiter_name,
            "difficulty_level": session.difficulty_level,
            "start_time": session.start_time.isoformat(),
            "scenarios_completed": session.scenarios_completed,
            "current_score": session.score,
            "feedback_count": len(session.feedback)
        }
    
    def get_available_categories(self) -> List[str]:
        """Get list of available training categories"""
        return list(self.scenarios.keys())
    
    def get_difficulty_levels(self) -> List[str]:
        """Get available difficulty levels"""
        return self.config.get("training", {}).get("difficulty_levels", [])
 