import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Type

from ollama import AsyncClient, Client



load_dotenv()

OLLAMA_HOST = "https://ollama.com"
DEFAULT_API_KEY = os.getenv("AI_API_KEY")


# Create Ollama async client
def create_client(api_key: str) -> AsyncClient:
    return AsyncClient(
        host=OLLAMA_HOST,
        headers={"Authorization": f"Bearer {api_key}"}
    )


async def generate_with_response_model(
    prompt: str,
    response_model: Type[BaseModel],
    api_key: str
) -> BaseModel:
    """
    Generate response with structured output using the configured Ollama LLM.
    """
    
    try:
        client = create_client(api_key)

        # Call the model and ask it to return raw JSON
        response = await client.chat(
            model="gemma4:31b-cloud",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that outputs only valid JSON. Always complete your JSON responses fully. Raw json, no wrapping in markdown or explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        # print("response: ", response)

        # Get the response text
        response_text = response.message.content
        
        # Parse JSON
        json_data = json.loads(response_text)
        
        # Handle list responses
        if isinstance(json_data, list):
            json_data = {"titles": json_data}
        
        # Validate with Pydantic
        validated_data = response_model(**json_data)
        
        return validated_data
        
    except json.JSONDecodeError as e:
        raise Exception(
            f"Failed to parse JSON response: {e}\n"
            f"Response was: {response_text[:500]}"
        )
    except Exception as e:
        raise Exception(f"Error generating response: {e}")
