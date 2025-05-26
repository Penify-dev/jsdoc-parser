"""Parser module for JSDoc strings."""

import re
from typing import Dict, List, Any, Union, Optional, Tuple


def parse_jsdoc(docstring: str) -> Dict[str, Any]:
    # Initialize the result dictionary
    """Parse a JSDoc string into a structured dictionary.
    
    This function processes a JSDoc string to extract structured information such
    as description, parameters, return values, exceptions, examples, and other
    tags. It handles the removal of opening and closing markers, splits the content
    into lines, and categorizes each line based on whether it is part of a tag or
    the main description.
    
    Args:
        docstring (str): The JSDoc string to parse.
    
    Returns:
        Dict[str, Any]: A dictionary representing the parsed JSDoc structure.
    """
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
            # Always start with the content from the tag line (even if empty)
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


def _extract_type_from_braces(content: str) -> Tuple[Optional[str], str]:
    """Extract a type definition from curly braces, handling nested braces.
    
    Args:
        content: The string potentially starting with a type in curly braces.
        
    Returns:
        A tuple with (extracted_type, remaining_string) where extracted_type is None
        if no valid type was found.
    """
    if not content.startswith('{'):
        return None, content
        
    # Count braces to handle nested structures
    brace_count = 0
    for i, char in enumerate(content):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                # Found the closing brace
                return content[1:i], content[i+1:].strip()
    
    # No matching closing brace found
    return None, content


def _process_tag(tag: str, content: List[str], result: Dict[str, Any]) -> None:
    """Process a JSDoc tag and update the result dictionary.
    
    The function processes different types of JSDoc tags such as `param`,
    `returns`, `throws`, `example`, and others, updating the provided result
    dictionary accordingly.
    
    Args:
        tag (str): The tag name (without the @ symbol).
        content (List[str]): The content lines associated with the tag.
        result (Dict[str, Any]): The dictionary to update.
    
    Returns:
        None: The function modifies the `result` dictionary in place and does not return any
            value.
    """
    # Join content lines, preserving structure for examples but collapsing spaces for other tags
    if tag == 'example':
        content_str = '\n'.join(content).strip()
    else:
        # For non-example tags, join all lines with spaces, filtering out empty lines
        # This handles cases where description starts on the next line after the tag
        content_str = ' '.join([line.strip() for line in content if line.strip()]).strip()
    
    if tag == 'param' or tag == 'argument' or tag == 'arg':
        # First extract the type if present using brace matching
        param_type, remaining = _extract_type_from_braces(content_str)
        
        if param_type is not None:
            # Type was found, parse the rest (name, default, description)
            # Handle parameter names with special characters like $ and _
            # Only match names that do not start with a digit
            
            # First try to match the full pattern with optional parts
            param_match = re.match(r'(?:\[)?([a-zA-Z_$][\w$.]*)(?:=([^]]+))?(?:\])?\s*(?:-\s*(.*))?$', remaining)
            
            if param_match:
                param_name = param_match.group(1)
                default_value = param_match.group(2)
                param_desc = param_match.group(3) or ''
                # Detect if parameter is optional (enclosed in [])
                is_optional = bool(re.match(r'^\[([a-zA-Z_$][\w$.]*)(?:=[^]]+)?\]', remaining))
            else:
                # Try simpler pattern for just name
                name_match = re.match(r'^([a-zA-Z_$][\w$.]*)(.*)$', remaining)
                if name_match:
                    param_name = name_match.group(1)
                    remaining_text = name_match.group(2).strip()
                    if remaining_text.startswith('-'):
                        param_desc = remaining_text[1:].strip()
                    else:
                        param_desc = remaining_text
                    default_value = None
                    is_optional = False
                else:
                    # If the name doesn't match, skip this param (e.g., numeric param names)
                    return
        else:
            # No type specified, try to parse as "name description"
            simple_match = re.match(r'([a-zA-Z_$][\w$.*]*)\s+(.*)', content_str)
            if simple_match:
                param_type = None
                param_name = simple_match.group(1)
                param_desc = simple_match.group(2)
                default_value = None
                is_optional = False
            else:
                # Just a name
                # Only accept names that do not start with a digit
                if re.match(r'^[a-zA-Z_$][\w$.*]*$', content_str):
                    param_type = None
                    param_name = content_str
                    param_desc = ''
                    default_value = None
                    is_optional = False
                else:
                    # Skip numeric or invalid param names
                    return
        
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
            elif is_optional:
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
            elif is_optional:
                param_data['optional'] = True
                
            result['params'].append(param_data)
    
    elif tag == 'returns' or tag == 'return':
        # Use the same brace-matching function for return types
        returns_type, remaining = _extract_type_from_braces(content_str)
        returns_desc = remaining if returns_type is not None else content_str
            
        result['returns'] = {
            'type': returns_type,
            'description': returns_desc
        }
    
    elif tag == 'throws' or tag == 'exception':
        # Use the same brace-matching function for exception types
        throws_type, remaining = _extract_type_from_braces(content_str)
        throws_desc = remaining if throws_type is not None else content_str
            
        result['throws'].append({
            'type': throws_type,
            'description': throws_desc
        })
    
    elif tag == 'example':
        result['examples'].append(content_str)
    
    elif tag == 'description':
        # Special handling for @description tag - add to the description field
        if result['description']:
            result['description'] += '\n' + content_str
        else:
            result['description'] = content_str
    
    else:
        # Store other tags
        if tag not in result['tags']:
            result['tags'][tag] = []
        result['tags'][tag].append(content_str)
