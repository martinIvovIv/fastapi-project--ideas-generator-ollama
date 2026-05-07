import json
import logging
import time
from typing import Annotated

from fastapi import APIRouter, Query, Request
from pydantic import ValidationError

# Import our custom modules
from ..models.project_models import ProjectIdeas, ProjectIdeasWithDescriptions
from ..services import llm_api as llm
from ..services import prompts as pr

logger = logging.getLogger("AppLogger")

router = APIRouter()


def log_request_attempt(
    request: Request,
    start_time: float,
    retry_count: int,
    max_retries: int
) -> None:
    elapsed_time = time.time() - start_time
    logger.info(
        "%s attempt %s/%s finished in %.2fs",
        request.url.path,
        retry_count + 1,
        max_retries,
        elapsed_time
    )


@router.get("/projects/generate-project-ideas")
async def generate_project_ideas(
    user_topic: Annotated[str, Query(min_length=1, max_length=140)],
    request: Request
):
    """
    Generate 10 interesting application projects for a given topic.
    
    Args:
        user_topic: The project topic (e.g., "AI tools for writers")
        request: FastAPI request object (automatically provided)
    
    Returns:
        JSON response with success status and list of project ideas
    """
    
    start_time = time.time()
    
    # Maximum number of retry attempts
    max_retries = 5
    
    # Try up to 5 times (in case of temporary failures)
    for retry_count in range(max_retries):
        try:
            
            prompt = pr.generate_project_ideas.format(topic=user_topic)
            
            result: ProjectIdeas = await llm.generate_with_response_model(
                prompt=prompt,
                response_model=ProjectIdeas
            )
            
            return {
                "success": True,
                "message": "Generated project ideas successfully",
                "result": result.titles
            }
        
        # Handle specific error types
        except (json.JSONDecodeError, ValidationError) as e:
            # JSON parsing failed or data validation failed
            logger.warning(
                f"Failed during JSON decoding or validation. "
                f"Retry count: {retry_count + 1}."
            )
        
        except KeyError as e:
            # Missing expected key in response
            logger.warning(f"Missing key in JSON: {e}")
        
        except Exception as e:
            # Any other unexpected error
            logger.error(e)
            continue
        
        finally:
            log_request_attempt(request, start_time, retry_count, max_retries)
    
    # If all retries failed, return failure response
    return {
        "success": False,
        "message": f"Failed to generate project ideas after {max_retries} attempts",
        "result": None
    }


@router.get("/projects/generate-project-ideas-with-descriptions")
async def generate_project_ideas_with_descriptions(
    project_idea: Annotated[str, Query(min_length=1, max_length=140)],
    tone: Annotated[str, Query(min_length=1, max_length=50)],
    request: Request
):
    """
    Generate 10 project ideas with descriptions.
    
    Args:
        project_idea: Topic category (e.g., "developer productivity tools")
        tone: Response tone (e.g., "professional", "casual", "friendly")
    """
    start_time = time.time()
    max_retries = 5

    for retry_count in range(max_retries):
        try:

            # Format prompt with BOTH parameters
            prompt = pr.generate_project_ideas_with_descriptions.format(
                project_idea=project_idea,
                tone=tone
            )
            
            # Call LLM with NEW model
            result: ProjectIdeasWithDescriptions = await llm.generate_with_response_model(
                prompt=prompt,
                # temperature=1,
                response_model=ProjectIdeasWithDescriptions
            )
            
            return {
                "success": True,
                "message": "Generated project ideas with descriptions successfully",
                "result": result.titles_with_descriptions
            }

        except (json.JSONDecodeError, ValidationError) as e:
            logger.warning(
                f"Failed during JSON decoding or validation. "
                f"Retry count: {retry_count + 1}."
            )
            
        except KeyError as e:
            logger.warning(f"Missing key in JSON: {e}")
            
        except Exception as e:
            logger.error(e)
            continue
            
        finally:
            log_request_attempt(request, start_time, retry_count, max_retries)

    return {
        "success": False,
        "message": "Failed to generate project ideas with descriptions",
        "result": None
    }
