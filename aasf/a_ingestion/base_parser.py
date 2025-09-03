# aasf/a_ingestion/base_parser.py

from abc import ABC, abstractmethod


class BaseParser(ABC):
    """
    Abstract Base Class for document parsers.

    Each concrete parser implementation must provide a 'parse' method
    that takes a file path and returns its text content as a string.
    """

    @abstractmethod
    def parse(self, filepath: str) -> str:
        """
        Parses the document at the given filepath.

        Args:
            filepath (str): The path to the document file.

        Returns:
            str: The extracted text content of the document.

        Raises:
            FileNotFoundError: If the file does not exist.
            Exception: For any other parsing-related errors.
        """
        pass
