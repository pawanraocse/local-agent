from dto.mcp import MCPContextRequest, MCPContextResponse
from agentic.agent_service import AgenticAIService
import logging

logger = logging.getLogger("mcp")

class MCPService:
    def __init__(self, agentic_service: AgenticAIService):
        self.agentic_service = agentic_service

    def handle_context(self, request: MCPContextRequest) -> MCPContextResponse:
        if request.context_type == "generate":
            task = request.payload.get("task")
            if not task:
                return MCPContextResponse(status="error", data={"error": "Missing 'task' in payload"})
            logger.info(f"MCPService: Generating code for task: {task}")
            result = self.agentic_service.run(task)
            return MCPContextResponse(status="ok", data={"result": result})
        # For demo: just echo the payload with a status
        return MCPContextResponse(
            status="ok",
            data={"echo": request.payload, "type": request.context_type}
        )
