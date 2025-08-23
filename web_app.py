#!/usr/bin/env python3
"""
FastAPI web application for the Waiter Training Agent
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from src.agent import WaiterTrainingAgent
from src.utils.helpers import ensure_directories, validate_config


# Pydantic models for API
class TrainingSessionRequest(BaseModel):
    waiter_name: str
    difficulty_level: str = "beginner"


class WaiterResponse(BaseModel):
    session_id: str
    scenario_category: str
    response: str


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
    
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
    
    async def send_message(self, session_id: str, message: Dict[str, Any]):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)


# Initialize FastAPI app
app = FastAPI(
    title="Waiter Training Agent",
    description="AI-powered chatbot for training restaurant waiters",
    version="1.0.0"
)

# Initialize components
manager = WebSocketManager()
agent: Optional[WaiterTrainingAgent] = None

# Ensure directories exist
ensure_directories({})


@app.on_event("startup")
async def startup_event():
    """Initialize the agent on startup"""
    global agent
    try:
        agent = WaiterTrainingAgent()
        if not validate_config(agent.config):
            print("Warning: Configuration validation failed")
        print("✅ Waiter Training Agent initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")


@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    """Serve the main training interface"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Waiter Training Agent</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .header {
                text-align: center;
                margin-bottom: 40px;
                color: white;
            }
            
            .header h1 {
                font-size: 3rem;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            .header p {
                font-size: 1.2rem;
                opacity: 0.9;
            }
            
            .training-interface {
                background: white;
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }
            
            .session-form {
                display: grid;
                grid-template-columns: 1fr 1fr auto;
                gap: 20px;
                align-items: end;
                margin-bottom: 30px;
            }
            
            .form-group {
                display: flex;
                flex-direction: column;
            }
            
            .form-group label {
                margin-bottom: 8px;
                font-weight: 600;
                color: #555;
            }
            
            .form-group input, .form-group select {
                padding: 12px;
                border: 2px solid #e1e5e9;
                border-radius: 10px;
                font-size: 16px;
                transition: border-color 0.3s;
            }
            
            .form-group input:focus, .form-group select:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
            }
            
            .btn:hover {
                transform: translateY(-2px);
            }
            
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            .training-area {
                display: none;
                margin-top: 30px;
            }
            
            .scenario-display {
                background: #f8f9fa;
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 25px;
                border-left: 5px solid #667eea;
            }
            
            .scenario-category {
                color: #667eea;
                font-weight: 600;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .scenario-prompt {
                font-size: 16px;
                line-height: 1.6;
                color: #333;
            }
            
            .response-form {
                display: grid;
                gap: 20px;
            }
            
            .response-textarea {
                width: 100%;
                min-height: 120px;
                padding: 15px;
                border: 2px solid #e1e5e9;
                border-radius: 10px;
                font-size: 16px;
                font-family: inherit;
                resize: vertical;
            }
            
            .response-textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .feedback-display {
                background: #e8f5e8;
                border-radius: 15px;
                padding: 20px;
                margin-top: 20px;
                border-left: 5px solid #28a745;
                display: none;
            }
            
            .score-display {
                background: #fff3cd;
                border-radius: 15px;
                padding: 20px;
                margin-top: 20px;
                border-left: 5px solid #ffc107;
                text-align: center;
            }
            
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            .stat-card {
                background: white;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .stat-value {
                font-size: 2rem;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 5px;
            }
            
            .stat-label {
                color: #666;
                font-size: 0.9rem;
            }
            
            .hidden {
                display: none;
            }
            
            @media (max-width: 768px) {
                .session-form {
                    grid-template-columns: 1fr;
                }
                
                .header h1 {
                    font-size: 2rem;
                }
                
                .container {
                    padding: 10px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🍽️ Waiter Training Agent</h1>
                <p>AI-powered training for restaurant service excellence</p>
            </div>
            
            <div class="training-interface">
                <div class="session-form">
                    <div class="form-group">
                        <label for="waiterName">Waiter Name</label>
                        <input type="text" id="waiterName" placeholder="Enter waiter name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="difficultyLevel">Difficulty Level</label>
                        <select id="difficultyLevel">
                            <option value="beginner">Beginner</option>
                            <option value="intermediate">Intermediate</option>
                            <option value="advanced">Advanced</option>
                        </select>
                    </div>
                    
                    <button class="btn" onclick="startTraining()">Start Training</button>
                </div>
                
                <div id="trainingArea" class="training-area">
                    <div class="stats">
                        <div class="stat-card">
                            <div class="stat-value" id="currentScore">0</div>
                            <div class="stat-label">Current Score</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="scenariosCompleted">0</div>
                            <div class="stat-label">Scenarios Completed</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="sessionDuration">0</div>
                            <div class="stat-label">Duration (min)</div>
                        </div>
                    </div>
                    
                    <div id="scenarioDisplay" class="scenario-display hidden">
                        <div class="scenario-category" id="scenarioCategory"></div>
                        <div class="scenario-prompt" id="scenarioPrompt"></div>
                    </div>
                    
                    <div id="responseForm" class="response-form hidden">
                        <label for="waiterResponse">Your Response:</label>
                        <textarea 
                            id="waiterResponse" 
                            class="response-textarea" 
                            placeholder="Describe how you would handle this situation..."
                        ></textarea>
                        <button class="btn" onclick="submitResponse()">Submit Response</button>
                    </div>
                    
                    <div id="feedbackDisplay" class="feedback-display">
                        <h4>Feedback:</h4>
                        <div id="feedbackText"></div>
                    </div>
                    
                    <div id="scoreDisplay" class="score-display hidden">
                        <h4>Updated Score</h4>
                        <div id="newScore"></div>
                        <div id="nextScenario"></div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <button class="btn" onclick="endSession()" style="background: #dc3545;">End Training Session</button>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            let currentSessionId = null;
            let sessionStartTime = null;
            
            async function startTraining() {
                const waiterName = document.getElementById('waiterName').value.trim();
                const difficultyLevel = document.getElementById('difficultyLevel').value;
                
                if (!waiterName) {
                    alert('Please enter a waiter name');
                    return;
                }
                
                try {
                    const response = await fetch('/api/start-session', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            waiter_name: waiterName,
                            difficulty_level: difficultyLevel
                        })
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        currentSessionId = data.session_id;
                        sessionStartTime = Date.now();
                        
                        document.getElementById('trainingArea').style.display = 'block';
                        document.getElementById('sessionForm').style.display = 'none';
                        
                        // Get first scenario
                        await getNextScenario();
                        updateStats();
                        
                        // Start timer
                        setInterval(updateStats, 30000); // Update every 30 seconds
                    } else {
                        alert('Failed to start training session');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Error starting training session');
                }
            }
            
            async function getNextScenario() {
                if (!currentSessionId) return;
                
                try {
                    const response = await fetch(`/api/get-scenario/${currentSessionId}`);
                    if (response.ok) {
                        const data = await response.json();
                        
                        document.getElementById('scenarioCategory').textContent = 
                            data.category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                        document.getElementById('scenarioPrompt').textContent = data.prompt;
                        document.getElementById('scenarioDisplay').classList.remove('hidden');
                        document.getElementById('responseForm').classList.remove('hidden');
                        document.getElementById('feedbackDisplay').style.display = 'none';
                        document.getElementById('scoreDisplay').classList.add('hidden');
                    }
                } catch (error) {
                    console.error('Error getting scenario:', error);
                }
            }
            
            async function submitResponse() {
                if (!currentSessionId) return;
                
                const response = document.getElementById('waiterResponse').value.trim();
                if (!response) {
                    alert('Please enter a response');
                    return;
                }
                
                try {
                    const apiResponse = await fetch('/api/submit-response', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            session_id: currentSessionId,
                            scenario_category: document.getElementById('scenarioCategory').textContent.toLowerCase().replace(/\s+/g, '_'),
                            response: response
                        })
                    });
                    
                    if (apiResponse.ok) {
                        const data = await apiResponse.json();
                        
                        // Show feedback
                        document.getElementById('feedbackText').textContent = data.feedback;
                        document.getElementById('feedbackDisplay').style.display = 'block';
                        
                        // Show score update
                        document.getElementById('newScore').textContent = `Score: ${data.score}`;
                        document.getElementById('nextScenario').textContent = `Next: ${data.next_scenario}`;
                        document.getElementById('scoreDisplay').classList.remove('hidden');
                        
                        // Update stats
                        updateStats();
                        
                        // Clear response
                        document.getElementById('waiterResponse').value = '';
                        
                        // Hide response form temporarily
                        document.getElementById('responseForm').classList.add('hidden');
                        
                        // Show next scenario after a delay
                        setTimeout(() => {
                            getNextScenario();
                        }, 3000);
                    }
                } catch (error) {
                    console.error('Error submitting response:', error);
                    alert('Error submitting response');
                }
            }
            
            async function endSession() {
                if (!currentSessionId) return;
                
                try {
                    const response = await fetch(`/api/end-session/${currentSessionId}`);
                    if (response.ok) {
                        const data = await response.json();
                        alert(`Training session ended!\\nFinal Score: ${data.final_score}\\nScenarios Completed: ${data.scenarios_completed.length}\\nDuration: ${data.duration_minutes} minutes`);
                        
                        // Reset interface
                        resetInterface();
                    }
                } catch (error) {
                    console.error('Error ending session:', error);
                }
            }
            
            function updateStats() {
                if (!currentSessionId || !sessionStartTime) return;
                
                const duration = Math.round((Date.now() - sessionStartTime) / 60000);
                document.getElementById('sessionDuration').textContent = duration;
                
                // Update other stats from session status
                fetch(`/api/session-status/${currentSessionId}`)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('currentScore').textContent = Math.round(data.current_score);
                        document.getElementById('scenariosCompleted').textContent = data.scenarios_completed.length;
                    })
                    .catch(error => console.error('Error updating stats:', error));
            }
            
            function resetInterface() {
                currentSessionId = null;
                sessionStartTime = null;
                
                document.getElementById('trainingArea').style.display = 'none';
                document.getElementById('sessionForm').style.display = 'grid';
                document.getElementById('waiterName').value = '';
                document.getElementById('difficultyLevel').value = 'beginner';
                
                // Hide all training elements
                document.getElementById('scenarioDisplay').classList.add('hidden');
                document.getElementById('responseForm').classList.add('hidden');
                document.getElementById('feedbackDisplay').style.display = 'none';
                document.getElementById('scoreDisplay').classList.add('hidden');
            }
        </script>
    </body>
    </html>
    """


# API endpoints
@app.post("/api/start-session")
async def start_session(request: TrainingSessionRequest):
    """Start a new training session"""
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:
        session_id = await agent.start_training_session(
            request.waiter_name, 
            request.difficulty_level
        )
        return {"session_id": session_id, "status": "started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/get-scenario/{session_id}")
async def get_scenario(session_id: str, category: str = None):
    """Get a training scenario for the session"""
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:
        scenario = await agent.get_training_scenario(session_id, category)
        return scenario
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/submit-response")
async def submit_response(request: WaiterResponse):
    """Submit a waiter's response to a scenario"""
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:
        result = await agent.process_waiter_response(
            request.session_id,
            request.scenario_category,
            request.response
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/session-status/{session_id}")
async def get_session_status(session_id: str):
    """Get current status of a training session"""
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    status = agent.get_session_status(session_id)
    if not status:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return status


@app.post("/api/end-session/{session_id}")
async def end_session(session_id: str):
    """End a training session"""
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    try:
        summary = await agent.end_training_session(session_id)
        return summary
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/categories")
async def get_categories():
    """Get available training categories"""
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    return {"categories": agent.get_available_categories()}


@app.get("/api/difficulty-levels")
async def get_difficulty_levels():
    """Get available difficulty levels"""
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")
    
    return {"difficulty_levels": agent.get_difficulty_levels()}


if __name__ == "__main__":
    uvicorn.run(
        "web_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 