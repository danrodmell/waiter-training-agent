import { MastraAgent } from '@mastra/core';

// Waiter Training Agent Configuration
export const waiterTrainingAgent = new MastraAgent({
  name: 'Waiter Training Agent',
  version: '1.0.0',
  description: 'AI-powered chatbot for training restaurant waiters',
  
  // Agent capabilities
  capabilities: {
    training: true,
    feedback: true,
    scenarios: true,
    progress_tracking: true
  },
  
  // Training categories
  trainingCategories: [
    'customer_greeting',
    'menu_knowledge', 
    'order_taking',
    'upselling',
    'problem_resolution',
    'service_recovery'
  ],
  
  // Difficulty levels
  difficultyLevels: [
    'beginner',
    'intermediate',
    'advanced'
  ],
  
  // Entry points
  entryPoints: {
    cli: 'main.py',
    web: 'web_app.py',
    api: 'web_app.py'
  },
  
  // Dependencies
  dependencies: {
    python: '>=3.8',
    packages: 'requirements.txt'
  },
  
  // Environment variables
  environmentVariables: [
    'OPENAI_API_KEY',
    'MASTRA_API_KEY',
    'MASTRA_PROJECT_ID'
  ]
});

// Export the agent instance
export default waiterTrainingAgent;
