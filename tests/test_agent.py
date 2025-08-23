"""
Tests for the Waiter Training Agent
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.agent import WaiterTrainingAgent, TrainingSession
from src.agent.training_scenarios import TrainingScenario


class TestTrainingScenario:
    """Test the TrainingScenario class"""
    
    def test_scenario_creation(self):
        """Test creating a training scenario"""
        scenario = TrainingScenario(
            category="customer_greeting",
            difficulty_levels=["beginner", "intermediate", "advanced"]
        )
        
        assert scenario.category == "customer_greeting"
        assert scenario.difficulty_levels == ["beginner", "intermediate", "advanced"]
    
    def test_generate_prompt_beginner(self):
        """Test generating a beginner level prompt"""
        scenario = TrainingScenario(
            category="customer_greeting",
            difficulty_levels=["beginner", "intermediate", "advanced"]
        )
        
        prompt = scenario.generate_prompt("beginner")
        assert "beginner" in prompt.lower()
        assert "customer" in prompt.lower()
    
    def test_generate_prompt_invalid_difficulty(self):
        """Test generating prompt with invalid difficulty level"""
        scenario = TrainingScenario(
            category="customer_greeting",
            difficulty_levels=["beginner", "intermediate", "advanced"]
        )
        
        prompt = scenario.generate_prompt("expert")
        assert "beginner" in prompt.lower()  # Should default to beginner
    
    def test_get_scenario_summary(self):
        """Test getting scenario summary"""
        scenario = TrainingScenario(
            category="customer_greeting",
            difficulty_levels=["beginner", "intermediate", "advanced"]
        )
        
        summary = scenario.get_scenario_summary()
        assert summary["category"] == "customer_greeting"
        assert "first impressions" in summary["description"].lower()


class TestWaiterTrainingAgent:
    """Test the WaiterTrainingAgent class"""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing"""
        return {
            "agent": {"name": "Test Agent"},
            "training": {
                "difficulty_levels": ["beginner", "intermediate", "advanced"],
                "scenario_categories": ["customer_greeting", "menu_knowledge"]
            },
            "ai": {
                "model": "gpt-4",
                "temperature": 0.7,
                "openai_api_key": "test_key"
            },
            "logging": {"level": "INFO"}
        }
    
    @patch('src.agent.openai')
    @patch('src.utils.helpers.load_config')
    @patch('src.utils.helpers.setup_logging')
    def test_agent_initialization(self, mock_setup_logging, mock_load_config, mock_openai):
        """Test agent initialization"""
        mock_load_config.return_value = self.mock_config()
        mock_logger = Mock()
        mock_setup_logging.return_value = mock_logger
        
        agent = WaiterTrainingAgent()
        
        assert agent.model == "gpt-4"
        assert agent.temperature == 0.7
        assert len(agent.scenarios) == 2
        assert "customer_greeting" in agent.scenarios
        assert "menu_knowledge" in agent.scenarios
    
    @pytest.mark.asyncio
    @patch('src.agent.openai')
    @patch('src.utils.helpers.load_config')
    @patch('src.utils.helpers.setup_logging')
    async def test_start_training_session(self, mock_setup_logging, mock_load_config, mock_openai):
        """Test starting a training session"""
        mock_load_config.return_value = self.mock_config()
        mock_logger = Mock()
        mock_setup_logging.return_value = mock_logger
        
        agent = WaiterTrainingAgent()
        session_id = await agent.start_training_session("John Doe", "intermediate")
        
        assert session_id.startswith("session_")
        assert "John Doe" in session_id
        assert session_id in agent.active_sessions
        
        session = agent.active_sessions[session_id]
        assert session.waiter_name == "John Doe"
        assert session.difficulty_level == "intermediate"
        assert session.score == 0.0
        assert len(session.scenarios_completed) == 0
    
    @pytest.mark.asyncio
    @patch('src.agent.openai')
    @patch('src.utils.helpers.load_config')
    @patch('src.utils.helpers.setup_logging')
    async def test_get_training_scenario(self, mock_setup_logging, mock_load_config, mock_openai):
        """Test getting a training scenario"""
        mock_load_config.return_value = self.mock_config()
        mock_logger = Mock()
        mock_setup_logging.return_value = mock_logger
        
        agent = WaiterTrainingAgent()
        session_id = await agent.start_training_session("Jane Doe", "beginner")
        
        scenario = await agent.get_training_scenario(session_id)
        
        assert "category" in scenario
        assert "prompt" in scenario
        assert "difficulty" in scenario
        assert scenario["difficulty"] == "beginner"
    
    @pytest.mark.asyncio
    @patch('src.agent.openai')
    @patch('src.utils.helpers.load_config')
    @patch('src.utils.helpers.setup_logging')
    async def test_get_session_status(self, mock_setup_logging, mock_load_config, mock_openai):
        """Test getting session status"""
        mock_load_config.return_value = self.mock_config()
        mock_logger = Mock()
        mock_setup_logging.return_value = mock_logger
        
        agent = WaiterTrainingAgent()
        session_id = await agent.start_training_session("Bob Smith", "advanced")
        
        status = agent.get_session_status(session_id)
        
        assert status is not None
        assert status["waiter_name"] == "Bob Smith"
        assert status["difficulty_level"] == "advanced"
        assert status["current_score"] == 0.0
    
    def test_get_available_categories(self):
        """Test getting available categories"""
        with patch('src.agent.WaiterTrainingAgent._load_training_scenarios') as mock_load:
            mock_load.return_value = {
                "customer_greeting": Mock(),
                "menu_knowledge": Mock()
            }
            
            agent = WaiterTrainingAgent()
            categories = agent.get_available_categories()
            
            assert "customer_greeting" in categories
            assert "menu_knowledge" in categories
            assert len(categories) == 2
    
    def test_get_difficulty_levels(self):
        """Test getting difficulty levels"""
        with patch('src.agent.WaiterTrainingAgent._load_training_scenarios'):
            agent = WaiterTrainingAgent()
            agent.config = self.mock_config()
            
            levels = agent.get_difficulty_levels()
            
            assert "beginner" in levels
            assert "intermediate" in levels
            assert "advanced" in levels


if __name__ == "__main__":
    pytest.main([__file__]) 