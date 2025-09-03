# aasf/b_discovery/section_finder.py

import logging
from typing import List, Dict

logger = logging.getLogger("AASF.SectionFinder")


class SectionFinder:
    """Finds and isolates agent definition sections within a document's text."""

    def __init__(self, config: Dict):
        self.delimiter = config.get('section_delimiter', '---')
        logger.debug(f"Initialized SectionFinder with delimiter: '{self.delimiter}'")

    def find_sections(self, full_text: str) -> List[str]:
        """
        Splits the document text into sections based on the configured delimiter.

        Args:
            full_text (str): The entire text content of the document.

        Returns:
            List[str]: A list of text blocks, each potentially an agent definition.
        """
        logger.info(f"Splitting document content into sections using delimiter.")
        sections = full_text.split(self.delimiter)

        # Filter out empty sections that may result from splitting
        valid_sections = [s.strip() for s in sections if s.strip()]
        logger.info(f"Found {len(valid_sections)} non-empty sections.")

        return valid_sections