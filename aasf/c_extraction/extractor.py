# aasf/c_extraction/extractor.py

import re
import logging
from typing import Dict, Optional
from .models import AgentDefinition

logger = logging.getLogger("AASF.Extractor")


class AgentExtractor:
    """Extracts structured agent data from a text section."""

    def __init__(self, config: Dict):
        self.patterns = config.get('extraction_patterns', {})
        if not self.patterns:
            raise ValueError("Extraction patterns not found in configuration.")
        logger.debug("AgentExtractor initialized with configured patterns.")

    def extract(self, section_text: str) -> Optional[AgentDefinition]:
        """
        Extracts agent details from a text block based on config patterns.

        Args:
            section_text (str): A block of text containing one agent's definition.

        Returns:
            Optional[AgentDefinition]: A validated Pydantic model or None if extraction fails.
        """
        header_pattern = self.patterns.get('header')
        if not header_pattern:
            logger.error("Header pattern is missing in config.")
            return None

        header_match = re.search(header_pattern, section_text, re.MULTILINE)
        if not header_match:
            return None  # This is expected for non-agent sections, so no warning.

        agent_data = header_match.groupdict()
        logger.info(f"Found potential agent header for ID: {agent_data.get('agent_id')}")

        for attr, pattern in self.patterns.get('attributes', {}).items():
            attr_match = re.search(pattern, section_text, re.MULTILINE)
            if attr_match:
                agent_data[attr] = attr_match.group(1).strip()

        try:
            return AgentDefinition(**agent_data, raw_section_text=section_text)
        except Exception as e:
            logger.error(f"Pydantic validation failed for agent '{agent_data.get('agent_id')}': {e}")
            return None