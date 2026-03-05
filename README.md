# 📋 Policy Management AI

An intelligent, AI-powered policy management system built with FastAPI that enables organizations to upload, store, and query their policy documents using advanced Retrieval-Augmented Generation (RAG) technology.

## 🎯 Overview

Policy Management AI is a full-stack application that combines document management with generative AI to provide intelligent policy search and Q&A capabilities. Users can upload PDF policy documents, which are automatically processed, indexed, and made queryable through a conversational AI interface powered by Cohere's language models.

### Key Features

- 🔐 **Secure Authentication**: User registration and login with JWT-based authorization
- 📄 **Document Management**: Upload, store, and manage policy PDF documents
- 🔍 **Intelligent Search**: RAG-powered search using vector embeddings for semantic understanding
- 💬 **AI Chat Interface**: Ask questions about your policies and get AI-generated responses backed by actual document content
- 📊 **Session Management**: Track chat conversations and maintain context across messages
- 🛡️ **Role-Based Access Control**: Admin-only document uploads with secure user authentication
- ☁️ **Cloud Storage**: Documents stored in Supabase with PostgreSQL vector database support

## 🏗️ Architecture

### Technology Stack

**Backend Framework**
- FastAPI - Modern, fast web framework for building APIs
- Uvicorn - ASGI server for running the FastAPI application

**Database & Storage**
- PostgreSQL - Primary relational database with Supabase hosting
- pgvector - PostgreSQL extension for vector similarity search
- Supabase - Cloud storage for PDF files and managed PostgreSQL

**AI & Machine Learning**
- Cohere API - LLM for text generation and embeddings
  - Generation Model: `command-r-08-2024`
  - Embedding Model: `embed-v4.0`

**Authentication & Security**
- PyJWT - JWT token generation and verification
- Passlib + Bcrypt - Password hashing and verification
- OAuth2 - Token-based authentication flow

**Document Processing**
- PyMuPDF (fitz) - PDF text extraction

**Data Validation**
- Pydantic - Data validation and settings management

### Project Structure

```
Policy-Management/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── alembic/                  # Database migrations
│   └── env.py
│
└── app/                      # Main application package
    ├── __init__.py
    ├── main.py              # FastAPI app initialization
    │
    ├── api/                 # API layer
    │   ├── dependencies.py   # Shared dependencies (auth, DB)
    │   └── routers/         # API route handlers
    │       ├── auth.py      # Authentication endpoints
    │       ├── chat.py      # Chat/RAG endpoints
    │       └── document.py  # Document management endpoints
    │
    ├── core/                # Core application logic
    │   ├── config.py        # Settings and environment variables
    │   ├── auth.py          # Authentication logic
    │   └── security.py      # Security utilities (password hashing, JWT)
    │
    ├── db/                  # Database configuration
    │   ├── base.py          # SQLAlchemy declarative base
    │   └── session.py       # Database session management
    │
    ├── models/              # SQLAlchemy ORM models
    │   ├── user.py          # User model
    │   ├── document.py      # Document model
    │   ├── chunk.py         # Document chunk model
    │   ├── chat.py          # Chat session model
    │   └── message.py       # Chat message model
    │
    ├── schemas/             # Pydantic request/response schemas
    │   ├── user.py
    │   ├── document.py
    │   └── chat.py
    │
    ├── repositories/        # Data access layer
    │   ├── user.py
    │   ├── document.py
    │   ├── chunk.py
    │   ├── chat.py
    │   └── message.py
    │
    ├── services/            # Business logic layer
    │   ├── auth.py          # Authentication services
    │   ├── document.py      # Document storage and processing
    │   ├── chunk.py         # Document chunking logic
    │   ├── chat.py          # Chat and RAG logic
    │   ├── llm.py           # LLM integration (Cohere)
    │   └── retrieval.py     # Vector search and retrieval
    │
    └── client/              # External service clients
        └── supabase.py      # Supabase client initialization
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL database (via Supabase or local)
- Cohere API key
- Supabase account

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Policy-management
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # Supabase Configuration
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   SUPABASE_DB_URL=postgresql://user:password@host:5432/database
   
   # LLM Configuration (Cohere)
   COHERE_API_KEY=your_cohere_api_key
   
   # Security
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # Optional: Override default models
   LLM_MODEL=command-r-08-2024
   EMB_MODEL=embed-v4.0
   ```

5. **Set up the database**
   ```bash
   # Run migrations (if using Alembic)
   alembic upgrade head
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`
   
   API documentation (Swagger UI): `http://localhost:8000/docs`

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```
POST /auth/register
```
Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "User Name"
}
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "User Name",
  "role": "user"
}
```

#### Login
```
POST /auth/login
```
Authenticate and receive a JWT token.

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer",
  "role": "user"
}
```

#### Get Current User
```
GET /auth/me
```
Retrieve authenticated user information.

**Headers:**
```
Authorization: Bearer <access_token>
```

---

### Document Management Endpoints

#### Upload Document
```
POST /documents/upload
```
Upload a PDF policy document (Admin only).

**Request:**
- Multipart form data with file field
- Requires authentication

**Response:**
```json
{
  "id": "document_uuid",
  "filename": "policy.pdf",
  "original_name": "policy.pdf",
  "file_size": 1024000,
  "status": "uploaded",
  "uploaded_at": "2024-01-15T10:30:00",
  "uploaded_by": "user_uuid",
  "extracted_text": "120 chunks created"
}
```

#### List Documents
```
GET /documents/
```
Retrieve all uploaded documents (Admin only).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "id": "document_uuid",
    "filename": "policy1.pdf",
    ...
  }
]
```

---

### Chat & RAG Endpoints

#### Chat with Policy Documents
```
POST /chat/
```
Send a message and receive an AI-generated response based on policy documents.

**Request Body:**
```json
{
  "message": "What is the refund policy?",
  "session_id": "optional_session_uuid"
}
```

**Response:**
```json
{
  "session_id": "chat_session_uuid",
  "reply": "Based on our policies, the refund policy allows customers to request refunds within 30 days of purchase..."
}
```

## 🔄 How It Works

### Document Upload & Processing Pipeline

1. **Upload**: User uploads a PDF file
2. **Extraction**: Text is extracted from the PDF using PyMuPDF
3. **Storage**: PDF is stored in Supabase cloud storage
4. **Chunking**: Extracted text is split into manageable chunks
5. **Embedding**: Each chunk is embedded using Cohere's embedding model
6. **Indexing**: Embeddings are stored in PostgreSQL with pgvector
7. **Database**: Document metadata is saved to PostgreSQL

### Chat & RAG Pipeline

1. **User Query**: User sends a question via the chat endpoint
2. **Embedding**: User's message is embedded using the same model
3. **Retrieval**: Vector similarity search finds relevant document chunks
4. **Context Building**: Retrieved chunks are combined as context
5. **Generation**: Cohere's LLM generates a response using the context
6. **Response**: AI-generated answer is returned to the user
7. **Session Storage**: Chat history is saved for future reference

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **Role-Based Access**: Admin-only document upload functionality
- **Environment Variables**: Sensitive credentials stored in `.env`
- **CORS Ready**: Can be configured for secure cross-origin requests

## 📦 Dependencies

See `requirements.txt` for complete list:
- fastapi - Web framework
- uvicorn[standard] - ASGI server
- sqlalchemy - ORM
- pydantic & pydantic-settings - Data validation
- python-jose[cryptography] - JWT handling
- passlib[bcrypt] - Password hashing
- cohere - LLM API client
- supabase - Cloud database and storage
- pgvector - Vector search extension
- asyncpg - Async PostgreSQL driver
- PyMuPDF - PDF text extraction

## 🛠️ Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints for better code clarity
- Keep functions small and focused

## 📝 Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SUPABASE_URL` | Supabase project URL | ✓ | - |
| `SUPABASE_KEY` | Supabase API key | ✓ | - |
| `SUPABASE_DB_URL` | PostgreSQL connection string | ✓ | - |
| `COHERE_API_KEY` | Cohere API key | ✓ | - |
| `SECRET_KEY` | JWT secret key | ✓ | - |
| `ALGORITHM` | JWT algorithm | ✗ | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | ✗ | 30 |
| `LLM_MODEL` | Cohere model for generation | ✗ | command-r-08-2024 |
| `EMB_MODEL` | Cohere model for embeddings | ✗ | embed-v4.0 |

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure allowed hosts/CORS
- [ ] Use environment variables for all secrets
- [ ] Set up proper logging
- [ ] Enable HTTPS
- [ ] Configure database backups
- [ ] Set up monitoring and alerting
- [ ] Review security headers

## 📖 API Documentation

Once the server is running, interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Add tests
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**Database Connection Error**
- Verify `SUPABASE_DB_URL` is correct
- Check PostgreSQL service is running
- Ensure network connectivity to Supabase

**Cohere API Error**
- Verify `COHERE_API_KEY` is valid
- Check API quota and billing
- Ensure you have permission for the specified models

**PDF Upload Fails**
- Verify file is a valid PDF
- Check Supabase storage bucket permissions
- Ensure disk space is available

## 📞 Support

For issues, questions, or contributions, please contact the development team or open an issue in the repository.

---

**Last Updated**: March 2026