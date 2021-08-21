"""
Internal memory representation of the declarations in the header file
"""

from dataclasses import dataclass
from typing import Any

@dataclass 
class Declaration:
    # TODO: provide more fine grained typing information
    name: str
    ret_tpy: Any 
    parameters: Any
