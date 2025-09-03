# aasf/c_extraction/models.py

from pydantic import BaseModel, Field, validator
from typing import Optional


class AgentDefinition(BaseModel):
    """A validated data model representing a single extracted agent."""
    agent_id: str
    agent_name: str
    class_name: Optional[str] = Field(None, description="A Python-valid class name")

    primary_function: Optional[str]
    type: Optional[str]
    priority: Optional[str]
    resource_requirements: Optional[str]

    raw_section_text: str = Field(..., repr=False, description="The original text block for this agent.")

    @validator('class_name', pre=True, always=True)
    def generate_class_name(cls, v, values):
        """Generates a PEP-8 compliant class name from the agent_name."""
        if 'agent_name' in values and values.get('agent_name'):
            name = values['agent_name']
            # e.g., "Document Analysis Agent" -> "DocumentAnalysisAgent"
            return "".join(word.capitalize() for word in name.split())
        # This fallback should ideally not be hit if agent_name is present
        return "UnnamedAgent"