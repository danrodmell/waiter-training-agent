# Deployment Guide for Waiter Training Agent

This guide will help you deploy the Waiter Training Agent to Mastra.ai and set up the necessary infrastructure.

## Prerequisites

- GitHub account connected to Mastra.ai
- Python 3.8+ installed
- Git installed
- OpenAI API key (for AI feedback generation)

## Step 1: Repository Setup

The repository has been created with the following structure:

```
waiter-training-agent/
├── src/
│   ├── agent/           # Core AI agent logic
│   ├── data/            # Training materials and knowledge base
│   └── utils/           # Helper utilities
├── config/              # Configuration files
├── tests/               # Test suite
├── main.py              # CLI application
├── web_app.py           # FastAPI web interface
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup
└── README.md           # Project documentation
```

## Step 2: Configuration

1. Copy the example configuration:
   ```bash
   cp config/config.example.yaml config/config.yaml
   ```

2. Edit `config/config.yaml` with your settings:
   - Set your OpenAI API key
   - Configure Mastra.ai integration settings
   - Adjust training parameters as needed

3. Set environment variables:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"
   export MASTRA_API_KEY="your_mastra_api_key_here"
   export MASTRA_PROJECT_ID="your_mastra_project_id_here"
   ```

## Step 3: Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the CLI version:
   ```bash
   python main.py
   ```

4. Run the web interface:
   ```bash
   python web_app.py
   ```

5. Run tests:
   ```bash
   pytest tests/
   ```

## Step 4: Deploy to Mastra.ai

### Option 1: Direct GitHub Integration

1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit: Waiter Training Agent"
   git push origin main
   ```

2. In Mastra.ai:
   - Go to your project dashboard
   - Click "Import from GitHub"
   - Select the `waiter-training-agent` repository
   - Configure the deployment settings

### Option 2: Manual Deployment

1. Create a new project in Mastra.ai
2. Upload the project files
3. Configure the runtime environment:
   - Python 3.8+
   - Install dependencies from `requirements.txt`
   - Set environment variables

## Step 5: Mastra.ai Configuration

### Agent Configuration

In your Mastra.ai project, configure:

1. **Model Settings**:
   - Use GPT-4 or GPT-3.5-turbo
   - Set appropriate temperature and token limits
   - Configure response formatting

2. **Training Scenarios**:
   - Import the predefined scenarios from `src/agent/training_scenarios.py`
   - Customize scenarios for your restaurant's specific needs
   - Add industry-specific knowledge

3. **Integration Settings**:
   - Configure webhook endpoints if needed
   - Set up monitoring and logging
   - Configure user authentication

### Customization

1. **Restaurant-Specific Content**:
   - Modify training scenarios to match your menu
   - Add your restaurant's policies and procedures
   - Include specific customer service standards

2. **Branding**:
   - Customize the agent's personality
   - Add your restaurant's voice and tone
   - Include company-specific examples

## Step 6: Testing and Validation

1. **Test Training Scenarios**:
   - Run through each difficulty level
   - Verify feedback quality and relevance
   - Test edge cases and error handling

2. **Performance Testing**:
   - Load test with multiple concurrent users
   - Monitor response times
   - Check resource usage

3. **User Acceptance Testing**:
   - Have actual waiters test the system
   - Gather feedback on scenario relevance
   - Adjust difficulty levels as needed

## Step 7: Production Deployment

1. **Environment Setup**:
   - Production API keys
   - Monitoring and alerting
   - Backup and recovery procedures

2. **User Training**:
   - Train managers on system administration
   - Provide user guides for waiters
   - Set up support procedures

3. **Monitoring**:
   - Track training completion rates
   - Monitor user satisfaction scores
   - Analyze common training needs

## Step 8: Maintenance and Updates

1. **Regular Updates**:
   - Update training scenarios based on feedback
   - Refresh AI models and prompts
   - Add new training categories as needed

2. **Performance Optimization**:
   - Monitor and optimize response times
   - Update training materials
   - Improve scenario relevance

## Troubleshooting

### Common Issues

1. **Configuration Errors**:
   - Verify all required environment variables are set
   - Check configuration file syntax
   - Ensure API keys are valid

2. **Performance Issues**:
   - Monitor API rate limits
   - Check network connectivity
   - Verify resource allocation

3. **Training Quality**:
   - Review and refine prompts
   - Adjust difficulty levels
   - Update scenario content

### Support

- Check the project's GitHub issues
- Review Mastra.ai documentation
- Contact the development team

## Next Steps

After successful deployment:

1. **Expand Training Content**:
   - Add more specialized scenarios
   - Include video and multimedia content
   - Create certification programs

2. **Integration Opportunities**:
   - Connect with HR systems
   - Integrate with restaurant management software
   - Add mobile app support

3. **Analytics and Insights**:
   - Track training effectiveness
   - Identify common training gaps
   - Measure ROI and impact

## Resources

- [Mastra.ai Documentation](https://docs.mastra.ai)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Project GitHub Repository](https://github.com/yourusername/waiter-training-agent) 