"""CLI interface for ${project_name}."""

import argparse
import sys


def main(args=None):
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="${project_name}",
        description="${description}"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    # Add your subcommands or arguments here
    # parser.add_argument("input", help="Input file")
    
    parsed = parser.parse_args(args)
    
    if parsed.verbose:
        print("Verbose mode enabled")
    
    # Your main logic here
    print(f"${project_name} running...")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
