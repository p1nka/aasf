# aasf/a_ingestion/text_parser.py

import logging
from .base_parser import BaseParser

logger = logging.getLogger("AASF.TextParser")

class TextParser(BaseParser):
    """A concrete parser for plain text (.txt) files."""

    def parse(self, filepath: str) -> str:
        """
        Reads and returns the content of a text file.

        Args:
            filepath (str): The path to the .txt file.

        Returns:
            str: The content of the file.
        """
        logger.info(f"Parsing text file: {filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
        except Exception as e:
            logger.error(f"Could not parse text file {filepath}: {e}")
            raise