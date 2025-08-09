# Copilot Index: Local-Agent Project

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
- [ ] **LangChain Integration:**
    - Use LangChain chains/tools for orchestration and reasoning.
    - Connect LangChain to Ollama for LLM-powered code tasks.
- [ ] **LangChain Orchestration:**
    - Integrate LangChain chains, tools, and agents for modular, composable workflows.
    - Enable multi-step, multi-agent orchestration for complex coding tasks.
- [ ] **Memory & RAG:**
    - Persist agent history, context, and code snippets in a vector DB (ChromaDB).
    - Implement Retrieval-Augmented Generation (RAG) for context-aware responses.
- [ ] **Advanced Memory & RAG:**
    - Maintain agent context/history using vector stores (ChromaDB, Weaviate, etc.).
    - Implement advanced Retrieval-Augmented Generation (RAG) for context-aware, high-quality responses.
- [ ] **DTOs & API Design:**
    - Use DTOs for all external communications.
    - Document and validate all API endpoints.
- [ ] **Security & Validation:**
    - Add authentication (OAuth2/JWT) and input validation for production readiness.
    - Integrate structured error handling and validation at all layers.
- [ ] **Testing & CI/CD:**
    - Expand unit/integration tests for agent logic and API endpoints.
    - Integrate with CI/CD (Jenkins, GitHub Actions) for automated validation.
    - Achieve 80%+ test coverage for business logic.
    - Use Testcontainers for integration tests.
- [ ] **Logging & Traceability:**
    - Ensure structured logging with business context (requestId, operation, userId).
    - Maintain traceable history of agent actions and decisions.
    - Use SLF4J-style logging (or Python equivalent) with context.
- [ ] **Documentation:**
    - Update README.md and copilot-index.md with new modules, APIs, and flows.
    - Auto-generate OpenAPI documentation for all endpoints.
    - Maintain up-to-date project index after every significant change.
- [ ] **Architecture & Modularity:**
    - Apply clean architecture layering: Controllers → Services → Repositories.
    - Promote testability, modularity, readability, and traceability.
    - Use abstractions and avoid tight coupling.
- [ ] **MCP Integration (Future):**
    - Add a Model Control Plane (MCP) server/module to enable integration with external UIs or tools.
    - Define clear APIs/interfaces for communication (REST/gRPC/message queues).
    - Document responsibilities, flows, and update security/logging as needed.
- [ ] **Naming Conventions & Update Policy:**
    - Enforce naming conventions for controllers, services, DTOs, and tests.
    - Update copilot-index.md after every significant code change, new feature, or refactor.
