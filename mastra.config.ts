import { MastraConfig } from '@mastra/core';

export const mastraConfig: MastraConfig = {
  // Project metadata
  project: {
    name: 'Waiter Training Agent',
    version: '1.0.0',
    description: 'AI-powered chatbot for training restaurant waiters using Mastra.ai',
    author: 'Daniel Melendez',
    repository: 'https://github.com/danrodmell/waiter-training-agent'
  },

  // Agent configuration
  agent: {
    type: 'training',
    model: 'gpt-4',
    capabilities: [
      'interactive_training',
      'scenario_based_learning',
      'real_time_feedback',
      'progress_tracking',
      'adaptive_difficulty'
    ]
  },

  // Training scenarios
  training: {
    categories: [
      'customer_greeting',
      'menu_knowledge',
      'order_taking',
      'upselling',
      'problem_resolution',
      'service_recovery'
    ],
    difficultyLevels: [
      'beginner',
      'intermediate',
      'advanced'
    ],
    feedbackTypes: [
      'immediate',
      'detailed',
      'constructive'
    ]
  },

  // Runtime configuration
  runtime: {
    language: 'python',
    version: '3.8+',
    entryPoint: 'main.py',
    webInterface: 'web_app.py',
    requirements: 'requirements.txt'
  },

  // Environment variables
  environment: {
    required: [
      'OPENAI_API_KEY',
      'MASTRA_API_KEY',
      'MASTRA_PROJECT_ID'
    ],
    optional: [
      'DEBUG',
      'LOG_LEVEL',
      'HOST',
      'PORT'
    ]
  },

  // Deployment settings
  deployment: {
    platform: 'mastra.ai',
    autoScale: true,
    healthCheck: '/health',
    monitoring: true
  }
};

export default mastraConfig;
