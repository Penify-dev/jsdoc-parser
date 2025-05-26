#!/usr/bin/env python
"""
Command-line interface for the JSDoc parser library.

This script provides a simple command-line interface for parsing and composing JSDoc strings.
"""

import argparse
import json
import sys
from docstring_parser.parser import parse_jsdoc
from docstring_parser.composer import compose_jsdoc
from docstring_parser.utils import remove_jsdoc_component


def main():
    """Entry point for the command-line interface."""
    parser = argparse.ArgumentParser(description='Parse and compose JSDoc strings')
    subparsers = parser.add_subparsers(dest='command', required=True, help='Command to execute')
    
    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse a JSDoc string into a JSON object')
    parse_parser.add_argument('file', type=str, nargs='?', help='File containing a JSDoc string (or use stdin)')
    parse_parser.add_argument('-o', '--output', type=str, help='Output file (default: stdout)')
    
    # Compose command
    compose_parser = subparsers.add_parser('compose', help='Compose a JSDoc string from a JSON object')
    compose_parser.add_argument('file', type=str, nargs='?', help='JSON file containing a JSDoc object (or use stdin)')
    compose_parser.add_argument('-o', '--output', type=str, help='Output file (default: stdout)')
    
    # Remove component command
    remove_parser = subparsers.add_parser('remove', help='Remove a component from a JSDoc object')
    remove_parser.add_argument('file', type=str, nargs='?', help='JSON file containing a JSDoc object (or use stdin)')
    remove_parser.add_argument('-t', '--type', type=str, required=True,
                           choices=['description', 'param', 'returns', 'throws', 'example', 'tag'],
                           help='Type of component to remove')
    remove_parser.add_argument('-i', '--identifier', type=str,
                           help='Identifier of the component (e.g., param name, tag name)')
    remove_parser.add_argument('-o', '--output', type=str, help='Output file (default: stdout)')
    remove_parser.add_argument('-f', '--format', type=str, choices=['json', 'jsdoc'], default='json',
                            help='Output format: json or jsdoc (default: json)')
    
    args = parser.parse_args()
    
    # Handle input
    input_data = ''
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            input_data = f.read()
    else:
        input_data = sys.stdin.read()
    
    # Process commands
    if args.command == 'parse':
        try:
            result = parse_jsdoc(input_data)
            output = json.dumps(result, indent=2)
        except Exception as e:
            print(f"Error parsing JSDoc: {str(e)}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'compose':
        try:
            jsdoc_obj = json.loads(input_data)
            output = compose_jsdoc(jsdoc_obj)
        except json.JSONDecodeError:
            print("Error: Input is not valid JSON", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error composing JSDoc: {str(e)}", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'remove':
        try:
            jsdoc_obj = json.loads(input_data)
            result = remove_jsdoc_component(jsdoc_obj, args.type, args.identifier)
            
            if args.format == 'json':
                output = json.dumps(result, indent=2)
            else:  # jsdoc format
                output = compose_jsdoc(result)
        except json.JSONDecodeError:
            print("Error: Input is not valid JSON", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error removing component: {str(e)}", file=sys.stderr)
            sys.exit(1)
    
    # Handle output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
    else:
        print(output)


if __name__ == '__main__':
    main()
