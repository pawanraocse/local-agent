# Copilot Index: Local-Agent Project

## TODO / Recent Updates
- [x] Integrated LangChain ReAct agent via `AgenticAIService` (`app/agentic/agent_service.py`) for advanced code generation and tool use.
- [x] Added robust error handling, DTO usage, and structured logging throughout the agent and API layers.
- [x] Switched to model auto-selection logic in `config.py` for test/dev speed.
- [x] Updated prompt engineering and agent execution for smaller models and better reliability.
- [x] Improved project index to reflect new agentic architecture and flows.

## Overview
Local-Agent is a Python-based backend service designed for local AI agent orchestration. It leverages Docker for containerization and supports integration with Ollama for LLM operations. The project is structured for modularity, testability, and clean separation of concerns.

### Tech Stack
- **Language:** Python 3.11+
- **Containerization:** Docker, Docker Compose
- **LLM Integration:** Ollama (via Dockerfile.ollama)
- **Dependency Management:** requirements.txt

## Module Boundaries & Responsibilities

### app/
- **__init__.py:** Initializes the app module.
- **config.py:** Centralized configuration management (env vars, constants, secrets).
- **init_ollama.py:** Handles Ollama LLM initialization and integration logic.
- **main.py:** Application entrypoint; orchestrates startup, routing, and service registration. Implements API endpoints for code generation, code review, and agent history.

### Root Files
- **docker-compose.yml:** Multi-container orchestration (app, Ollama, etc.).
- **Dockerfile:** Builds the main Python app container.
- **Dockerfile.ollama:** Builds the Ollama LLM container.
- **requirements.txt:** Python dependencies (FastAPI, pydantic, logging, etc.).
- **start-ollama.sh:** Shell script to bootstrap Ollama service.
- **README.md:** Project documentation, setup, and usage instructions.

## Key Classes & Relationships
- **Config (config.py):** Loads and validates environment/configuration variables.
- **OllamaInit (init_ollama.py):** Encapsulates Ollama startup and health checks.
- **Main Application (main.py):** Registers routes, initializes services, and manages lifecycle events. Implements /generate, /review, and /history endpoints.

## Critical APIs
- **POST /generate:** Generate code for a given task (accepts task/context, returns code).
- **POST /review:** Review code for quality, bugs, and improvements (accepts code, returns review).
- **GET /history:** Retrieve recent agent history (returns documents and metadata).

## Event Flows
- **API Flow:** User → FastAPI endpoint (/generate, /review, /history) → Agent service → LLM/ChromaDB → Response.
- **CLI Flow:** User → CLI (cli_agent.py) → Agent service → LLM/ChromaDB → Output.

## Auth & Session Management
- **Current State:** No explicit authentication/session management implemented. Recommend adding OAuth2/JWT for production.

## Logging & Security
- **Logging:** Use Python logging module; ensure structured logs with context (requestId, operation).
- **Security:** Validate all inputs, restrict Docker exposure, and isolate secrets in config.py.

## Testing Strategy
- **Unit Tests:** For config, Ollama integration, agent logic, and DTOs.
- **Integration Tests:** For API endpoints (/generate, /review, /history), CLI, and container orchestration.

## CI/CD & Automated Testing

- **Test Automation:**
  - test.sh script orchestrates Docker build, service startup, health checks, and test execution.
  - Tests are run inside the running app container using docker exec, ensuring volume mounts sync test reports to the host.
  - HTML test reports are generated in ./test-reports/report.html for host access and review.
  - The script ensures clean startup/shutdown of all services for reliable, repeatable test runs.
- **Integration Points:**
  - Ready for integration with CI/CD tools (e.g., Jenkins, GitHub Actions) by invoking test.sh for automated validation.
  - All service ports (app: 8000, Ollama: 11434) are exposed for host and pipeline access.
  - Health checks and volume mounts ensure production-like test environments.

## Test Coverage & How to Run Tests

- All tests (unit, API, CLI) are located in the `tests/` directory.
- To run all tests and generate an HTML report, use:
  ```bash
  bash test.sh
  ```
- This script runs all tests inside the Docker container, generates a report at `./test-reports/report.html`, and cleans up containers after the run.
- Open `test-reports/report.html` in your browser to review detailed results.

## Recent Improvements

- **API Support:**
  - Implemented /generate and /review endpoints for code generation and code review, respectively.
  - Implemented /history endpoint to retrieve recent agent history from the vector DB.
- **Docker Compose:**
  - Removed obsolete version attribute for compatibility and clarity.
  - Added volume mounts for tests and test-reports to ensure test discovery and report accessibility.
- **Testing Workflow:**
  - test.sh now checks for running services, ensures clean startup, and always brings down services after tests.
  - Health checks for Ollama service prevent false negatives and improve reliability.
- **Traceability:**
  - All test results and reports are accessible from the host for manual review or CI/CD archiving.

## How to Resume

- Run `bash test.sh` to build, start, test, and clean up the environment.
- Access test reports at `./test-reports/report.html`.
- All changes and workflow improvements are documented here for future reference.

## Recommendations
- Add authentication and structured error handling.
- Document all public APIs in README.md.

## TODO: Coding Agent Roadmap

To make Local-Agent a full-featured coding agent (using LangChain + local Ollama model) that acts as a senior developer, the following tasks are planned:

- [x] **Agent Capabilities:**
    - Code generation, review, refactoring, bug fixing, test case creation, API design, code flow analysis.
    - Expose these capabilities via REST API endpoints.
- [ ] **Agentic AI Architecture:**
    - Refactor Local-Agent to use an agentic architecture leveraging LangChain and LangGraph for multi-step reasoning, tool use, and orchestration (e.g., code review → refactor → test generation).
    - Use LangGraph to compose and orchestrate complex, multi-step coding workflows.
    - Register all agent tools as LangChain tools for composability and extensibility.
    - Integrate vector DBs (ChromaDB, Weaviate, etc.) to persist agent history, context, and code snippets.
    - Implement advanced RAG for context-aware, high-quality responses.
    - Add authentication (OAuth2/JWT), input validation, and structured error handling at all layers for production readiness.
    - Ensure structured logging with business context (requestId, operation, userId) and maintain traceable history of agent actions and decisions.
    - Expand unit/integration tests for agentic workflows and API endpoints; target 80%+ test coverage.
    - Integrate with CI/CD (Jenkins, GitHub Actions) for automated validation.
    - Update README.md and copilot-index.md with new modules, APIs, and flows after every significant change.
    - Auto-generate OpenAPI documentation for all endpoints.
    - Maintain up-to-date project index and architectural documentation.
    - Apply clean architecture layering: Controllers → Services → Repositories.
    - Promote testability, modularity, readability, and traceability.
    - Use abstractions and avoid tight coupling.
    - Enforce naming conventions for controllers, services, DTOs, and tests.
    - Update copilot-index.md after every significant code change, new feature, or refactor.
    - Add a Model Control Plane (MCP) server/module to enable integration with external UIs or tools.
    - Define clear APIs/interfaces for communication (REST/gRPC/message queues).
    - Document responsibilities, flows, and update security/logging as needed.
- [ ] Integrate vector DB memory (ChromaDB) for agent context/history and RAG (Retrieval-Augmented Generation).
    - Store user queries, agent responses, code snippets, reviews, and metadata.
    - Use LangChain's VectorStoreRetrieverMemory or similar for memory integration.
    - Update AgenticAIService to inject and use memory for context-aware responses.
    - Expose memory/history APIs for querying and management.
    - Ensure persistent ChromaDB storage in Docker Compose.

## Agentic AI End-to-End Flow Diagram

[User/API Client]
    |
    v
[FastAPI Endpoint (/generate)]
    |
    v
[LangChainAgent (app/agentic/langchain_agent.py)]
    |
    v
[Code Generation Tool]
    |
    v
[Code Review Tool]
    |
    v
[Code Refactor Tool]
    |
    v
[Test Generation Tool]
    |
    v
[AgentMemory (ChromaDB) - stores input/output for traceability]
    |
    v
[Comprehensive Response (code, review, refactored code, tests, metadata)]
    |
    v
[API Response to User]

**Flow Description:**
1. User/API Client sends a request (e.g., /generate) to the FastAPI backend.
2. FastAPI Endpoint receives the request and forwards it to the LangChainAgent.
3. LangChainAgent orchestrates a multi-step workflow:
    - Code Generation Tool: Generates initial code based on the task/context.
    - Code Review Tool: Reviews the generated code for quality and issues.
    - Code Refactor Tool: Refactors the code for readability, performance, or maintainability.
    - Test Generation Tool: Generates test cases for the code.
4. At each step, AgentMemory (ChromaDB) stores input/output for traceability and future retrieval (RAG).
5. The final, comprehensive response (including code, review, refactored code, tests, and metadata) is returned to the user/client.
