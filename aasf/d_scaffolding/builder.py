# aasf/d_scaffolding/builder.py

import os
import json
import logging
from typing import List, Dict
from jinja2 import Environment, FileSystemLoader
from ..c_extraction.models import AgentDefinition

logger = logging.getLogger("AASF.Builder")


class ScaffoldingBuilder:
    """Builds output files (code, config) from agent definitions."""

    def __init__(self, config: Dict):
        self.output_dir = config.get('output_directory', 'generated_agents')
        self.templates_config = config.get('templates', [])

        # Set up Jinja2 environment to look for templates in a 'templates' folder
        template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
        logger.debug(f"ScaffoldingBuilder initialized. Output dir: '{self.output_dir}'")

    def build_all(self, agents: List[AgentDefinition]):
        """
        Generates all configured files for a list of agents.

        Args:
            agents (List[AgentDefinition]): The list of extracted agent models.
        """
        logger.info(f"Starting scaffolding process for {len(agents)} agents.")
        os.makedirs(self.output_dir, exist_ok=True)

        for agent in agents:
            logger.info(f"--- Scaffolding files for agent: {agent.agent_id} ---")
            for template_cfg in self.templates_config:
                self._generate_file(agent, template_cfg)

    def _generate_file(self, agent: AgentDefinition, template_cfg: Dict):
        """Generates a single output file for an agent."""
        try:
            # Render the output filename from a template string
            filename_template = self.jinja_env.from_string(template_cfg['output_filename_template'])
            output_filename = filename_template.render(agent=agent)
            output_path = os.path.join(self.output_dir, output_filename)

            # Check if a Jinja template is used or if it's a direct JSON dump
            if template_cfg['template_file']:
                template = self.jinja_env.get_template(template_cfg['template_file'])
                content = template.render(agent=agent)
            else:  # Direct JSON dump
                content = agent.json(indent=4)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"  -> Successfully created {output_path}")

        except Exception as e:
            logger.error(f"  -> FAILED to generate file for agent {agent.agent_id} "
                         f"using template config '{template_cfg.get('name')}': {e}")