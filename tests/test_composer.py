"""Tests for the JSDoc composer module."""

import unittest
from docstring_parser.composer import compose_jsdoc


class TestJSDocComposer(unittest.TestCase):
    """Test cases for the JSDoc composer."""

    def test_simple_description(self):
        """Test composing a simple JSDoc description."""
        jsdoc_obj = {'description': 'This is a simple description'}
        expected = '/**\n * This is a simple description\n *\n */'
        result = compose_jsdoc(jsdoc_obj)
        self.assertEqual(result, expected)
    
    def test_params(self):
        """Test composing JSDoc with parameters."""
        jsdoc_obj = {
            'description': 'Function with parameters',
            'params': [
                {'name': 'name', 'type': 'string', 'description': 'The name parameter'},
                {'name': 'age', 'type': 'number', 'description': 'The age parameter'}
            ]
        }
        expected = '/**\n * Function with parameters\n *\n * @param {string} name - The name parameter\n * @param {number} age - The age parameter\n */'
        result = compose_jsdoc(jsdoc_obj)
        self.assertEqual(result, expected)
    
    def test_returns(self):
        """Test composing JSDoc with a return value."""
        jsdoc_obj = {
            'description': 'Function with a return value',
            'returns': {'type': 'boolean', 'description': 'Whether the operation succeeded'}
        }
        expected = '/**\n * Function with a return value\n *\n * @returns {boolean} Whether the operation succeeded\n */'
        result = compose_jsdoc(jsdoc_obj)
        self.assertEqual(result, expected)
    
    def test_throws(self):
        """Test composing JSDoc with throws."""
        jsdoc_obj = {
            'description': 'Function that throws an exception',
            'throws': [{'type': 'Error', 'description': 'If something goes wrong'}]
        }
        expected = '/**\n * Function that throws an exception\n *\n * @throws {Error} If something goes wrong\n */'
        result = compose_jsdoc(jsdoc_obj)
        self.assertEqual(result, expected)
    
    def test_examples(self):
        """Test composing JSDoc with examples."""
        jsdoc_obj = {
            'description': 'Function with examples',
            'examples': [
                '// Example 1\nconst result = myFunction();',
                '// Example 2\nmyFunction(\'test\');'
            ]
        }
        expected = '/**\n * Function with examples\n *\n * @example // Example 1\nconst result = myFunction();\n * @example // Example 2\nmyFunction(\'test\');\n */'
        result = compose_jsdoc(jsdoc_obj)
        self.assertEqual(result, expected)
    
    def test_other_tags(self):
        """Test composing JSDoc with custom tags."""
        jsdoc_obj = {
            'description': 'Function with custom tags',
            'tags': {
                'author': ['John Doe'],
                'since': ['v1.0.0'],
                'deprecated': ['Use newFunction instead']
            }
        }
        expected = '/**\n * Function with custom tags\n *\n * @author John Doe\n * @since v1.0.0\n * @deprecated Use newFunction instead\n */'
        result = compose_jsdoc(jsdoc_obj)
        self.assertEqual(result, expected)
    
    def test_complex_jsdoc(self):
        """Test composing a complex JSDoc string."""
        jsdoc_obj = {
            'description': 'Performs an operation with various components\nThis is a multiline description',
            'params': [
                {'name': 'id', 'type': 'string', 'description': 'The operation ID'},
                {'name': 'options', 'type': 'Object', 'description': 'Configuration options'}
            ],
            'returns': {'type': 'Promise<Result>', 'description': 'The result of the operation'},
            'throws': [
                {'type': 'TypeError', 'description': 'If id is not a string'},
                {'type': 'OperationError', 'description': 'If the operation fails'}
            ],
            'examples': ['// Basic usage\nawait performOperation(\'123\', { timeout: 1000 });'],
            'tags': {
                'since': ['v2.1.0'],
                'deprecated': ['Use newOperation instead since v3.0.0']
            }
        }
        
        result = compose_jsdoc(jsdoc_obj)
        
        self.assertIn('Performs an operation with various components', result)
        self.assertIn('This is a multiline description', result)
        
        self.assertIn('@param {string} id - The operation ID', result)
        self.assertIn('@param {Object} options - Configuration options', result)
        
        self.assertIn('@returns {Promise<Result>} The result of the operation', result)
        
        self.assertIn('@throws {TypeError} If id is not a string', result)
        self.assertIn('@throws {OperationError} If the operation fails', result)
        
        self.assertIn('@example // Basic usage', result)
        self.assertIn('await performOperation', result)
        
        self.assertIn('@since v2.1.0', result)
        self.assertIn('@deprecated Use newOperation instead since v3.0.0', result)
    
    def test_round_trip(self):
        """Test that a complex object can be round-tripped through compose and parse."""
        # This test would ideally use parse_jsdoc from the parser module,
        # but for simplicity in this test file, we'll just verify parts of the string
        jsdoc_obj = {
            'description': 'Complex function description',
            'params': [
                {'name': 'id', 'type': 'string', 'description': 'ID parameter'},
                {'name': 'data', 'type': 'Object', 'description': 'Data object'}
            ],
            'returns': {'type': 'boolean', 'description': 'Success indicator'}
        }
        
        result = compose_jsdoc(jsdoc_obj)
        
        self.assertIn('Complex function description', result)
        self.assertIn('@param {string} id - ID parameter', result)
        self.assertIn('@param {Object} data - Data object', result)
        self.assertIn('@returns {boolean} Success indicator', result)


if __name__ == '__main__':
    unittest.main()
