import os
import logging
from typing import Optional, Dict, Any
from urllib import response
import httpx

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"


class ClaudeClient:
    """Client for interacting with OpenRouter API (Anthropic-compatible format) with wiki context support."""

    def __init__(self):
        """Initialize the OpenRouter client with API key from environment."""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", DEFAULT_BASE_URL)

        # Model must be set in .env file
        self.model = os.getenv("OPENROUTER_MODEL")
        if not self.model:
            logger.warning("OPENROUTER_MODEL not set in .env file. Please configure it.")

        # Max tokens must be set in .env file
        max_tokens_str = os.getenv("MAX_TOKENS")
        if not max_tokens_str:
            logger.warning("MAX_TOKENS not set in .env file. Please configure it.")
            self.max_tokens = 4096  # Fallback default
        else:
            self.max_tokens = int(max_tokens_str)

        if not self.api_key:
            logger.warning("OPENROUTER_API_KEY not set. OpenRouter API calls will fail.")
        else:
            logger.info(f"OpenRouter client initialized with model: {self.model}")
            logger.info(f"Base URL: {self.base_url}")

    def _build_system_prompt(self, wiki_content: str) -> str:
        """
        Build the system prompt incorporating wiki content.

        Args:
            wiki_content: Combined content from Obsidian wiki

        Returns:
            System prompt string
        """
        if not wiki_content:
            return "You are a helpful assistant."

        # Truncate if too long (approximate token count as chars/4)
        max_chars = self.max_tokens * 4  # Rough estimate
        if len(wiki_content) > max_chars:
            logger.warning(
                f"Wiki content too long ({len(wiki_content)} chars), "
                f"truncating to {max_chars} chars"
            )
            wiki_content = wiki_content[:max_chars] + "\n... (content truncated)"
            logger.warning(
                f"After truncated the wiki_content is: {wiki_content}"
            )
        system_prompt = f"""You are a helpful assistant with access to an Obsidian wiki knowledge base.

Here is the content from the Obsidian wiki:

{wiki_content}

Please use this wiki content as context when answering questions. If the answer can be found in the wiki, cite the relevant sections. If the wiki doesn't contain relevant information, you can still answer based on your general knowledge."""

        return system_prompt

    def generate_response(
        self,
        user_message: str,
        wiki_content: str = "",
        conversation_history: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Generate a response using OpenRouter API with wiki context.

        Args:
            user_message: The user's input message
            wiki_content: Content from Obsidian wiki to use as context
            conversation_history: Optional list of previous messages

        Returns:
            Dict containing response text and metadata
        """
        if not self.api_key:
            error_msg = "OpenRouter API client not initialized. Check OPENROUTER_API_KEY."
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "response": None
            }

        try:
            # Build system prompt with wiki content
            system_prompt = self._build_system_prompt(wiki_content)

            logger.debug(f"Final System Prompt: {system_prompt[:200]}...")
            # Build messages list
            messages = []

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Add current user message
            messages.append({"role": "user", "content": user_message})

            logger.info(f"Sending request to OpenRouter API with {len(messages)} messages")

            # Prepare the request payload 
            payload = { 
                "model": self.model,
                "max_tokens": self.max_tokens,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    *messages
                ]
            }

            # Call OpenRouter API using httpx
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",  # OpenRouter requires this
                "X-Title": "n8n-Claude Wiki API"  # Optional: identifies your app
            }

            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers
                )

                # Check for HTTP errors
                if response.status_code != 200:
                    error_msg = f"OpenRouter API error: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    return {"success": False, "error": error_msg, "response": None}

                result = response.json()

            # Extract response text
            response_text = result["choices"][0]["message"]["content"]

            # Get usage information
            usage = result.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)


            logger.info(f"OpenRouter API response received: {len(response_text)} chars")

            return {
                "success": True,
                "response": response_text,
                "model": result.get("model", self.model),
                "usage": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens
                }
            }

        except httpx.TimeoutException as e:
            error_msg = f"OpenRouter API timeout: {e}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg, "response": None}

        except httpx.ConnectError as e:
            error_msg = f"OpenRouter API connection error: {e}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg, "response": None}

        except Exception as e:
            error_msg = f"Unexpected error calling OpenRouter API: {e}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg, "response": None}
