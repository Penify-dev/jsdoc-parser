"""Tests for the JSDoc parser module."""

import unittest
from docstring_parser.parser import parse_jsdoc


class TestJSDocParser(unittest.TestCase):
    """Test cases for the JSDoc parser."""

    def test_simple_description(self):
        """Test parsing a simple JSDoc description."""
        jsdoc = """/**
 * This is a simple description
 */"""
        result = parse_jsdoc(jsdoc)
        self.assertEqual(result['description'], 'This is a simple description')
        self.assertNotIn('params', result)
    
    def test_params(self):
        """Test parsing JSDoc with parameters."""
        jsdoc = """/**
 * Function with parameters
 * @param {string} name - The name parameter
 * @param {number} age - The age parameter
 */"""
        result = parse_jsdoc(jsdoc)
        self.assertEqual(result['description'], 'Function with parameters')
        self.assertEqual(len(result['params']), 2)
        self.assertEqual(result['params'][0]['name'], 'name')
        self.assertEqual(result['params'][0]['type'], 'string')
        self.assertEqual(result['params'][0]['description'], 'The name parameter')
        self.assertEqual(result['params'][1]['name'], 'age')
        self.assertEqual(result['params'][1]['type'], 'number')
        self.assertEqual(result['params'][1]['description'], 'The age parameter')
    
    def test_returns(self):
        """Test parsing JSDoc with a return value."""
        jsdoc = """/**
 * Function with a return value
 * @returns {boolean} Whether the operation succeeded
 */"""
        result = parse_jsdoc(jsdoc)
        self.assertEqual(result['description'], 'Function with a return value')
        self.assertEqual(result['returns']['type'], 'boolean')
        self.assertEqual(result['returns']['description'], 'Whether the operation succeeded')
    
    def test_throws(self):
        """Test parsing JSDoc with throws."""
        jsdoc = """/**
 * Function that throws an exception
 * @throws {Error} If something goes wrong
 */"""
        result = parse_jsdoc(jsdoc)
        self.assertEqual(result['description'], 'Function that throws an exception')
        self.assertEqual(len(result['throws']), 1)
        self.assertEqual(result['throws'][0]['type'], 'Error')
        self.assertEqual(result['throws'][0]['description'], 'If something goes wrong')
    
    def test_examples(self):
        """Test parsing JSDoc with examples."""
        jsdoc = """/**
 * Function with examples
 * @example
 * // Example 1
 * const result = myFunction();
 * @example
 * // Example 2
 * myFunction('test');
 */"""
        result = parse_jsdoc(jsdoc)
        self.assertEqual(result['description'], 'Function with examples')
        self.assertEqual(len(result['examples']), 2)
        self.assertIn('// Example 1', result['examples'][0])
        self.assertIn('// Example 2', result['examples'][1])
    
    def test_other_tags(self):
        """Test parsing JSDoc with custom tags."""
        jsdoc = """/**
 * Function with custom tags
 * @author John Doe
 * @since v1.0.0
 * @deprecated Use newFunction instead
 */"""
        result = parse_jsdoc(jsdoc)
        self.assertEqual(result['description'], 'Function with custom tags')
        self.assertEqual(len(result['tags']['author']), 1)
        self.assertEqual(result['tags']['author'][0], 'John Doe')
        self.assertEqual(result['tags']['since'][0], 'v1.0.0')
        self.assertEqual(result['tags']['deprecated'][0], 'Use newFunction instead')
    
    def test_complex_jsdoc(self):
        """Test parsing a complex JSDoc string."""
        jsdoc = """/**
 * Performs an operation with various components
 * This is a multiline description
 * 
 * @param {string} id - The operation ID
 * @param {Object} options - Configuration options
 * @param {number} options.timeout - Timeout in milliseconds
 * @param {boolean} [options.silent=false] - Run in silent mode
 * @returns {Promise<Result>} The result of the operation
 * @throws {TypeError} If id is not a string
 * @throws {OperationError} If the operation fails
 * @example
 * // Basic usage
 * await performOperation('123', { timeout: 1000 });
 * @since v2.1.0
 * @deprecated Use newOperation instead since v3.0.0
 */"""
        result = parse_jsdoc(jsdoc)
        
        self.assertIn('Performs an operation with various components', result['description'])
        self.assertIn('This is a multiline description', result['description'])
        
        self.assertEqual(len(result['params']), 2)
        self.assertEqual(result['params'][0]['name'], 'id')
        self.assertEqual(result['params'][1]['name'], 'options')
        # Check nested parameters
        self.assertIn('properties', result['params'][1])
        self.assertEqual(len(result['params'][1]['properties']), 2)
        self.assertEqual(result['params'][1]['properties'][0]['name'], 'timeout')
        self.assertEqual(result['params'][1]['properties'][0]['type'], 'number')
        self.assertEqual(result['params'][1]['properties'][1]['name'], 'silent')
        self.assertEqual(result['params'][1]['properties'][1]['type'], 'boolean')
        
        self.assertEqual(result['returns']['type'], 'Promise<Result>')
        
        self.assertEqual(len(result['throws']), 2)
        self.assertEqual(result['throws'][0]['type'], 'TypeError')
        self.assertEqual(result['throws'][1]['type'], 'OperationError')
        
        self.assertEqual(len(result['examples']), 1)
        self.assertIn('Basic usage', result['examples'][0])
        
        self.assertEqual(len(result['tags']['since']), 1)
        self.assertEqual(result['tags']['since'][0], 'v2.1.0')
        
        self.assertEqual(len(result['tags']['deprecated']), 1)
        self.assertEqual(result['tags']['deprecated'][0], 'Use newOperation instead since v3.0.0')


if __name__ == '__main__':
    unittest.main()
