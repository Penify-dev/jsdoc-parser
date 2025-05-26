"""Utils module for JSDoc handling."""

from typing import Dict, Any, List, Optional
import re


def extract_type_info(type_str: str) -> Dict[str, Any]:
    """
    Extract detailed type information from a JSDoc type string.
    
    Args:
        type_str (str): The type string from a JSDoc tag
        
    Returns:
        Dict[str, Any]: A dictionary with parsed type information
        
    Example:
        >>> extract_type_info('Array<string>')
        {'name': 'Array', 'params': ['string']}
        >>> extract_type_info('Object<string, number>')
        {'name': 'Object', 'params': ['string', 'number']}
        >>> extract_type_info('string|number')
        {'union': ['string', 'number']}
    """
    result = {}
    
    # Check for union types
    if '|' in type_str:
        union_types = [t.strip() for t in type_str.split('|')]
        result['union'] = union_types
        return result
    
    # Check for generics/templates
    generic_match = re.match(r'(\w+)\s*<\s*(.+)\s*>', type_str)
    if generic_match:
        base_type = generic_match.group(1)
        params_str = generic_match.group(2)
        
        # Handle nested generics by counting brackets
        params = []
        current_param = ''
        bracket_level = 0
        
        for char in params_str:
            if char == ',' and bracket_level == 0:
                params.append(current_param.strip())
                current_param = ''
            else:
                if char == '<':
                    bracket_level += 1
                elif char == '>':
                    bracket_level -= 1
                current_param += char
        
        if current_param:
            params.append(current_param.strip())
        
        result['name'] = base_type
        result['params'] = params
        return result
    
    # Simple type
    result['name'] = type_str
    return result


def merge_jsdoc_objects(base: Dict[str, Any], overlay: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two JSDoc objects, with the overlay taking precedence.
    
    Args:
        base (Dict[str, Any]): The base JSDoc object
        overlay (Dict[str, Any]): The overlay JSDoc object that takes precedence
        
    Returns:
        Dict[str, Any]: The merged JSDoc object
    """
    result = base.copy()
    
    # Merge description
    if 'description' in overlay:
        result['description'] = overlay['description']
    
    # Merge params
    if 'params' in overlay:
        if 'params' not in result:
            result['params'] = []
            
        # Create lookup for existing params
        param_lookup = {p['name']: i for i, p in enumerate(result['params'])}
        
        for overlay_param in overlay['params']:
            if overlay_param['name'] in param_lookup:
                # Update existing param
                idx = param_lookup[overlay_param['name']]
                result['params'][idx].update(overlay_param)
            else:
                # Add new param
                result['params'].append(overlay_param)
    
    # Merge returns
    if 'returns' in overlay:
        result['returns'] = overlay['returns']
    
    # Merge throws
    if 'throws' in overlay:
        if 'throws' not in result:
            result['throws'] = []
        result['throws'].extend(overlay['throws'])
    
    # Merge examples
    if 'examples' in overlay:
        if 'examples' not in result:
            result['examples'] = []
        result['examples'].extend(overlay['examples'])
    
    # Merge tags
    if 'tags' in overlay:
        if 'tags' not in result:
            result['tags'] = {}
            
        for tag, values in overlay['tags'].items():
            if tag not in result['tags']:
                result['tags'][tag] = []
            result['tags'][tag].extend(values)
    
    return result


def remove_jsdoc_component(jsdoc_obj: Dict[str, Any], component_type: str, identifier: Optional[str] = None) -> Dict[str, Any]:
    """
    Remove a component from a JSDoc object.
    
    Args:
        jsdoc_obj (Dict[str, Any]): The JSDoc object
        component_type (str): The component type to remove ('param', 'returns', 'throws', 'example', 'tag')
        identifier (Optional[str]): The identifier of the component (e.g., param name, tag name)
        
    Returns:
        Dict[str, Any]: The modified JSDoc object
    """
    result = jsdoc_obj.copy()
    
    if component_type == 'description':
        if 'description' in result:
            del result['description']
    
    elif component_type == 'param':
        if 'params' in result and identifier:
            result['params'] = [p for p in result['params'] if p['name'] != identifier]
            if not result['params']:
                del result['params']
    
    elif component_type == 'returns':
        if 'returns' in result:
            del result['returns']
    
    elif component_type == 'throws':
        if 'throws' in result:
            if identifier:
                # Remove throws with matching type
                result['throws'] = [t for t in result['throws'] if t.get('type') != identifier]
                if not result['throws']:
                    del result['throws']
            else:
                # Remove all throws
                del result['throws']
    
    elif component_type == 'example':
        if 'examples' in result:
            if identifier is not None:
                # Remove specific example by index or content match
                try:
                    idx = int(identifier)
                    if 0 <= idx < len(result['examples']):
                        result['examples'].pop(idx)
                except ValueError:
                    # If not an index, try to match content
                    # Keep examples that don't contain the identifier
                    original_examples = result['examples'].copy()
                    result['examples'] = [e for e in original_examples if identifier not in e]
                
                if not result['examples']:
                    del result['examples']
            else:
                # Remove all examples
                del result['examples']
    
    elif component_type == 'tag':
        if 'tags' in result and identifier:
            if identifier in result['tags']:
                del result['tags'][identifier]
                if not result['tags']:
                    del result['tags']
    
    return result
