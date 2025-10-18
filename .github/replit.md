# ChatNova AI

## Overview

ChatNova AI is a commercial-grade multi-model AI chat application built with Python and Streamlit. It provides a unified interface for interacting with multiple AI providers (OpenAI GPT, Anthropic Claude, and Google Gemini) through a single application. The app features specialized AI personas, document processing capabilities, multi-threaded chat management, and conversation export functionality. It's designed as a productivity tool for content creation, coding assistance, business analysis, and research.

The application was built by converting an open-source base project into a branded commercial product suitable for platforms like AppSumo. It emphasizes a modern, cyber-themed UI with midnight blue and electric cyan branding.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework**: Streamlit multi-page application
- **Rationale**: Streamlit provides rapid development of data-driven web apps with Python, eliminating the need for separate frontend/backend architecture
- **Structure**: Multi-page app pattern with separate pages for Chat and Settings
- **UI Theme**: Custom CSS-based cyber/techy design with animated grid backgrounds, gradient effects, and glowing elements
- **State Management**: Streamlit session state for persisting user data, chat threads, API keys, and settings across page navigation
- **Styling Approach**: Inline CSS markdown injection for consistent branding (midnight blue #16213e, electric cyan #00BFFF)

**Pros**: 
- Rapid prototyping and deployment
- Python-native (no JavaScript required)
- Built-in reactive components

**Cons**: 
- Limited customization compared to React/Vue
- Not ideal for complex client-side interactions
- State resets on page refresh without persistence layer

### Backend Architecture

**Service Layer Pattern**: Utility modules in `utils/` directory provide separated concerns
- `ai_providers.py`: Multi-provider AI integration layer
- `chat_manager.py`: Thread-based conversation management
- `document_processor.py`: File upload and text extraction
- `export_manager.py`: Conversation export (TXT, PDF)
- `personas.py`: AI persona configuration and system prompts

**Rationale**: Modular separation allows easy provider swapping, testing, and feature extension without touching core chat logic

**No Database**: Uses Streamlit session state for data persistence
- **Limitation**: Data is browser-session-only and not persisted to disk
- **Trade-off**: Simpler deployment without database setup, but unsuitable for production multi-user scenarios
- **Future consideration**: Add SQLite or PostgreSQL for persistent storage

### AI Provider Integration

**Multi-Provider Strategy**: Abstracted provider interface supporting three AI services
- OpenAI (GPT models)
- Anthropic (Claude models)  
- Google Gemini

**Implementation**: 
- Provider-specific clients initialized on-demand with user-supplied API keys
- Unified `get_response()` method routes requests to appropriate provider
- Message format normalization across different provider APIs

**Alternatives Considered**:
- LangChain integration (rejected for simplicity - adds overhead)
- Single provider lock-in (rejected - multi-model is core feature)

**Pros**: Flexibility, user choice, redundancy if one provider fails
**Cons**: Requires users to manage multiple API keys, increased complexity in error handling

### Document Processing

**Supported Formats**: PDF, DOCX, TXT, CSV, images (PNG, JPG, etc.)

**Processing Pipeline**:
1. File upload via Streamlit file uploader
2. Format detection via file extension
3. Library-specific extraction (PyPDF2, python-docx, pandas)
4. Text content injection into chat context

**Rationale**: Enables "chat with documents" functionality without vector databases or RAG complexity

**Limitation**: Simple text extraction only - no semantic chunking, embeddings, or similarity search

### Chat Thread Management

**Multi-Thread Design**: Users can create multiple independent conversation threads
- Thread data structure: ID, name, messages array, timestamps, document context
- CRUD operations: Create, delete, rename threads
- Current thread pointer in session state

**Message Structure**:
```python
{
  'role': 'user' | 'assistant',
  'content': str,
  'timestamp': ISO datetime
}
```

**Persistence**: Session-only (browser refresh loses data)

### AI Persona System

**Four Pre-Configured Personas**:
1. Creative Writer (storytelling, poetry)
2. Code Assistant (programming, debugging)
3. Business Expert (strategy, analysis)
4. Research Pro (fact-checking, academic writing)

**Implementation**: Each persona has custom system prompt prepended to conversation
- Prompts defined in `personas.py`
- User selects persona via sidebar
- System prompt auto-injected before API call

**Rationale**: Provides specialized behavior without training custom models

### Export Functionality

**Supported Formats**: TXT (plain text), PDF (formatted document)

**Export Contents**:
- Thread metadata (name, timestamps)
- Document context (if attached)
- Full message history
- Branding footer

**PDF Generation**: Uses ReportLab for formatted PDF creation with styling

## External Dependencies

### AI Service APIs

1. **OpenAI API** (primary)
   - Endpoint: `https://api.openai.com/v1/`
   - Models: GPT-4, GPT-3.5, GPT-5 (referenced)
   - Authentication: Bearer token (user-provided API key)
   - Client: `openai` Python package

2. **Anthropic API** (optional)
   - Models: Claude family
   - Authentication: API key header
   - Client: `anthropic` Python package

3. **Google Gemini API** (optional)
   - Models: Gemini family
   - Authentication: API key
   - Client: `google-genai` Python package

### Document Processing Libraries

- **PyPDF2**: PDF text extraction
- **python-docx**: Microsoft Word document processing
- **pandas**: CSV file parsing and tabular data handling

### PDF Generation

- **ReportLab**: Professional PDF document creation with formatting
- **FPDF**: Alternative PDF generation library

### Web Framework

- **Streamlit**: Core application framework
  - Version: Latest stable
  - Deployment: Runs on configurable port (default: 5000)
  - Serves static assets from `assets/` directory

### Python Standard Library

- `os`: File system operations
- `datetime`: Timestamp management
- `io`: File-like object handling for document processing
- `uuid`: Unique thread ID generation
- `sys`: Path manipulation for module imports

### Storage

**Current**: Browser session storage (Streamlit session_state)
- No external database
- No file system persistence

**Note for Future Enhancement**: The application architecture is compatible with adding Drizzle ORM with PostgreSQL for persistent multi-user storage. Thread data structure is already dictionary-based and can map to relational schema.

### API Key Management

**User-Managed**: API keys stored in session state (non-persistent)
- Keys required: At least one provider (OpenAI, Anthropic, or Gemini)
- Storage: Memory-only during browser session
- Security consideration: Keys not encrypted or persisted to disk