"""Tests for the JSDoc utils module."""

import unittest
from jsdoc_parser.utils import extract_type_info, merge_jsdoc_objects, remove_jsdoc_component


class TestJSDocUtils(unittest.TestCase):
    """Test cases for the JSDoc utilities."""

    def test_extract_type_info_simple(self):
        """Test extracting simple type information."""
        result = extract_type_info('string')
        self.assertEqual(result['name'], 'string')
    
    def test_extract_type_info_union(self):
        """Test extracting union type information."""
        result = extract_type_info('string|number')
        self.assertEqual(result['union'], ['string', 'number'])
    
    def test_extract_type_info_generic(self):
        """Test extracting generic type information."""
        result = extract_type_info('Array<string>')
        self.assertEqual(result['name'], 'Array')
        self.assertEqual(result['params'], ['string'])
    
    def test_extract_type_info_complex(self):
        """Test extracting complex type information."""
        result = extract_type_info('Object<string, number>')
        self.assertEqual(result['name'], 'Object')
        self.assertEqual(result['params'], ['string', 'number'])
    
    def test_extract_type_info_nested(self):
        """Test extracting nested generic type information."""
        result = extract_type_info('Promise<Array<string>>')
        self.assertEqual(result['name'], 'Promise')
        self.assertEqual(result['params'], ['Array<string>'])
    
    def test_merge_jsdoc_objects_simple(self):
        """Test merging simple JSDoc objects."""
        base = {'description': 'Base description'}
        overlay = {'description': 'Overlay description'}
        
        result = merge_jsdoc_objects(base, overlay)
        self.assertEqual(result['description'], 'Overlay description')
    
    def test_merge_jsdoc_objects_params(self):
        """Test merging JSDoc objects with params."""
        base = {
            'description': 'Base description',
            'params': [
                {'name': 'a', 'type': 'string', 'description': 'Parameter A'}
            ]
        }
        
        overlay = {
            'description': 'Overlay description',
            'params': [
                {'name': 'a', 'description': 'Updated parameter A'},
                {'name': 'b', 'type': 'number', 'description': 'Parameter B'}
            ]
        }
        
        result = merge_jsdoc_objects(base, overlay)
        
        self.assertEqual(result['description'], 'Overlay description')
        self.assertEqual(len(result['params']), 2)
        
        # Check that parameter A was updated
        self.assertEqual(result['params'][0]['name'], 'a')
        self.assertEqual(result['params'][0]['type'], 'string')  # Preserved from base
        self.assertEqual(result['params'][0]['description'], 'Updated parameter A')
        
        # Check that parameter B was added
        self.assertEqual(result['params'][1]['name'], 'b')
        self.assertEqual(result['params'][1]['type'], 'number')
        self.assertEqual(result['params'][1]['description'], 'Parameter B')
    
    def test_merge_jsdoc_objects_complex(self):
        """Test merging complex JSDoc objects."""
        base = {
            'description': 'Base description',
            'params': [
                {'name': 'a', 'type': 'string', 'description': 'Parameter A'}
            ],
            'returns': {'type': 'boolean', 'description': 'Base return'},
            'throws': [{'type': 'Error', 'description': 'Base error'}],
            'examples': ['Base example'],
            'tags': {'since': ['v1.0.0']}
        }
        
        overlay = {
            'description': 'Overlay description',
            'returns': {'type': 'number', 'description': 'Overlay return'},
            'throws': [{'type': 'TypeError', 'description': 'Overlay error'}],
            'examples': ['Overlay example'],
            'tags': {'deprecated': ['Use new function']}
        }
        
        result = merge_jsdoc_objects(base, overlay)
        
        self.assertEqual(result['description'], 'Overlay description')
        self.assertEqual(len(result['params']), 1)  # Preserved from base
        
        self.assertEqual(result['returns']['type'], 'number')
        self.assertEqual(result['returns']['description'], 'Overlay return')
        
        self.assertEqual(len(result['throws']), 2)
        self.assertEqual(result['throws'][0]['type'], 'Error')
        self.assertEqual(result['throws'][1]['type'], 'TypeError')
        
        self.assertEqual(len(result['examples']), 2)
        self.assertEqual(result['examples'][0], 'Base example')
        self.assertEqual(result['examples'][1], 'Overlay example')
        
        self.assertEqual(len(result['tags']), 2)
        self.assertEqual(result['tags']['since'][0], 'v1.0.0')
        self.assertEqual(result['tags']['deprecated'][0], 'Use new function')
    
    def test_remove_jsdoc_component_description(self):
        """Test removing a description from a JSDoc object."""
        jsdoc = {
            'description': 'Test description',
            'params': [{'name': 'a', 'type': 'string', 'description': 'Parameter A'}]
        }
        
        result = remove_jsdoc_component(jsdoc, 'description')
        self.assertNotIn('description', result)
        self.assertIn('params', result)
    
    def test_remove_jsdoc_component_param(self):
        """Test removing a parameter from a JSDoc object."""
        jsdoc = {
            'description': 'Test description',
            'params': [
                {'name': 'a', 'type': 'string', 'description': 'Parameter A'},
                {'name': 'b', 'type': 'number', 'description': 'Parameter B'}
            ]
        }
        
        result = remove_jsdoc_component(jsdoc, 'param', 'a')
        self.assertIn('description', result)
        self.assertEqual(len(result['params']), 1)
        self.assertEqual(result['params'][0]['name'], 'b')
    
    def test_remove_jsdoc_component_returns(self):
        """Test removing returns from a JSDoc object."""
        jsdoc = {
            'description': 'Test description',
            'returns': {'type': 'boolean', 'description': 'Test return'}
        }
        
        result = remove_jsdoc_component(jsdoc, 'returns')
        self.assertIn('description', result)
        self.assertNotIn('returns', result)
    
    def test_remove_jsdoc_component_throws(self):
        """Test removing throws from a JSDoc object."""
        jsdoc = {
            'description': 'Test description',
            'throws': [
                {'type': 'Error', 'description': 'Error 1'},
                {'type': 'TypeError', 'description': 'Error 2'}
            ]
        }
        
        # Remove specific throws
        result = remove_jsdoc_component(jsdoc, 'throws', 'TypeError')
        self.assertIn('throws', result)
        self.assertEqual(len(result['throws']), 1)
        self.assertEqual(result['throws'][0]['type'], 'Error')
        
        # Remove all throws
        result = remove_jsdoc_component(jsdoc, 'throws')
        self.assertNotIn('throws', result)
    
    def test_remove_jsdoc_component_example(self):
        """Test removing examples from a JSDoc object."""
        # Test removing by index
        jsdoc1 = {
            'description': 'Test description',
            'examples': ['Example 1', 'Example 2 with specific content', 'Example 3']
        }
        result1 = remove_jsdoc_component(jsdoc1, 'example', '0')
        self.assertEqual(len(result1['examples']), 2)
        self.assertEqual(result1['examples'][0], 'Example 2 with specific content')
        
        # Test removing by content match
        jsdoc2 = {
            'description': 'Test description',
            'examples': ['Example 1', 'Example 2 with specific content', 'Example 3']
        }
        result2 = remove_jsdoc_component(jsdoc2, 'example', 'specific')
        self.assertEqual(len(result2['examples']), 2)
        self.assertEqual(result2['examples'][0], 'Example 1')
        self.assertEqual(result2['examples'][1], 'Example 3')
        
        # Test removing all examples
        jsdoc3 = {
            'description': 'Test description',
            'examples': ['Example 1', 'Example 2 with specific content', 'Example 3']
        }
        result3 = remove_jsdoc_component(jsdoc3, 'example')
        self.assertNotIn('examples', result3)
    
    def test_remove_jsdoc_component_tag(self):
        """Test removing tags from a JSDoc object."""
        jsdoc = {
            'description': 'Test description',
            'tags': {
                'since': ['v1.0.0'],
                'deprecated': ['Use new function']
            }
        }
        
        result = remove_jsdoc_component(jsdoc, 'tag', 'since')
        self.assertIn('tags', result)
        self.assertNotIn('since', result['tags'])
        self.assertIn('deprecated', result['tags'])
        
        # Remove the last tag
        result = remove_jsdoc_component(result, 'tag', 'deprecated')
        self.assertNotIn('tags', result)


if __name__ == '__main__':
    unittest.main()
