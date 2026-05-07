import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import project_tools

logging.basicConfig(level=logging.INFO)

# Create FastAPI application instance
app = FastAPI(
    title="Developer Project Idea Generator API",
    description="Generate interesting application project ideas for developers",
    version="1.0.0"
)

# Configure CORS (allows frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include our project tools routes
app.include_router(
    project_tools.router,
    prefix="/api",  # All routes start with /api
    tags=["project_tools"]  # Group in API docs
)

# Root endpoint (for testing if API is running)
@app.get("/")
async def root():
    return {
        "message": "Developer Project Idea Generator API is running!",
        "endpoints": {
            "generate_project_ideas": "/api/projects/generate-project-ideas?user_topic=YOUR_TOPIC",
            "generate_project_ideas_with_descriptions": "/api/projects/generate-project-ideas-with-descriptions?project_idea=YOUR_TOPIC&tone=professional"
        }
    }


# Run the application (only when running directly)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
