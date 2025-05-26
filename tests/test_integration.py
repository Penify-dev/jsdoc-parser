"""Integration tests for the JSDoc parser and composer."""

import unittest
from docstring_parser.parser import parse_jsdoc
from docstring_parser.composer import compose_jsdoc


class TestJSDocIntegration(unittest.TestCase):
    """Integration test cases for the JSDoc parser and composer."""

    def test_round_trip_simple(self):
        """Test round-trip parsing and composing of a simple JSDoc."""
        original = """/**
 * This is a simple description
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        
        # The composed JSDoc might have slightly different formatting
        # but should contain the same content
        self.assertIn('This is a simple description', composed)
        
        # Parse the composed JSDoc again to check content equality
        reparsed = parse_jsdoc(composed)
        self.assertEqual(parsed['description'], reparsed['description'])
    
    def test_round_trip_complex(self):
        """Test round-trip parsing and composing of a complex JSDoc."""
        original = """/**
 * Calculates the sum of two numbers
 * 
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} The sum of a and b
 * @throws {TypeError} If a or b are not numbers
 * @example
 * add(1, 2); // returns 3
 * @since v1.0.0
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        # Verify that the essential content is preserved
        self.assertEqual(parsed['description'], reparsed['description'])
        self.assertEqual(len(parsed['params']), len(reparsed['params']))
        
        for i in range(len(parsed['params'])):
            self.assertEqual(parsed['params'][i]['name'], reparsed['params'][i]['name'])
            self.assertEqual(parsed['params'][i]['type'], reparsed['params'][i]['type'])
            self.assertEqual(parsed['params'][i]['description'], reparsed['params'][i]['description'])
        
        self.assertEqual(parsed['returns']['type'], reparsed['returns']['type'])
        self.assertEqual(parsed['returns']['description'], reparsed['returns']['description'])
        
        self.assertEqual(len(parsed['throws']), len(reparsed['throws']))
        self.assertEqual(parsed['throws'][0]['type'], reparsed['throws'][0]['type'])
        self.assertEqual(parsed['throws'][0]['description'], reparsed['throws'][0]['description'])
        
        self.assertEqual(len(parsed['examples']), len(reparsed['examples']))
        self.assertTrue(any('add(1, 2)' in ex for ex in reparsed['examples']))
        
        self.assertEqual(len(parsed['tags']['since']), len(reparsed['tags']['since']))
        self.assertEqual(parsed['tags']['since'][0], reparsed['tags']['since'][0])
    
    def test_manipulation(self):
        """Test manipulating a parsed JSDoc object and then recomposing it."""
        original = """/**
 * Calculates the sum of two numbers
 * 
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} The sum of a and b
 */"""
        
        # Parse the original JSDoc
        parsed = parse_jsdoc(original)
        
        # Manipulate the parsed object
        parsed['description'] = 'Modified function description'
        parsed['params'][0]['description'] = 'Modified first parameter description'
        parsed['returns']['description'] = 'Modified return description'
        
        # Add a new parameter
        parsed['params'].append({
            'name': 'c',
            'type': 'number',
            'description': 'Third number (optional)'
        })
        
        # Add a throws tag
        if 'throws' not in parsed:
            parsed['throws'] = []
        parsed['throws'].append({
            'type': 'TypeError',
            'description': 'If parameters are not numbers'
        })
        
        # Compose the modified object
        composed = compose_jsdoc(parsed)
        
        # Verify that the modifications are present in the composed string
        self.assertIn('Modified function description', composed)
        self.assertIn('Modified first parameter description', composed)
        self.assertIn('Modified return description', composed)
        self.assertIn('@param {number} c - Third number (optional)', composed)
        self.assertIn('@throws {TypeError} If parameters are not numbers', composed)
        
        # Parse the composed string again to verify structural correctness
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(reparsed['description'], 'Modified function description')
        self.assertEqual(len(reparsed['params']), 3)
        self.assertEqual(reparsed['params'][0]['description'], 'Modified first parameter description')
        self.assertEqual(reparsed['params'][2]['name'], 'c')
        self.assertEqual(reparsed['returns']['description'], 'Modified return description')
        self.assertEqual(len(reparsed['throws']), 1)
        self.assertEqual(reparsed['throws'][0]['type'], 'TypeError')


if __name__ == '__main__':
    unittest.main()
