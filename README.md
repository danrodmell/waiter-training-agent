# Waiter Training Agent

An AI-powered chatbot agent designed to train restaurant waiters using Mastra.ai technology. This agent provides interactive training scenarios, best practices, and real-time feedback to help waiters improve their service skills.

## Features

- **Interactive Training Scenarios**: Real-world restaurant situations and customer interactions
- **Best Practices Guide**: Comprehensive coverage of service standards and protocols
- **Role-playing Exercises**: Practice customer service scenarios with AI feedback
- **Knowledge Base**: Restaurant operations, menu knowledge, and service etiquette
- **Progress Tracking**: Monitor training progress and identify areas for improvement

## Getting Started

### Prerequisites

- Python 3.8+
- Mastra.ai account
- GitHub account connected to Mastra

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd waiter-training-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Mastra.ai configuration:
```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your Mastra.ai credentials
```

4. Run the agent:
```bash
python main.py
```

## Project Structure

```
waiter-training-agent/
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── waiter_agent.py
│   │   └── training_scenarios.py
│   ├── data/
│   │   ├── training_materials/
│   │   └── knowledge_base/
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── config/
│   └── config.yaml
├── tests/
├── requirements.txt
├── main.py
└── README.md
```

## Training Scenarios

The agent covers various training scenarios including:

- **Customer Greeting**: Proper welcome protocols and first impressions
- **Menu Knowledge**: Understanding dishes, ingredients, and preparation methods
- **Order Taking**: Efficient order processing and special requests
- **Upselling**: Appropriate recommendations and sales techniques
- **Problem Resolution**: Handling complaints and difficult situations
- **Service Recovery**: Turning negative experiences into positive ones

## Configuration

Edit `config/config.yaml` to customize:

- Training difficulty levels
- Scenario categories
- Feedback preferences
- Integration settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in this repository or contact the development team. 