"""
CLI entry point for the GenomicStudy Parser.

Usage:
    python -m src path/to/study.json
    python -m src study.json --api-link https://fhir.example.org/r5 --pretty
"""
import argparse
import json
import sys

from parser import Genomic_Study_Parser


def main():
    arg_parser = argparse.ArgumentParser(
        description='Parse FHIR R5 GenomicStudy resources and extract file references.'
    )
    arg_parser.add_argument(
        'input_file',
        help='Path to the GenomicStudy JSON file'
    )
    arg_parser.add_argument(
        '--api-link',
        help='Base API URL to prepend to file references'
    )
    arg_parser.add_argument(
        '--output', '-o',
        help='Output file path (default: stdout)'
    )
    arg_parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty print JSON output'
    )

    args = arg_parser.parse_args()

    parser = Genomic_Study_Parser()
    try:
        files = parser.parse_genomic_study(args.input_file, api_link=args.api_link)
    except FileNotFoundError:
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    indent = 2 if args.pretty else None
    output = json.dumps(files, indent=indent)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Output written to {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
