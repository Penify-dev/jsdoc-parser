"""Parser module for JSDoc strings."""

import re
from typing import Dict, List, Any, Union, Optional


def parse_jsdoc(docstring: str) -> Dict[str, Any]:
    """
    Parse a JSDoc string into a structured dictionary.
    
    Args:
        docstring (str): The JSDoc string to parse
        
    Returns:
        Dict[str, Any]: A dictionary representing the parsed JSDoc structure
    
    Example:
        >>> parse_jsdoc("/**\\n * Description\\n * @param {string} name - The name\\n */")
        {'description': 'Description', 'params': [{'name': 'name', 'type': 'string', 'description': 'The name'}]}
    """
    # Initialize the result dictionary
    result = {
        'description': '',
        'params': [],
        'returns': None,
        'throws': [],
        'examples': [],
        'tags': {}
    }
    
    # Clean up the docstring
    docstring = docstring.strip()
    
    # Remove the opening and closing markers /** and */
    if docstring.startswith('/**'):
        docstring = docstring[3:]
    if docstring.endswith('*/'):
        docstring = docstring[:-2]
        
    # Split into lines and clean them up
    lines = [line.strip() for line in docstring.split('\n')]
    lines = [re.sub(r'^[ \t]*\*', '', line).strip() for line in lines]
    
    # Process the lines
    current_tag = None
    current_content = []
    
    for line in lines:
        # Check if the line starts with a tag
        tag_match = re.match(r'^@(\w+)\s*(.*)', line)
        
        if tag_match:
            # Process the previous tag if there was one
            if current_tag:
                _process_tag(current_tag, current_content, result)
            
            # Start a new tag
            current_tag = tag_match.group(1)
            current_content = [tag_match.group(2)]
        elif current_tag:
            # Continue with the current tag
            current_content.append(line)
        else:
            # This is part of the description
            if line:
                if result['description']:
                    result['description'] += '\n' + line
                else:
                    result['description'] = line
    
    # Process the last tag if there was one
    if current_tag:
        _process_tag(current_tag, current_content, result)
    
    # Clean up the result
    if not result['params']:
        del result['params']
    if result['returns'] is None:
        del result['returns']
    if not result['throws']:
        del result['throws']
    if not result['examples']:
        del result['examples']
    if not result['tags']:
        del result['tags']
    
    return result


def _process_tag(tag: str, content: List[str], result: Dict[str, Any]) -> None:
    """
    Process a JSDoc tag and update the result dictionary.
    
    Args:
        tag (str): The tag name (without the @ symbol)
        content (List[str]): The content lines associated with the tag
        result (Dict[str, Any]): The dictionary to update
    """
    content_str = ' '.join(content).strip()
    
    if tag == 'param' or tag == 'argument' or tag == 'arg':
        # Parse @param {type} name - description
        # Updated regex to handle parameter names with dots (nested parameters)
        # Also handle optional parameters with default values: [name=defaultValue]
        param_match = re.match(r'(?:{([^}]+)})?\s*(?:\[)?([\w.]+)(?:=([^]]+))?(?:\])?\s*(?:-\s*(.*))?', content_str)
        
        if param_match:
            param_type = param_match.group(1)
            param_name = param_match.group(2)
            default_value = param_match.group(3)
            param_desc = param_match.group(4) or ''
            
            # Check if this is a nested parameter (contains a dot)
            if '.' in param_name:
                parent_name, nested_name = param_name.split('.', 1)
                
                # Find the parent parameter if it exists
                parent_param = None
                for param in result['params']:
                    if param['name'] == parent_name:
                        parent_param = param
                        break
                
                # If parent not found, add it first (happens if child param appears before parent in JSDoc)
                if not parent_param:
                    parent_param = {
                        'name': parent_name,
                        'type': 'Object',
                        'description': '',
                        'properties': []
                    }
                    result['params'].append(parent_param)
                
                # Add the nested parameter as a property of the parent
                if 'properties' not in parent_param:
                    parent_param['properties'] = []
                
                prop_data = {
                    'name': nested_name,
                    'type': param_type,
                    'description': param_desc
                }
                
                if default_value:
                    prop_data['default'] = default_value
                    prop_data['optional'] = True
                    
                parent_param['properties'].append(prop_data)
            else:
                # Regular non-nested parameter
                param_data = {
                    'name': param_name,
                    'type': param_type,
                    'description': param_desc
                }
                
                if default_value:
                    param_data['default'] = default_value
                    param_data['optional'] = True
                    
                result['params'].append(param_data)
    
    elif tag == 'returns' or tag == 'return':
        # Parse @returns {type} description
        returns_match = re.match(r'(?:{([^}]+)})?\s*(.*)?', content_str)
        
        if returns_match:
            returns_type = returns_match.group(1)
            returns_desc = returns_match.group(2) or ''
            
            result['returns'] = {
                'type': returns_type,
                'description': returns_desc
            }
    
    elif tag == 'throws' or tag == 'exception':
        # Parse @throws {type} description
        throws_match = re.match(r'(?:{([^}]+)})?\s*(.*)?', content_str)
        
        if throws_match:
            throws_type = throws_match.group(1)
            throws_desc = throws_match.group(2) or ''
            
            result['throws'].append({
                'type': throws_type,
                'description': throws_desc
            })
    
    elif tag == 'example':
        result['examples'].append(content_str)
    
    else:
        # Store other tags
        if tag not in result['tags']:
            result['tags'][tag] = []
        result['tags'][tag].append(content_str)
