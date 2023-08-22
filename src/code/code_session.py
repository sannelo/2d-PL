
from queue import Queue
import config
from bitstring import Bits, BitArray, BitStream, pack
from typing import Any, List

# from src.blocks.IBlock import IBlock

# bits_type = List[int] | str | List[bool]

# class Bits:

#     _bits: bits_type

#     @property
#     def value(self):
#         return self._2bit_array(self._bits)
    
#     @value.setter
#     def value(self, value: bits_type):
#         self._bits = value

#     def append(self, bit: int | str | bool):
#         if type(self._bits) == str:
#             self._bits += str(int(bit))
#         elif type(self._bits) == list:
#             self._bits.append(bool(bit))
#         # elif type(self._bits) == list[int]:
#         #     self._bits.append(int(bit)) # type: ignore

#     def __iter__(self):
#         return iter(self._2bit_array(self._bits))
    
#     def __getitem__(self, index: int) -> int:
#         return self._2bit_array(self._bits)[index]

#     def __setitem__(self, index: int, bit: int | str | bool):
#         if type(self._bits) == str:
#             self._bits = self._bits[:index] + str(int(bit)) + self._bits[index + 1:]
#         elif type(self._bits) == list[bool]:
#             self._bits[index] = bool(bit)
#         elif type(self._bits) == list[int]:
#             self._bits[index] = int(bit) # type: ignore

#     def __str__(self) -> str:
#         return str(self.value)
    
#     def _2bit_array(self, bits: bits_type):
#         return [1 if bit == "1" or bit == True or bit == 1 else 0 for bit in bits]

#     def __init__(self, bits: list | str) -> None:
#         self._bits = bits

class CodeSession():
    variables: dict[str, str]

    nexts: list

    _steps: int = 0

    def __init__(self) -> None:
        self.nexts = [] # Queue()
        self.variables = {}

    def new_var(self, var_id: list[int | bool] | str, value: list[int | bool] | str):
        str_id: str = CodeSession._toBits(var_id).hex
        bin_value: str = CodeSession._toBits(value).bin
        self.variables[str_id] = bin_value

    def get_string(self, var_id: list[int | bool] | str):
        str_id: str = CodeSession._toBits(var_id).hex
        return Bits(bin=self.variables.get(str_id, "0b0")).tobytes().decode("utf-8", "ignore")
    
    def get_int(self, var_id: list[int | bool] | str):
        str_id: str = CodeSession._toBits(var_id).hex
        return int(Bits(bin=self.variables.get(str_id, "0b0")).tobytes())

    @staticmethod
    def _toBits(var: list[int | bool] | str):
        if type(var) == str:
            return Bits(bin="0b" + var)
        elif type(var) == list[int | bool]:
            return Bits(bin="0b" + "".join([str(i) for i in var]))
        else:
            raise ValueError("Incorect var_id type {}".format(type(var).__name__))
        
    def put(self, block):
        self.nexts.append(block)
        # if len(self.nexts) == 1:
        #     self.nexts.append([])
        
        # self.nexts[1].append(block)
    
    def step(self):
        if len(self.nexts) == 0: return

        nexts = self.nexts.copy()
        self.nexts: list = []


        for block in nexts:
            self._steps += 1
            if config.DEBUG: print(f"Step #{self._steps}")
            block.exec(self)
        
        # self.nexts[0] = self.nexts[1]
        # self.nexts[1] = []
        # while True:
        # try:
        #     block = self.nexts.get_nowait()
        #     block.exec(self)
        # except queue.Empty:  # on python 2 use Queue.Empty
        #     return
        
        # for block in iter(self.nexts.get, None):
            

CodeSession()