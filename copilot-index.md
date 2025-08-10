# Copilot Index: Local-Agent Project

## TODO / Recent Updates
- [x] Integrated LangChain ReAct agent via `AgenticAIService` (`app/agentic/agent_service.py`) for advanced code generation and tool use.
- [x] Added robust error handling, DTO usage, and structured logging throughout the agent and API layers.
- [x] Switched to model auto-selection logic in `config.py` for test/dev speed.
- [x] Updated prompt engineering and agent execution for smaller models and better reliability.
- [x] Improved project index to reflect new agentic architecture and flows.

## Overview
Local-Agent is a Python 3.11+ backend for local AI agent orchestration, leveraging Docker, Ollama, LangChain, and ChromaDB for advanced, context-aware code generation and review. The architecture is modular, testable, and production-ready, following clean layering and DTO-based API design.

## Entry Points
- **app/main.py**: FastAPI application entrypoint (API endpoints)
- **app/cli_agent.py**: CLI entrypoint for agent operations
- **test.sh**: Test automation script

## Modules/Folders
- **app/**: Backend application logic
  - **agent.py**: Core agent logic (LLM, RAG, ChromaDB integration)
  - **cli_agent.py**: CLI interface for agent operations
  - **dto/**: DTOs for API and CLI requests/responses
  - **config.py**: Centralized configuration (env vars, model, telemetry)
  - **init_ollama.py**: Ollama LLM initialization
  - **main.py**: FastAPI app, API endpoints, orchestration
  - **agentic/**: Agentic architecture (ReAct agent, tools, memory)
    - **agent_service.py**: LangChain ReAct agent, memory/context integration, error handling
    - **tools_loader.py**: Tool loading, Wikipedia tool patching
  - **llm/**: LLM interface (Ollama integration)
  - **memory/**: ChromaDB memory service
- **documents/**: Document storage
- **test-reports/**: HTML test reports
- **tests/**: Unit and integration tests

## Key Classes/Files
- **AgenticAIService** (`app/agentic/agent_service.py`):
  - Orchestrates ReAct agent, tool use, memory retrieval, and error handling
  - Configurable iteration/time limits (default: 8/60)
  - Structured logging and traceability
- **ChromaMemoryService** (`app/memory/chroma_memory_service.py`):
  - Handles persistent memory (query/response pairs) using ChromaDB
  - Handles result count warnings gracefully
- **DTOs** (`app/dto/`):
  - All API/CLI requests and responses use DTOs for security and consistency
- **Tool Loader** (`app/agentic/tools_loader.py`):
  - Loads LangChain tools, patches Wikipedia tool for lxml parser

## Main Flows
- **API**: User → FastAPI endpoint (/generate, /review, /history) → AgenticAIService → LLM/ChromaDB → Response
- **CLI**: User → CLI → AgenticAIService → LLM/ChromaDB → Output
- **Memory**: Each query/response is stored in ChromaDB; memory context is retrieved and injected for context-aware responses

## Dependencies
- **FastAPI**: API framework
- **LangChain**: Agentic reasoning, tool use
- **Ollama**: LLM backend
- **ChromaDB**: Vector DB for memory/context
- **Wikipedia**: Tool for external knowledge (patched for lxml parser)
- **Docker/Docker Compose**: Containerization

## Test Coverage
- All business logic, API, and CLI flows are covered by tests in `tests/`
- `test.sh` automates build, test, and reporting (HTML report in `test-reports/`)

## Auth/Security
- No authentication/session management by default; recommend OAuth2/JWT for production
- All inputs validated, secrets/config isolated in `config.py`

## Naming Conventions
- Controllers: `main.py` (API), `cli_agent.py` (CLI)
- Services: `*Service.py`
- DTOs: `dto/`
- Tests: `tests/`, `test_*.py`
- Config: `config.py`, `.env`

## Update Policy
- Update this file after every significant code change, new feature, or refactor.
- Document all new modules, flows, and dependencies.

## Recent Improvements
- Integrated persistent memory (ChromaDB) for context-aware agent responses
- Patched Wikipedia tool for parser stability
- Disabled ChromaDB telemetry by default
- Increased agent iteration/time limits for better tool use
- Enhanced logging, error handling, and DTO usage throughout
- Improved test automation and reporting
