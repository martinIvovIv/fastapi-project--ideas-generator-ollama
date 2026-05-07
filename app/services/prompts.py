generate_project_ideas = """I want you to act as a senior developer and product-minded project mentor.
Generate 10 practical but interesting application project ideas for a developer based on this topic: {topic}.
The ideas should be specific enough to build, creative enough to stand out in a portfolio, and varied in scope.
Favor projects that let a developer practice real-world skills such as APIs, databases, authentication, background jobs, automation, testing, integrations, or polished frontend workflows.
Avoid generic ideas like "todo app" unless they include a distinctive technical angle.
                                 
IMPORTANT: The output should be a JSON array of 10 project idea titles without field names. Just the titles. Make sure the JSON is valid.
                                                  
Example Output:
[
    "Project Idea 1",
    "Project Idea 2",
    "Project Idea 3",
    "Project Idea 4",
    "Project Idea 5",
    "Project Idea 6",
    "Project Idea 7",
    "Project Idea 8",
    "Project Idea 9",
    "Project Idea 10"
]"""



generate_project_ideas_with_descriptions = """As a senior developer mentor, generate a list of 10 creative application project ideas for a developer interested in {project_idea}.
Each idea should include a concise title and a brief description explaining what the developer would build, the main user value, and the notable technical concepts they could practice.
The ideas should be current, portfolio-worthy, and realistic for an individual developer or small team.
Use a {tone} tone.

IMPORTANT: Output should be valid JSON format like this:
{{
    "titles_with_descriptions": [
        {{
            "title": "Project Idea Title Here",
            "description": "Brief description of the application project idea"
        }}
    ]
}}
"""
