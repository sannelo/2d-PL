from typing import Dict, Generic, TypeVar
from src.blocks._blocks import NewVar, NoneBlock, Start

from enum import Enum

class BlockType(Enum):
    NONEBLOCK = NoneBlock
    NEW_VAR_BLOCK = NewVar
    START = Start

ALL_BLOCKS = {**{block.value.NAME: block.value for block in BlockType}}
ALL_BLOCKS_TYPE = TypeVar("ALL_BLOCKS_TYPE", *(block.value for block in BlockType)) # type: ignore

def get_by_index(index: int):
    block = ALL_BLOCKS.get(list(ALL_BLOCKS.keys())[index % len(ALL_BLOCKS.keys())])
    return block if block else NoneBlock

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

class Blocks(Generic[_KT, _VT]):

    def __init__(self) -> None:
        self.blocks: Dict[_KT, _VT] = {}

    def __str__(self):
        return str(self.blocks)

    def __getitem__(self, key: _KT) -> None | _VT:
        return self.blocks.get(key)

    def __setitem__(self, key: _KT, value: _VT):
        self.blocks[key] = value

    def clear(self):
        self.blocks.clear()

    def pop(self, key: _KT):
        return self.blocks.pop(key, None)

    def values(self):
        return self.blocks.values()
    
    def keys(self):
        return self.blocks.keys()

    def update(self, **params: _VT):
        self.blocks.update(params) # type: ignore

    def get(self, key: _KT):
        return self.blocks.get(key)

# if __name__ == "__main__":
#     blocks = Blocks[str, bool | int]()

#     # setattr(blocks, 'new_method', lambda x: [print(to) for to in x])

#     blocks["123"] = True # Обращение к Blocks.blocks

#     blocks.update(
#         **{
#             "abs": 123
#         }
#     )

#     var = blocks["123"]

#     print(blocks, blocks["1234"])
