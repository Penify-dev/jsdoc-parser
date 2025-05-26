"""JSDoc parser package initialization."""

from jsdoc_parser.parser import parse_jsdoc
from jsdoc_parser.composer import compose_jsdoc
from jsdoc_parser.utils import (
    extract_type_info,
    merge_jsdoc_objects,
    remove_jsdoc_component
)

__all__ = [
    'parse_jsdoc',
    'compose_jsdoc',
    'extract_type_info',
    'merge_jsdoc_objects',
    'remove_jsdoc_component'
]
