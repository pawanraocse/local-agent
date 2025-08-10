# Local AI Support Bot Template

A template project for creating local AI-powered support bots using Ollama. This project provides a Docker-based setup for running Ollama models locally and building AI-powered applications.

## Features

- 🐳 Docker-based setup with Ollama integration
- 📄 Document processing (PDF, TXT, DOC, DOCX)
- 🤖 Local AI processing using Ollama models
- 🔍 Document embeddings for semantic search
- 🌐 REST API interface with FastAPI
- 🔄 Automatic model management and updates

## Prerequisites

- Docker
- Docker Compose
- Git

## Quick Start

1. Clone this repository:

```bash
git clone <your-repo-url>
cd local-support-bot
```

2. Start the services:

```bash
docker-compose up --build
```

The services will be available at:

- Ollama API: `http://localhost:11434`
- Support Bot API: `http://localhost:8000`

## Project Structure

```
.
├── app/                    # Application code
│   └── main.py            # FastAPI application
├── documents/             # Document storage directory
├── Dockerfile            # Application container configuration
├── Dockerfile.ollama     # Ollama container configuration
├── docker-compose.yml    # Docker services configuration
├── requirements.txt      # Python dependencies
└── start-ollama.sh      # Ollama startup script
```

## Configuration

### Models

The project is configured to use the following models by default:

- `llama2` for general text generation
- `nomic-embed-text` for embeddings

You can modify the models in `docker-compose.yml` and `start-ollama.sh`.

### API Endpoints

- `POST /generate`: Generate code for a given task (JSON: `{ "task": "...", "context": "..." }`)
- `POST /review`: Review code for quality, bugs, and improvements (JSON: `{ "code": "..." }`)
- `GET /history`: Retrieve recent agent history (query param: `limit`)
- `POST /upload`: Upload new documents
- `GET /docs`: API documentation (Swagger UI)

## API Documentation UI

- The project provides an interactive API documentation UI using **Swagger (OpenAPI)**, automatically available at:
  - [http://localhost:8000/docs#/default/generate_code_generate_post](http://localhost:8000/docs#/default/generate_code_generate_post)
- Use this UI to explore, test, and debug all available API endpoints directly from your browser.

### CLI Usage

You can also use the agent via CLI for local/manual testing:

- Generate code:
  ```bash
  python app/cli_agent.py generate --task "Write a Python function to add two numbers"
  ```
- Review code (string):
  ```bash
  python app/cli_agent.py review --code "def add(a, b): return a + b"
  ```
- Review code (file):
  ```bash
  python app/cli_agent.py review --code path/to/your_file.py
  ```

## Using as a Template

1. Fork or clone this repository
2. Modify the following files to customize for your needs:
   - `app/main.py`: Update API endpoints and business logic
   - `docker-compose.yml`: Adjust service configurations
   - `requirements.txt`: Add/remove Python dependencies
   - `start-ollama.sh`: Modify model configurations

## Development

### Adding New Features

1. Update the FastAPI application in `app/main.py`
2. Add new dependencies to `requirements.txt`
3. Rebuild the containers:

```bash
docker-compose up --build
```

### Testing

All tests (unit, API, CLI) can be run with a single command:

```bash
bash test.sh
```

This script will:
- Run all tests inside the Docker container
- Generate an HTML report at `./test-reports/report.html`
- Clean up containers after the run

Open `test-reports/report.html` in your browser to review detailed results.

## Troubleshooting

1. If models fail to download:

   - Check your internet connection
   - Verify model names in `start-ollama.sh`
   - Check Docker logs: `docker-compose logs ollama`

2. If the API is not responding:
   - Ensure all containers are running: `docker-compose ps`
   - Check application logs: `docker-compose logs app`

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Project Index

- **app/agent.py**: Core agent logic (LLM, RAG, ChromaDB integration).
- **app/cli_agent.py**: CLI entry point for agent operations (code generation, review).
- **app/dto/**: DTOs for API and CLI requests/responses.
- **app/config.py**: Application configuration settings.
- **app/init_ollama.py**: Initialization logic for Ollama integration.
- **app/main.py**: Main entry point for the backend application.
- **requirements.txt**: Python dependencies for the project.
- **Dockerfile / Dockerfile.ollama**: Containerization setup for deployment.
- **docker-compose.yml**: Multi-container orchestration.
- **start-ollama.sh**: Script to start Ollama service.

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the application:
   ```bash
   python app/main.py
   ```
3. (Optional) Use Docker:
   ```bash
   docker-compose up --build
   ```

## Structure

- All backend logic is under the `app/` directory.
- Configuration and initialization are separated for clarity and maintainability.

## 🛠️ Agentic AI End-to-End Flow Diagram

**Agentic AI End-to-End Flow:**

1. **User/API Client** sends a request (e.g., `/generate`) to the FastAPI backend.
2. **FastAPI Endpoint** receives the request and forwards it to the **LangChainAgent**.
3. **LangChainAgent** orchestrates a multi-step workflow:
    - **Code Generation Tool**: Generates initial code based on the task/context.
    - **Code Review Tool**: Reviews the generated code for quality and issues.
    - **Code Refactor Tool**: Refactors the code for readability, performance, or maintainability.
    - **Test Generation Tool**: Generates test cases for the code.
4. At each step, **AgentMemory (ChromaDB)** stores input/output for traceability and future retrieval (RAG).
5. The final, comprehensive response (including code, review, refactored code, tests, and metadata) is returned to the user/client.

**Flow Diagram (Textual):**

```
User/API Client
   |
   v
FastAPI Endpoint (`/generate`, `/review`, `/history`)
   |
   v
LangChainAgent (ReAct, tools, memory)
   |
   v
[Code Generation Tool] → [Code Review Tool] → [Code Refactor Tool] → [Test Generation Tool]
   |
   v
AgentMemory (ChromaDB)
   |
   v
Comprehensive Response (API/CLI)
```

### **Flow Description**
1. **User/API Client** sends a request (e.g., /generate) to the FastAPI backend.
2. **FastAPI Endpoint** receives the request and forwards it to the **LangChainAgent**.
3. **LangChainAgent** orchestrates a multi-step workflow:
    - **Code Generation Tool**: Generates initial code based on the task/context.
    - **Code Review Tool**: Reviews the generated code for quality and issues.
    - **Code Refactor Tool**: Refactors the code for readability, performance, or maintainability.
    - **Test Generation Tool**: Generates test cases for the code.
4. At each step, **AgentMemory (ChromaDB)** stores input/output for traceability and future retrieval (RAG).
5. The final, comprehensive response (including code, review, refactored code, tests, and metadata) is returned to the user/client.

## Advanced Features & Architecture

### Agentic Memory with ChromaDB
- Integrated persistent memory using ChromaDB (vector DB) for context-aware agent responses.
- Memory context is retrieved and injected into agent prompts for multi-turn and context-dependent queries.
- Memory warnings (e.g., requesting more results than exist) are handled gracefully and do not impact agent stability.

### Tool Use & LangChain ReAct Agent
- Uses LangChain's ReAct agent architecture for tool-based reasoning (e.g., Wikipedia search, code review).
- Patched Wikipedia tool to always use the `lxml` parser, suppressing BeautifulSoup warnings.
- Agent iteration and execution time limits are configurable (default: 8 iterations, 60 seconds) to balance performance and completeness.

### Error Handling & Logging
- Structured logging throughout all layers for traceability and debugging.
- Robust error handling with clear, actionable error messages.
- All API responses use DTOs for consistency and security.

### Configuration & Telemetry
- Model and service configuration is centralized in `app/config.py`.
- ChromaDB telemetry is disabled by default for privacy and to avoid known errors.

## Recent Improvements
- Increased agent iteration and execution time limits for better tool use.
- Patched Wikipedia tool integration for parser stability.
- Disabled ChromaDB telemetry to prevent noisy errors.
- Improved memory context retrieval and injection for agent queries.
- Enhanced logging and error handling across all layers.

## How Memory Works
- The agent stores and retrieves query/response pairs in ChromaDB.
- For simple queries, memory may not impact results, but for multi-turn or context-dependent queries, memory provides relevant history to the agent.

## Production Readiness
- Modular, testable, and clean architecture following best practices.
- All major flows are covered by unit and integration tests (see `tests/`).
- CI/CD ready with automated test orchestration and reporting.

---
