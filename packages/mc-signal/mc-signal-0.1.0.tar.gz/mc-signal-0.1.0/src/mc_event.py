from dataclasses import dataclass
import types

@dataclass
class MCEvent:
    name: str
    call_function: types.FunctionType
