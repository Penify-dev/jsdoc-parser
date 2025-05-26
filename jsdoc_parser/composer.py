"""Composer module for JSDoc strings."""

from typing import Dict, List, Any, Union


def compose_jsdoc(jsdoc_obj: Dict[str, Any]) -> str:
    """Compose a JSDoc string from a structured dictionary.
    
    This function constructs a JSDoc comment based on the provided dictionary
    structure, handling various components such as descriptions, parameters,
    returns, throws, examples, and other tags. It ensures that each section is
    correctly formatted and included in the final JSDoc string if present in the
    input dictionary.
    
    Args:
        jsdoc_obj (Dict[str, Any]): The dictionary representing the JSDoc structure.
    
    Returns:
        str: The formatted JSDoc string.
    """
    lines = ['/**']
    
    # Add the description
    if 'description' in jsdoc_obj and jsdoc_obj['description']:
        for line in jsdoc_obj['description'].split('\n'):
            lines.append(f' * {line}')
        lines.append(' *')
    
    # Add the params
    if 'params' in jsdoc_obj:
        for param in jsdoc_obj['params']:
            param_str = ' * @param'
            
            if 'type' in param and param['type']:
                param_str += f' {{{param["type"]}}}'
                
            if 'name' in param and param['name']:
                param_str += f' {param["name"]}'
                
            if 'description' in param and param['description']:
                param_str += f' - {param["description"]}'
                
            lines.append(param_str)
    
    # Add the returns
    if 'returns' in jsdoc_obj and jsdoc_obj['returns']:
        returns_str = ' * @returns'
        
        if 'type' in jsdoc_obj['returns'] and jsdoc_obj['returns']['type']:
            returns_str += f' {{{jsdoc_obj["returns"]["type"]}}}'
            
        if 'description' in jsdoc_obj['returns'] and jsdoc_obj['returns']['description']:
            returns_str += f' {jsdoc_obj["returns"]["description"]}'
            
        lines.append(returns_str)
    
    # Add the throws
    if 'throws' in jsdoc_obj:
        for throws in jsdoc_obj['throws']:
            throws_str = ' * @throws'
            
            if 'type' in throws and throws['type']:
                throws_str += f' {{{throws["type"]}}}'
                
            if 'description' in throws and throws['description']:
                throws_str += f' {throws["description"]}'
                
            lines.append(throws_str)
    
    # Add the examples
    if 'examples' in jsdoc_obj:
        for example in jsdoc_obj['examples']:
            lines.append(f' * @example {example}')
    
    # Add other tags
    if 'tags' in jsdoc_obj:
        for tag, values in jsdoc_obj['tags'].items():
            for value in values:
                lines.append(f' * @{tag} {value}')
    
    # Add the closing marker
    lines.append(' */')
    
    # Return the composed JSDoc string
    return '\n'.join(lines)
