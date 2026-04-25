# CarbonIQ - Carbon Footprint Calculator

A modern web application for calculating and tracking carbon footprints using AI-powered predictions.

## Features

- 🌱 **AI-Powered Carbon Calculator** - Uses machine learning to predict carbon footprints
- 🤖 **AI Chatbot** - Get personalized sustainability advice
- 📊 **Dashboard & Analytics** - Track your progress over time
- 🏆 **Leaderboard** - Compete with friends for the greenest lifestyle
- 📄 **PDF Reports** - Generate detailed carbon footprint reports
- 🎯 **Gamification** - Earn green points for sustainable choices

## Local Development

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (for full deployment)
- Ollama (for AI features)

### Setup

1. **Clone and setup virtual environment:**
   ```bash
   cd CarbonIQ
   uv venv
   uv pip install -r requirements.txt
   ```

2. **Install Ollama and pull the model:**
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull llama3.2
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   ```
   http://localhost:5000
   ```

## Docker Deployment

### Quick Start with Docker Compose

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   ```
   http://localhost:5000
   ```

### Manual Docker Build

```bash
# Build the image
docker build -t carboniq .

# Run the container
docker run -p 5000:5000 carboniq
```

## Cloud Deployment Options

### 1. Railway (Recommended)

1. **Connect your GitHub repository**
2. **Add environment variables:**
   - `FLASK_ENV=production`
   - `PORT=5000`
3. **Deploy automatically**

### 2. Render

1. **Create a new Web Service**
2. **Connect your repository**
3. **Set build command:** `pip install -r requirements.txt`
4. **Set start command:** `python app.py`
5. **Add environment variables**

### 3. Heroku

1. **Create a new app**
2. **Set buildpacks:**
   - `heroku/python`
3. **Deploy via Git or GitHub integration**
4. **Set environment variables in Heroku dashboard**

### 4. DigitalOcean App Platform

1. **Create App Spec:**
   ```yaml
   name: carboniq
   services:
   - name: web
     source_dir: /
     github:
       repo: your-username/CarbonIQ
       branch: main
     run_command: python app.py
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: FLASK_ENV
       value: production
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `production` |
| `PORT` | Port to run on | `5000` |
| `OLLAMA_URL` | Ollama API endpoint | `http://localhost:11434/api/generate` |

## Project Structure

```
CarbonIQ/
├── app.py                 # Main Flask application
├── ai_engine.py          # AI prediction and chatbot logic
├── firebase_config.py    # Data persistence (JSON-based)
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker container configuration
├── docker-compose.yml   # Multi-container setup
├── .env                 # Environment variables
├── data/                # Application data storage
├── static/              # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── reports/         # Generated PDF reports
└── templates/           # HTML templates
    ├── index.html
    ├── calculator.html
    ├── dashboard.html
    ├── chatbot.html
    └── report.html
```

## API Endpoints

- `GET /` - Home page
- `GET /calculator` - Carbon calculator
- `GET /dashboard` - User dashboard
- `GET /chatbot` - AI chatbot interface
- `GET /report` - Report generation

### API Routes

- `POST /api/register` - User registration
- `POST /api/calculate` - Carbon footprint calculation
- `POST /api/chat` - AI chatbot interaction
- `GET /api/history` - User calculation history
- `GET /api/leaderboard` - Global leaderboard
- `POST /api/generate-report` - PDF report generation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue on GitHub or contact the development team.