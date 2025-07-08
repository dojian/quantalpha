# QuantAlpha - AI Portfolio Management

AI-powered portfolio management with real-time market analysis using Python analytics and Groq's Llama models.

## 👥 Our Team

| <img src="https://github.com/haris-mughal.png" width="100"/> <br> Haris Mughal | <img src="https://github.com/dojian.png" width="100"/> <br> An Jian | <img src="https://github.com/Hamzacancode.png" width="100"/> <br> Hamza Imran | <img src="https://github.com/Talhaasif7.png" width="100"/> <br> Talha Asif | <img src="https://github.com/arslansaeed.png" width="100"/> <br> Arslan Saeed | <img src="https://github.com/jps245.png" width="100"/> <br> Justin Sterling |
|---|---|---|---|---|---|


## 🚀 Features

- **Python-Powered Analytics**: Advanced portfolio calculations using NumPy and Pandas
- **AI Portfolio Manager**: Groq-powered Llama model for intelligent investment advice
- **Real-time Analysis**: Live portfolio monitoring and rebalancing recommendations
- **Risk Management**: Comprehensive risk profiling and scenario analysis
- **Modern UI**: Next.js dashboard with real-time AI chat

## 🛠️ Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Poetry (Python dependency management)

### Installation

1. **Install Poetry** (if not already installed):
   \`\`\`bash
   curl -sSL https://install.python-poetry.org | python3 -
   \`\`\`

2. **Install Python dependencies**:
   \`\`\`bash
   poetry install
   \`\`\`

3. **Install Node.js dependencies**:
   \`\`\`bash
   npm install
   \`\`\`

4. **Environment Setup**:
   \`\`\`bash
   cp .env.example .env
   # Add your Groq API key to .env
   \`\`\`

5. **Activate Poetry environment**:
   \`\`\`bash
   poetry shell
   \`\`\`

### Configuration

Create a `.env` file with your API keys:

\`\`\`env
GROQ_API_KEY=your_groq_api_key_here
\`\`\`

Get your Groq API key from: https://console.groq.com

## 🧪 Testing

### Test Groq Connection
\`\`\`bash
poetry run python scripts/test_groq_connection.py
\`\`\`

### Run Portfolio Analysis
\`\`\`bash
poetry run python scripts/portfolio_manager.py
\`\`\`

### Test AI Advisor
\`\`\`bash
poetry run python scripts/ai_portfolio_advisor.py
\`\`\`

## 🚀 Running the Application

### Development Mode
\`\`\`bash
# Start Next.js development server
npm run dev

# In another terminal, ensure Poetry environment is active
poetry shell
\`\`\`

### Production Mode
\`\`\`bash
npm run build
npm start
\`\`\`

## 📊 Python Scripts

- `portfolio_manager.py` - Core portfolio calculations and management
- `ai_portfolio_advisor.py` - Groq-powered AI investment advisor
- `scenario_analysis.py` - Monte Carlo simulations and scenario modeling
- `risk_profiler.py` - Risk assessment and profiling tools

## 🔧 Development

### Code Formatting
\`\`\`bash
poetry run black scripts/
\`\`\`

### Type Checking
\`\`\`bash
poetry run mypy scripts/
\`\`\`

### Testing
\`\`\`bash
poetry run pytest
\`\`\`

## 📈 Usage

1. **Portfolio Analysis**: Get comprehensive portfolio metrics
2. **AI Chat**: Interactive investment advice from AI advisor
3. **Risk Assessment**: Complete risk profiling questionnaire
4. **Scenario Analysis**: Monte Carlo simulations and stress testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and formatting
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.
