# 🧠 MindSpark AI - Generative AI Mental Health & Wellness Platform for Youth

<div align="center">
  <img src="https://img.shields.io/badge/React-18.x-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React 18.x" />
  <img src="https://img.shields.io/badge/FastAPI-0.104.1-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/TailwindCSS-3.x-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="Tailwind CSS" />
</div>

## 🌟 Overview

**MindSpark AI** is a privacy-first, intelligent mental wellness companion designed specifically for youth aged 15-25. Our platform bridges the critical gap between immediate mental health needs and professional care through empathetic AI conversations, comprehensive mood tracking, and 24/7 crisis support—all while maintaining complete data privacy and user autonomy.

### 🎯 Mission Statement
Empower young people to take control of their mental wellness journey through accessible, evidence-based AI technology that provides immediate support, insights, and resources while respecting privacy and promoting professional care when needed.

## ✨ Key Features

### 🔐 **Privacy-First Design**
- **Anonymous Authentication**: No personal information required
- **Local Data Storage**: All sensitive data encrypted locally
- **Zero Data Mining**: Your conversations remain private
- **JWT Security**: Industry-standard token-based authentication

### 🤖 **AI-Powered Wellness Support**
- **Intelligent Conversations**: Context-aware mental health discussions with 7 personality modes
- **Emotional Intelligence Engine**: Advanced sentiment analysis with 15 emotional states
- **Personalized Insights**: Tailored recommendations based on patterns
- **Crisis Detection**: Automated identification of concerning patterns with multi-level severity analysis

### 📊 **Comprehensive Tracking & Analytics**
- **Mood Journaling**: Daily mood tracking with AI-generated prompts
- **Wellness Analytics**: Visual insights into mental health patterns with optimized scoring
- **Progress Monitoring**: Track improvements over time with 30% focus on AI chat effectiveness
- **Goal Setting**: Personalized wellness objectives

### 🆘 **Crisis Support System**
- **24/7 Availability**: Always-on crisis detection and support
- **Emergency Resources**: Immediate access to helplines and resources
- **Safety Planning**: Collaborative safety plan development
- **Professional Referrals**: Seamless connection to mental health professionals

### 📝 **Therapeutic Journaling**
- **Privacy-First Journaling**: Three privacy levels with local encryption
- **AI-Generated Prompts**: Evidence-based therapeutic writing prompts
- **Sentiment Analysis**: Track emotional progression through journal entries
- **Cross-Platform Integration**: Seamless connection between chat and journal insights

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Redux Toolkit** for state management
- **Tailwind CSS** for responsive design
- **Heroicons** for consistent iconography
- **Axios** for API communication

### Backend
- **FastAPI** with Python 3.11+
- **SQLAlchemy** ORM with SQLite/PostgreSQL
- **JWT Authentication** with python-jose
- **Uvicorn** ASGI server
- **Alembic** for database migrations

### AI & Machine Learning
- **Google Gemini API** for conversational AI
- **Intelligent Conversation Engine** with dynamic personality blending
- **Emotional Intelligence Engine** with real-time calibration
- **VADER Sentiment Analysis** for mood detection
- **Optimized Wellness Calculator** with 40+ therapeutic metrics

## 📁 Project Structure

```
mindspark-ai/
├── 📂 frontend/                 # React TypeScript Frontend
│   ├── 📂 public/               # Static assets
│   ├── 📂 src/
│   │   ├── 📂 components/       # Reusable UI components
│   │   │   ├── AIChat.tsx       # AI conversation interface
│   │   │   ├── Dashboard.tsx    # Analytics dashboard
│   │   │   ├── Journal.tsx      # Journaling interface
│   │   │   ├── MoodTracker.tsx  # Mood tracking
│   │   │   └── CrisisSupport.tsx # Crisis support
│   │   ├── 📂 store/           # Redux store & slices
│   │   ├── 📂 hooks/           # Custom React hooks
│   │   └── 📄 App.tsx          # Main app component
│   ├── 📄 package.json
│   └── 📄 tailwind.config.js
├── 📂 backend/                  # FastAPI Python Backend
│   ├── 📂 app/
│   │   ├── 📂 routers/         # API route handlers
│   │   │   ├── auth.py         # Authentication
│   │   │   ├── conversation.py # AI conversations
│   │   │   ├── mood.py         # Mood tracking
│   │   │   ├── journal.py      # Journaling
│   │   │   └── crisis.py       # Crisis support
│   │   ├── 📂 models/          # SQLAlchemy models
│   │   ├── 📂 schemas/         # Pydantic schemas
│   │   ├── 📂 services/        # Business logic
│   │   │   ├── ai_service.py              # Main AI orchestration
│   │   │   ├── intelligent_conversation_engine.py  # Conversation AI
│   │   │   ├── emotional_intelligence_engine.py    # Emotional analysis
│   │   │   ├── optimized_wellness_calculator.py    # Wellness scoring
│   │   │   ├── gemini_service.py          # Google Gemini integration
│   │   │   ├── crisis_detection.py        # Crisis detection
│   │   │   └── journal_analysis_service.py # Journal analysis
│   │   ├── 📄 main.py          # FastAPI app entry point
│   │   └── 📄 database.py      # Database configuration
│   ├── 📄 requirements.txt     # Python dependencies
│   └── 📄 .env.example         # Environment variables template
├── 📄 README.md
├── 📄 .gitignore
└── 📄 LICENSE
```

## 🚀 Quick Start Guide

### Prerequisites
- **Node.js** 18.x or higher
- **Python** 3.11 or higher
- **Git** for version control
- **Google Gemini API Key** for AI conversations

### 🔧 Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start the development server**
   ```bash
   python start_server.py
   ```

   Server will be available at: `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### ⚛️ Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

   Application will be available at: `http://localhost:3000`

### 🔧 Development Scripts

**Frontend Scripts (package.json)**
- `npm start` - Runs the development server
- `npm test` - Launches test runner  
- `npm run build` - Builds for production
- `npm run eject` - Ejects from Create React App (one-way operation)

### 🧪 Running Tests

**Backend Tests**
```bash
cd backend
pytest
```

**Frontend Tests**
```bash
cd frontend
npm test
```

## 🔐 Environment Configuration

### Backend Environment Variables (.env)
```env
# Database Configuration
DATABASE_URL=sqlite:///./mindspark.db

# Security
SECRET_KEY=your-super-secret-jwt-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Configuration
GEMINI_API_KEY=your-google-gemini-api-key-here

# CORS Settings
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

## 🧠 AI System Architecture

### Intelligent Conversation Engine
- **7 Personality Modes**: Empathetic, Analytical, Encouraging, Humorous, Wise, Practical, Calming
- **Dynamic Blending**: Adaptive personality mixing based on user needs
- **Context Awareness**: Maintains conversation history and emotional context
- **Conversation Intelligence**: Advanced pattern recognition and response optimization

### Emotional Intelligence Engine  
- **15 Emotional States**: Comprehensive emotional spectrum analysis
- **8 Response Tones**: Adaptive response styling based on emotional needs
- **Real-Time Calibration**: Continuous emotional state monitoring
- **Cross-Session Memory**: Emotional context retention across conversations

### Optimized Wellness Calculator
- **Enhanced AI Chat Focus**: 30% weight on therapeutic relationship quality
- **40+ Metrics**: Detailed therapeutic effectiveness measurement
- **Age-Based Adjustments**: Youth-optimized scoring (15-17, 18-21, 22-25)
- **Comprehensive Analysis**: Risk factors, strengths, and personalized recommendations

## 📊 API Documentation

The backend provides a comprehensive REST API with the following main endpoints:

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/anonymous` - Anonymous user creation
- `GET /api/auth/me` - Get current user

### Mood Tracking
- `GET /api/mood/` - Get mood entries
- `POST /api/mood/` - Create mood entry
- `PUT /api/mood/{id}` - Update mood entry

### AI Conversations
- `GET /api/conversation/list` - Get conversations
- `POST /api/conversation/start` - Start new conversation
- `POST /api/conversation/{id}/message` - Send message

### Journal
- `GET /api/journal/` - Get journal entries
- `POST /api/journal/` - Create journal entry
- `GET /api/journal/prompts` - Get AI-generated prompts

### Crisis Support
- `POST /api/crisis/assess` - Crisis risk assessment
- `GET /api/crisis/resources` - Get crisis resources
- `POST /api/crisis/safety-plan` - Create safety plan

Full API documentation is available at `/docs` when running the backend server.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Resources

### Crisis Resources
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

### Mental Health Resources
- **National Alliance on Mental Illness (NAMI)**: https://www.nami.org/
- **Mental Health America**: https://www.mhanational.org/
- **Youth Mental Health Resources**: https://www.nimh.nih.gov/health/topics/child-and-adolescent-mental-health

## 📞 Contact

- **Project Repository**: [GitHub Repository](https://github.com/mindspark-ai)
- **Issues**: [GitHub Issues](https://github.com/mindspark-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mindspark-ai/discussions)

---

<div align="center">
  <p><strong>🧠 MindSpark AI - Empowering Youth Mental Wellness Through Technology 🧠</strong></p>
  <p>Made with ❤️ for mental health awareness and youth empowerment</p>
  <p>🎯 Enhanced with AI Chat Therapeutic Effectiveness & Comprehensive Wellness Analytics</p>
</div>