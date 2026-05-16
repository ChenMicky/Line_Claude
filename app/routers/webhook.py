import logging
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from app.services.claude_client import ClaudeClient
from app.services.wiki_loader import load_wiki_content

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["webhook"])

# Initialize clients
claude_client = ClaudeClient()


class N8nWebhookRequest(BaseModel):
    """Request model for n8n webhook endpoint."""
    message: str = Field(..., description="The user's message to process")
    conversation_history: Optional[list] = Field(
        default=None,
        description="Optional conversation history for context"
    )
    wiki_path: Optional[str] = Field(
        default=None,
        description="Optional custom path to wiki directory"
    )

    class Config:
        schema_extra = {
            "example": {
                "message": "What is the capital of France?",
                "conversation_history": None,
                "wiki_path": None
            }
        }


class N8nWebhookResponse(BaseModel):
    """Response model for n8n webhook endpoint."""
    success: bool
    response: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@router.post("/n8n", response_model=N8nWebhookResponse, status_code=status.HTTP_200_OK)
async def n8n_webhook(request: N8nWebhookRequest):
    """
    Receive webhook data from n8n and process with Claude API + wiki context.

    This endpoint:
    - Receives data from n8n workflows
    - Loads Obsidian wiki content as context
    - Calls Claude API with the context and user message
    - Returns the generated response
    """
    try:
        logger.info(f"Received webhook request: {request.message[:50]}...")

        # Load wiki content
        wiki_content = load_wiki_content(request.wiki_path)
        logger.info(f"Wiki content loaded: {len(wiki_content)} characters")

        # Generate response using Claude API
        result = claude_client.generate_response(
            user_message=request.message,
            wiki_content=wiki_content,
            conversation_history=request.conversation_history
        )

        if result["success"]:
            return N8nWebhookResponse(
                success=True,
                response=result["response"],
                metadata={
                    "model": result.get("model"),
                    "usage": result.get("usage")
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Unknown error occurred")
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/n8n/health")
async def webhook_health():
    """Health check for webhook endpoint."""
    return {"status": "healthy", "endpoint": "n8n-webhook"}


# Health check endpoint is in the main router
# This is here for modularity if we split health checks later
