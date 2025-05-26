# JSDoc Parser

A Python library for parsing and composing JSDoc strings.

## Installation

```bash
pip install jsdoc-parser
```

## Usage

```python
from jsdoc_parser import parse_jsdoc, compose_jsdoc

# Parse a JSDoc string into an object
jsdoc_str = """/**
 * Calculates the sum of two numbers
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} The sum of a and b
 */"""

parsed = parse_jsdoc(jsdoc_str)
print(parsed)
# Output: {'description': 'Calculates the sum of two numbers', 'params': [{'name': 'a', 'type': 'number', 'description': 'First number'}, {'name': 'b', 'type': 'number', 'description': 'Second number'}], 'returns': {'type': 'number', 'description': 'The sum of a and b'}}

# Modify the parsed object
parsed['params'][0]['description'] = 'Modified description'

# Compose the modified object back to a JSDoc string
new_jsdoc = compose_jsdoc(parsed)
print(new_jsdoc)
```

## Features

- Parse JSDoc strings into structured Python objects
- Compose JSDoc objects back into properly formatted JSDoc strings
- Support for various JSDoc tags: @param, @returns, @throws, etc.
- Easy manipulation of JSDoc components

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
