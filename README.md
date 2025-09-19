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
- **Intelligent Conversations**: Context-aware mental health discussions
- **Mood Analysis**: Advanced sentiment analysis using VADER
- **Personalized Insights**: Tailored recommendations based on patterns
- **Crisis Detection**: Automated identification of concerning patterns

### 📊 **Comprehensive Tracking**
- **Mood Journaling**: Daily mood tracking with AI-generated prompts
- **Wellness Analytics**: Visual insights into mental health patterns
- **Progress Monitoring**: Track improvements over time
- **Goal Setting**: Personalized wellness objectives

### 🆘 **Crisis Support System**
- **24/7 Availability**: Always-on crisis detection and support
- **Emergency Resources**: Immediate access to helplines and resources
- **Safety Planning**: Collaborative safety plan development
- **Professional Referrals**: Seamless connection to mental health professionals

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Redux Toolkit** for state management
- **Tailwind CSS** for responsive design
- **Heroicons** for consistent iconography
- **Axios** for API communication

### Backend
- **FastAPI** with Python 3.11+
- **SQLAlchemy** ORM with PostgreSQL
- **JWT Authentication** with python-jose
- **Uvicorn** ASGI server
- **Alembic** for database migrations

### AI & Machine Learning
- **Hugging Face Transformers** for NLP
- **PyTorch** for model inference
- **VADER Sentiment Analysis** for mood detection
- **Custom fine-tuned models** for mental health conversations

## 📁 Project Structure

```
mindspark-ai/
├── 📂 frontend/                 # React TypeScript Frontend
│   ├── 📂 public/               # Static assets
│   ├── 📂 src/
│   │   ├── 📂 components/       # Reusable UI components
│   │   ├── 📂 pages/           # Page components
│   │   ├── 📂 store/           # Redux store & slices
│   │   ├── 📂 hooks/           # Custom React hooks
│   │   ├── 📂 utils/           # Utility functions
│   │   └── 📂 types/           # TypeScript type definitions
│   ├── 📄 package.json
│   └── 📄 tailwind.config.js
├── 📂 backend/                  # FastAPI Python Backend
│   ├── 📂 app/
│   │   ├── 📂 routers/         # API route handlers
│   │   ├── 📂 models/          # SQLAlchemy models
│   │   ├── 📂 schemas/         # Pydantic schemas
│   │   ├── 📂 services/        # Business logic
│   │   ├── 📄 main.py          # FastAPI app entry point
│   │   └── 📄 database.py      # Database configuration
│   ├── 📂 venv/                # Python virtual environment
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
- **PostgreSQL** 13+ (or SQLite for development)
- **Git** for version control

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

5. **Initialize database**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
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
DATABASE_URL=postgresql://username:password@localhost/mindspark_db
# Or for SQLite development:
# DATABASE_URL=sqlite:///./mindspark.db

# Security
SECRET_KEY=your-super-secret-jwt-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Configuration
HUGGINGFACE_API_KEY=your-huggingface-api-key
MODEL_PATH=./models/mental-health-model

# CORS Settings
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

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

- **Project Maintainer**: [GitHub Profile](https://github.com/anujkdotexe)
- **Issues**: [GitHub Issues](https://github.com/anujkdotexe/Gen-AI-Mental-Health-Wellnes-For-Youth/issues)
- **Discussions**: [GitHub Discussions](https://github.com/anujkdotexe/Gen-AI-Mental-Health-Wellnes-For-Youth/discussions)

---

<div align="center">
  <p><strong>🧠 MindSpark AI - Empowering Youth Mental Wellness Through Technology 🧠</strong></p>
  <p>Made with ❤️ for mental health awareness and youth empowerment</p>
</div>