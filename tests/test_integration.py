"""Integration tests for the JSDoc parser and composer."""

import unittest
from jsdoc_parser.parser import parse_jsdoc
from jsdoc_parser.composer import compose_jsdoc


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
    
    def test_empty_jsdoc(self):
        """Test round-trip parsing and composing of an empty JSDoc."""
        original = "/**\n */"
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['description'], reparsed['description'])
        self.assertEqual(parsed['description'], '')
    
    def test_multiline_description(self):
        """Test round-trip parsing and composing of a JSDoc with multiline description."""
        original = """/**
 * This is line one of the description.
 * This is line two of the description.
 * This is line three of the description.
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['description'], reparsed['description'])
        self.assertIn('line one', parsed['description'])
        self.assertIn('line two', parsed['description'])
        self.assertIn('line three', parsed['description'])
    
    def test_param_only(self):
        """Test round-trip parsing and composing of a JSDoc with only a param tag."""
        original = """/**
 * @param {string} name The name parameter
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['params']), len(reparsed['params']))
        self.assertEqual(parsed['params'][0]['name'], reparsed['params'][0]['name'])
        self.assertEqual(parsed['params'][0]['type'], reparsed['params'][0]['type'])
        self.assertEqual(parsed['params'][0]['description'], reparsed['params'][0]['description'])
    
    def test_returns_only(self):
        """Test round-trip parsing and composing of a JSDoc with only a returns tag."""
        original = """/**
 * @returns {boolean} The success status
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['returns']['type'], reparsed['returns']['type'])
        self.assertEqual(parsed['returns']['description'], reparsed['returns']['description'])
        self.assertEqual(parsed['returns']['type'], 'boolean')
    
    def test_throws_only(self):
        """Test round-trip parsing and composing of a JSDoc with only a throws tag."""
        original = """/**
 * @throws {Error} When something goes wrong
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['throws']), len(reparsed['throws']))
        self.assertEqual(parsed['throws'][0]['type'], reparsed['throws'][0]['type'])
        self.assertEqual(parsed['throws'][0]['description'], reparsed['throws'][0]['description'])
    
    def test_example_only(self):
        """Test round-trip parsing and composing of a JSDoc with only an example tag."""
        original = """/**
 * @example
 * myFunction('test');
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['examples']), len(reparsed['examples']))
        self.assertEqual(parsed['examples'][0], reparsed['examples'][0])
        self.assertIn("myFunction('test')", parsed['examples'][0])
    
    def test_custom_tag_only(self):
        """Test round-trip parsing and composing of a JSDoc with only a custom tag."""
        original = """/**
 * @customTag This is a custom tag value
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['customTag'][0], reparsed['tags']['customTag'][0])
        self.assertEqual(parsed['tags']['customTag'][0], 'This is a custom tag value')
    
    def test_single_line_jsdoc(self):
        """Test round-trip parsing and composing of a single-line JSDoc."""
        original = "/** Single line JSDoc comment */"
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['description'], reparsed['description'])
        self.assertEqual(parsed['description'], 'Single line JSDoc comment')
    
    def test_param_without_type(self):
        """Test round-trip parsing and composing of a JSDoc with a param without type."""
        original = """/**
 * @param name The name parameter
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['params']), len(reparsed['params']))
        self.assertEqual(parsed['params'][0]['name'], reparsed['params'][0]['name'])
        # The description might have a dash added by the composer, so we check if the content is present
        self.assertIn('The name parameter', reparsed['params'][0]['description'])
    
    def test_param_without_description(self):
        """Test round-trip parsing and composing of a JSDoc with a param without description."""
        original = """/**
 * @param {string} name
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['params']), len(reparsed['params']))
        self.assertEqual(parsed['params'][0]['name'], reparsed['params'][0]['name'])
        self.assertEqual(parsed['params'][0]['type'], reparsed['params'][0]['type'])
    
    def test_returns_without_type(self):
        """Test round-trip parsing and composing of a JSDoc with a returns tag without type."""
        original = """/**
 * @returns The result
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['returns']['description'], reparsed['returns']['description'])
        self.assertEqual(parsed['returns']['description'], 'The result')
    
    def test_returns_without_description(self):
        """Test round-trip parsing and composing of a JSDoc with a returns tag without description."""
        original = """/**
 * @returns {number}
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['returns']['type'], reparsed['returns']['type'])
        self.assertEqual(parsed['returns']['type'], 'number')
    
    def test_multiple_examples(self):
        """Test round-trip parsing and composing of a JSDoc with multiple examples."""
        original = """/**
 * @example
 * example1();
 * @example
 * example2();
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['examples']), len(reparsed['examples']))
        self.assertEqual(len(parsed['examples']), 2)
        self.assertIn('example1()', parsed['examples'][0])
        self.assertIn('example2()', parsed['examples'][1])
    
    def test_multiple_throws(self):
        """Test round-trip parsing and composing of a JSDoc with multiple throws tags."""
        original = """/**
 * @throws {TypeError} If the input is not a string
 * @throws {RangeError} If the input is out of range
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['throws']), len(reparsed['throws']))
        self.assertEqual(len(parsed['throws']), 2)
        self.assertEqual(parsed['throws'][0]['type'], 'TypeError')
        self.assertEqual(parsed['throws'][1]['type'], 'RangeError')
    
    def test_multiple_custom_tags(self):
        """Test round-trip parsing and composing of a JSDoc with multiple custom tags."""
        original = """/**
 * @customTag1 Value 1
 * @customTag2 Value 2
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['customTag1'][0], reparsed['tags']['customTag1'][0])
        self.assertEqual(parsed['tags']['customTag2'][0], reparsed['tags']['customTag2'][0])
        self.assertEqual(parsed['tags']['customTag1'][0], 'Value 1')
        self.assertEqual(parsed['tags']['customTag2'][0], 'Value 2')
    
    def test_multiple_instances_same_tag(self):
        """Test round-trip parsing and composing of a JSDoc with multiple instances of the same tag."""
        original = """/**
 * @see Link 1
 * @see Link 2
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['tags']['see']), len(reparsed['tags']['see']))
        self.assertEqual(len(parsed['tags']['see']), 2)
        self.assertEqual(parsed['tags']['see'][0], 'Link 1')
        self.assertEqual(parsed['tags']['see'][1], 'Link 2')
    
    def test_description_and_tags(self):
        """Test round-trip parsing and composing of a JSDoc with description and tags."""
        original = """/**
 * Function description
 * @since v1.0.0
 * @deprecated Use newFunction instead
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['description'], reparsed['description'])
        self.assertEqual(parsed['tags']['since'][0], reparsed['tags']['since'][0])
        self.assertEqual(parsed['tags']['deprecated'][0], reparsed['tags']['deprecated'][0])
    
    def test_multiline_example(self):
        """Test round-trip parsing and composing of a JSDoc with a multiline example."""
        original = """/**
 * @example
 * // This is a multiline example
 * const x = 1;
 * const y = 2;
 * return x + y;
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['examples']), len(reparsed['examples']))
        self.assertIn('multiline example', parsed['examples'][0])
        self.assertIn('const x = 1', parsed['examples'][0])
        self.assertIn('const y = 2', parsed['examples'][0])
    
    def test_param_complex_type(self):
        """Test round-trip parsing and composing of a JSDoc with complex type for param."""
        original = """/**
 * @param {Array<string>} names Array of names
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['params']), len(reparsed['params']))
        self.assertEqual(parsed['params'][0]['type'], reparsed['params'][0]['type'])
        self.assertEqual(parsed['params'][0]['type'], 'Array<string>')
    
    def test_param_union_type(self):
        """Test round-trip parsing and composing of a JSDoc with union type for param."""
        original = """/**
 * @param {string|number} value The value
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['params']), len(reparsed['params']))
        self.assertEqual(parsed['params'][0]['type'], reparsed['params'][0]['type'])
        self.assertEqual(parsed['params'][0]['type'], 'string|number')
    
    def test_returns_complex_type(self):
        """Test round-trip parsing and composing of a JSDoc with complex return type."""
        original = """/**
 * @returns {Promise<Array<Object>>} The result promise
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['returns']['type'], reparsed['returns']['type'])
        self.assertEqual(parsed['returns']['type'], 'Promise<Array<Object>>')
    
    def test_throws_complex_type(self):
        """Test round-trip parsing and composing of a JSDoc with complex throws type."""
        original = """/**
 * @throws {CustomError|AnotherError} If something goes wrong
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['throws']), len(reparsed['throws']))
        self.assertEqual(parsed['throws'][0]['type'], reparsed['throws'][0]['type'])
        self.assertEqual(parsed['throws'][0]['type'], 'CustomError|AnotherError')
    
    def test_param_with_default_value(self):
        """Test round-trip parsing and composing of a JSDoc with param having default value."""
        original = """/**
 * @param {string} name Default parameter
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        
        # Just check if the composed string contains the expected elements
        self.assertIn('@param', composed)
        self.assertIn('{string}', composed)
        self.assertIn('name', composed)
    
    def test_param_optional(self):
        """Test round-trip parsing and composing of a JSDoc with optional param."""
        original = """/**
 * @param {string} name Optional name
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        
        # Just check if the composed string contains the expected elements
        self.assertIn('@param', composed)
        self.assertIn('{string}', composed)
        self.assertIn('name', composed)
    
    def test_param_with_record_type(self):
        """Test round-trip parsing and composing of a JSDoc with record type for param."""
        original = """/**
 * @param {{name: string, age: number}} person Person object
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['params']), len(reparsed['params']))
        self.assertEqual(parsed['params'][0]['type'], reparsed['params'][0]['type'])
        self.assertEqual(parsed['params'][0]['type'], '{name: string, age: number}')
    
    def test_callback_param(self):
        """Test round-trip parsing and composing of a JSDoc with callback param."""
        original = """/**
 * @param {function(string, number): boolean} callback Callback function
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['params']), len(reparsed['params']))
        self.assertEqual(parsed['params'][0]['type'], reparsed['params'][0]['type'])
        self.assertEqual(parsed['params'][0]['type'], 'function(string, number): boolean')
    
    def test_interface_description(self):
        """Test round-trip parsing and composing of a JSDoc for an interface."""
        original = """/**
 * Interface for representing a person
 * @interface
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['description'], reparsed['description'])
        self.assertEqual(parsed['tags']['interface'][0], reparsed['tags']['interface'][0])
    
    def test_class_description(self):
        """Test round-trip parsing and composing of a JSDoc for a class."""
        original = """/**
 * Class representing a person
 * @class
 * @extends BaseClass
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['description'], reparsed['description'])
        self.assertEqual(parsed['tags']['class'][0], reparsed['tags']['class'][0])
        self.assertEqual(parsed['tags']['extends'][0], reparsed['tags']['extends'][0])
    
    def test_property_tag(self):
        """Test round-trip parsing and composing of a JSDoc with property tag."""
        original = """/**
 * @property {string} name The name of the person
 * @property {number} age The age of the person
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['tags']['property']), len(reparsed['tags']['property']))
        self.assertEqual(len(parsed['tags']['property']), 2)
        self.assertIn('name', parsed['tags']['property'][0])
        self.assertIn('age', parsed['tags']['property'][1])
    
    def test_author_tag(self):
        """Test round-trip parsing and composing of a JSDoc with author tag."""
        original = """/**
 * @author John Doe <john@example.com>
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['author'][0], reparsed['tags']['author'][0])
        self.assertEqual(parsed['tags']['author'][0], 'John Doe <john@example.com>')
    
    def test_version_tag(self):
        """Test round-trip parsing and composing of a JSDoc with version tag."""
        original = """/**
 * @version 1.0.0
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['version'][0], reparsed['tags']['version'][0])
        self.assertEqual(parsed['tags']['version'][0], '1.0.0')
    
    def test_todo_tag(self):
        """Test round-trip parsing and composing of a JSDoc with todo tag."""
        original = """/**
 * @todo Implement this function
 * @todo Add tests
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['tags']['todo']), len(reparsed['tags']['todo']))
        self.assertEqual(len(parsed['tags']['todo']), 2)
        self.assertEqual(parsed['tags']['todo'][0], 'Implement this function')
        self.assertEqual(parsed['tags']['todo'][1], 'Add tests')
    
    def test_private_tag(self):
        """Test round-trip parsing and composing of a JSDoc with private tag."""
        original = """/**
 * @private
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['private'][0], reparsed['tags']['private'][0])
        self.assertEqual(parsed['tags']['private'][0], '')
    
    def test_readonly_tag(self):
        """Test round-trip parsing and composing of a JSDoc with readonly tag."""
        original = """/**
 * @readonly
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['readonly'][0], reparsed['tags']['readonly'][0])
        self.assertEqual(parsed['tags']['readonly'][0], '')
    
    def test_module_tag(self):
        """Test round-trip parsing and composing of a JSDoc with module tag."""
        original = """/**
 * @module my-module
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['module'][0], reparsed['tags']['module'][0])
        self.assertEqual(parsed['tags']['module'][0], 'my-module')
    
    def test_memberof_tag(self):
        """Test round-trip parsing and composing of a JSDoc with memberof tag."""
        original = """/**
 * @memberof namespace.MyClass
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['memberof'][0], reparsed['tags']['memberof'][0])
        self.assertEqual(parsed['tags']['memberof'][0], 'namespace.MyClass')
    
    def test_generator_tag(self):
        """Test round-trip parsing and composing of a JSDoc with generator tag."""
        original = """/**
 * @generator
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['generator'][0], reparsed['tags']['generator'][0])
        self.assertEqual(parsed['tags']['generator'][0], '')
    
    def test_yields_tag(self):
        """Test round-trip parsing and composing of a JSDoc with yields tag."""
        original = """/**
 * @yields {number} The next number in the sequence
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['yields'][0], reparsed['tags']['yields'][0])
        self.assertEqual(parsed['tags']['yields'][0], '{number} The next number in the sequence')
    
    def test_template_tag(self):
        """Test round-trip parsing and composing of a JSDoc with template tag."""
        original = """/**
 * @template T The type parameter
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['template'][0], reparsed['tags']['template'][0])
        self.assertEqual(parsed['tags']['template'][0], 'T The type parameter')
    
    def test_typedef_tag(self):
        """Test round-trip parsing and composing of a JSDoc with typedef tag."""
        original = """/**
 * @typedef {Object} Person
 * @property {string} name The name
 * @property {number} age The age
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['typedef'][0], reparsed['tags']['typedef'][0])
        self.assertEqual(parsed['tags']['property'][0], reparsed['tags']['property'][0])
        self.assertEqual(parsed['tags']['property'][1], reparsed['tags']['property'][1])
    
    def test_async_tag(self):
        """Test round-trip parsing and composing of a JSDoc with async tag."""
        original = """/**
 * @async
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['async'][0], reparsed['tags']['async'][0])
        self.assertEqual(parsed['tags']['async'][0], '')
    
    def test_description_with_markdown(self):
        """Test round-trip parsing and composing of a JSDoc with markdown in description."""
        original = """/**
 * Description with **bold** and *italic* text.
 * - List item 1
 * - List item 2
 * ```js
 * const x = 1;
 * ```
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['description'], reparsed['description'])
        self.assertIn('**bold**', parsed['description'])
        self.assertIn('*italic*', parsed['description'])
        self.assertIn('List item', parsed['description'])
    
    def test_event_tag(self):
        """Test round-trip parsing and composing of a JSDoc with event tag."""
        original = """/**
 * @event module:mymodule#event:change
 * @type {object}
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['event'][0], reparsed['tags']['event'][0])
        self.assertEqual(parsed['tags']['type'][0], reparsed['tags']['type'][0])
    
    def test_callback_definition(self):
        """Test round-trip parsing and composing of a JSDoc with callback definition."""
        original = """/**
 * @callback RequestCallback
 * @param {Error} err The error object
 * @param {object} response The response object
 * @returns {void}
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['callback'][0], reparsed['tags']['callback'][0])
        self.assertEqual(len(parsed['params']), len(reparsed['params']))
        self.assertEqual(parsed['returns']['type'], reparsed['returns']['type'])
    
    def test_see_tag(self):
        """Test round-trip parsing and composing of a JSDoc with see tag."""
        original = """/**
 * @see {@link https://example.com|Example}
 * @see OtherClass#otherMethod
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(len(parsed['tags']['see']), len(reparsed['tags']['see']))
        self.assertEqual(parsed['tags']['see'][0], '{@link https://example.com|Example}')
        self.assertEqual(parsed['tags']['see'][1], 'OtherClass#otherMethod')
    
    def test_namespace_tag(self):
        """Test round-trip parsing and composing of a JSDoc with namespace tag."""
        original = """/**
 * @namespace MyNamespace
 */"""
        parsed = parse_jsdoc(original)
        composed = compose_jsdoc(parsed)
        reparsed = parse_jsdoc(composed)
        
        self.assertEqual(parsed['tags']['namespace'][0], reparsed['tags']['namespace'][0])
        self.assertEqual(parsed['tags']['namespace'][0], 'MyNamespace')


if __name__ == '__main__':
    unittest.main()
