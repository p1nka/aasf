# aasf/orchestrator.py

import os
import logging
from typing import Dict, List
from .a_ingestion.base_parser import BaseParser
from .a_ingestion.text_parser import TextParser
from .a_ingestion.pdf_parser import PdfParser
from .b_discovery.section_finder import SectionFinder
from .c_extraction.extractor import AgentExtractor
from .c_extraction.models import AgentDefinition
from .d_scaffolding.builder import ScaffoldingBuilder

logger = logging.getLogger("AASF.Orchestrator")


class Orchestrator:
    """Orchestrates the entire agent scaffolding pipeline."""

    def __init__(self, config: Dict):
        self.config = config
        self.parser_factory = self._init_parser_factory()
        self.finder = SectionFinder(config.get('discovery_settings', {}))
        self.extractor = AgentExtractor(config.get('extraction_settings', {}))
        self.builder = ScaffoldingBuilder(config.get('scaffolding_settings', {}))

    def _init_parser_factory(self) -> Dict[str, BaseParser]:
        """Initializes a mapping of file extensions to parser instances."""
        # This factory pattern makes it easy to add new parsers
        return {
            ".txt": TextParser(),
            ".pdf": PdfParser(),
        }

    def _get_parser(self, filepath: str) -> BaseParser:
        """Selects the correct parser based on file extension."""
        ext = os.path.splitext(filepath)[1].lower()
        parser = self.parser_factory.get(ext)
        if not parser:
            raise NotImplementedError(f"No parser implemented for file type '{ext}'")
        return parser

    def run(self, input_filepath: str):
        """
        Executes the full AASF pipeline from ingestion to scaffolding.

        Args:
            input_filepath (str): The path to the source rulebook document.
        """
        logger.info("===== AASF Pipeline Started =====")

        try:
            # 1. Ingestion (with dynamic parser selection)
            parser = self._get_parser(input_filepath)
            content = parser.parse(input_filepath)

            # 2. Discovery
            sections = self.finder.find_sections(content)

            # 3. Extraction
            extracted_agents: List[AgentDefinition] = []
            for section in sections:
                agent_def = self.extractor.extract(section)
                if agent_def:
                    extracted_agents.append(agent_def)

            if not extracted_agents:
                logger.warning("Pipeline finished, but no valid agent definitions were extracted.")
                return

            logger.info(f"Successfully extracted definitions for {len(extracted_agents)} agents.")

            # 4. Scaffolding
            self.builder.build_all(extracted_agents)

            logger.info("===== AASF Pipeline Finished Successfully =====")

        except FileNotFoundError:
            logger.critical(f"Input file not found: {input_filepath}")
        except NotImplementedError as e:
            logger.critical(str(e))
        except Exception as e:
            logger.critical(f"An unexpected error occurred during the pipeline execution: {e}", exc_info=True)