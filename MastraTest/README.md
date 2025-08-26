# Waiter Training Agent - Mastra Project

This is the Mastra.ai configuration for the Waiter Training Agent, an AI-powered chatbot designed to train restaurant waiters.

## Project Structure

```
MastraTest/
├── src/
│   └── mastra/
│       └── index.ts          # Main Mastra agent configuration
├── mastra.config.ts          # Mastra project configuration
├── package.json              # Node.js dependencies and scripts
├── tsconfig.json            # TypeScript configuration
└── README.md                # This file
```

## Mastra.ai Configuration

### Agent Type
- **Type**: Training Agent
- **Model**: GPT-4
- **Capabilities**: Interactive training, scenario-based learning, real-time feedback

### Training Categories
1. Customer Greeting
2. Menu Knowledge
3. Order Taking
4. Upselling
5. Problem Resolution
6. Service Recovery

### Difficulty Levels
- Beginner
- Intermediate
- Advanced

## Deployment

### Prerequisites
- Mastra.ai account
- OpenAI API key
- GitHub repository access

### Steps
1. Import this repository to Mastra.ai
2. Set environment variables:
   - `OPENAI_API_KEY`
   - `MASTRA_API_KEY`
   - `MASTRA_PROJECT_ID`
3. Deploy the agent
4. Configure training scenarios

## Development

### Build
```bash
npm install
npm run build
```

### Run
```bash
npm start
```

## Integration

This Mastra project integrates with the main Python application located in the parent directory. The Python application handles the actual training logic, while this Mastra configuration provides the deployment and integration layer for Mastra.ai.

## Support

For issues or questions, please refer to the main project repository or contact the development team.