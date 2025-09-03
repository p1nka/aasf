# aasf/a_ingestion/pdf_parser.py

import logging
import pdfplumber
from .base_parser import BaseParser

logger = logging.getLogger("AASF.PdfParser")

class PdfParser(BaseParser):
    """A concrete parser for Portable Document Format (.pdf) files."""

    def parse(self, filepath: str) -> str:
        """
        Opens a PDF, extracts text from all pages, and joins them.

        Args:
            filepath (str): The path to the .pdf file.

        Returns:
            str: The concatenated text content of the PDF.
        """
        logger.info(f"Parsing PDF file: {filepath}")
        full_text = []
        try:
            with pdfplumber.open(filepath) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        full_text.append(text)
                    else:
                        logger.warning(f"No text found on page {i+1} of {filepath}")
            return "\n".join(full_text)
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
        except Exception as e:
            logger.error(f"Could not parse PDF file {filepath}: {e}")
            raise