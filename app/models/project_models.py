from pydantic import BaseModel
from typing import List

class ProjectIdeas(BaseModel):
    titles: List[str]

class ProjectIdeasGeneratorResponse(BaseModel):
    success: bool
    message: str
    titles: List[str]

class ProjectIdeasWithDescription(BaseModel):
    title: str
    description: str

class ProjectIdeasWithDescriptions(BaseModel):
    titles_with_descriptions: List[ProjectIdeasWithDescription]
