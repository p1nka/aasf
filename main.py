import argparse
import yaml
import logging

from aasf.orchestrator import Orchestrator
from aasf.logger_config import setup_logging


def main():
    """Main entry point for the AASF command-line application."""
    parser = argparse.ArgumentParser(description="Automated Agent Scaffolding Framework (AASF)")
    parser.add_argument("rulebook_file", type=str, help="Path to the rulebook/specification file.")
    parser.add_argument(
        "-c", "--config",
        type=str,
        default="config.yaml",
        help="Path to the configuration file (default: config.yaml)"
    )

    args = parser.parse_args()

    # Load configuration
    try:
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{args.config}'")
        return
    except yaml.YAMLError as e:
        print(f"Error parsing YAML configuration: {e}")
        return

    # Setup logging
    logger = setup_logging(config.get("log_level", "INFO"))

    # Initialize and run the orchestrator
    orchestrator = Orchestrator(config)
    orchestrator.run(args.rulebook_file)


if __name__ == "__main__":
    main()