"""filename: ast_dialog.py
used to develop the classes to rapresent the Dialog Tree
in all possible nodes.
author: Domenico Francesco De Angelis
"""
from typing import List, Dict, Union

class Node:
    """Abstract base class for AST nodes."""
    __slots__ = ('inner', )
    def __init__(self):
        self.inner = 0
    def __repr__(self):
        """ Generates a python representation of the current node"""
        result = self.__class__.__name__ + '('
        self.inner += 1
        for child in self.children():
            result += f"\n{' '*self.inner}{child}\n"
        result += ')'
        return result
    def children(self):
        """ A sequence of all children that are Nodes"""
        pass
class RootDialog(Node):
    __slots__ = ('file_name', 'blocks', '__weakref__')
    def __init__(self, file_name:str, blocks:list):
        super().__init__()
        self.file_name = file_name
        self.blocks:Dict[BlockInstr] = {i.label:i for i in blocks}
    def children(self):
        return ("blocks", self.blocks)
    def __iter__(self):
        yield self.blocks
    attr_names = ()
class Dialog(Node):
    __slots__ = ('char_name', 'text', 'action', '__weakref__')
    def __init__(self, char_name:str, text:str, action:str):
        super().__init__()
        self.char_name:str = char_name
        self.text:str = text
        self.action:List[str] = action
    def children(self):
        return (("char_name", self.char_name), ("text", self.text))
    def __iter__(self):
        yield self.char_name
        yield self.text
    attr_names = ()
class PythonExp(Node):
    __slots__ = ('expr', '__weakref__')
    def __init__(self, expr:str):
        super().__init__()
        self.expr:str = expr
    def children(self):
        return ("expr", self.expr)
    def __iter__(self):
        yield self.expr
    attr_names = ()
class BlockInstr(Node):
    __slots__ = ('label', 'block', '__weakref__')
    def __init__(self, label:str, block:list):
        super().__init__()
        self.label:str = label
        self.block:List[Union[Dialog, Menu, PythonExp, Jump]] = block
    def children(self):
        nodelist = [("label", self.label)]
        if self.block is not None:
            nodelist.append(("block", self.block))
        return tuple(nodelist)
    def __iter__(self):
        yield self.label
        if self.block is not None:
            yield self.block
    attr_names = ()
class If(Node):
    __slots__ = ('cond', 'iftrue', 'iffalse', '__weakref__')
    def __init__(self, cond, iftrue, iffalse):
        super().__init__()
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse
    def children(self):
        nodelist = []
        if self.cond is not None:
            nodelist.append(("cond", self.cond))
        if self.iftrue is not None:
            nodelist.append(("iftrue", self.iftrue))
        if self.iffalse is not None:
            nodelist.append(("iffalse", self.iffalse))
        return tuple(nodelist)
    def __iter__(self):
        if self.cond is not None:
            yield self.cond
        if self.iftrue is not None:
            yield self.iftrue
        if self.iffalse is not None:
            yield self.iffalse
    attr_names = ()
class Menu(Node):
    __slots__ = ('cases', 'type_menu', '__weakref__')
    def __init__(self):
        super().__init__()
        self.type_menu:str = ""
        self.cases:List[BlockInstr] = []
    def children(self):
        return ("cases", self.cases)
    def __iter__(self):
        yield self.cases
    attr_names = ()

class Request(Node):
    __slots__ = ('type_request', 'event_name', '__weakref__')
    def __init__(self):
        super().__init__()
        self.type_request:str = ""
        self.event_name:str   = ""
    def children(self):
        return ('event_name', self.event_name)
    def __iter__(self):
        return
        yield
    attr_names = ()
    
class Jump(Node):
    __slots__ = ('name', '__weakref__')
    def __init__(self, name):
        super().__init__()
        self.name:str = name
    def children(self):
        return ("name", self.name)
    def __iter__(self):
        return
        yield
    attr_names = ('name', )

__author__ = "dfdeangelis"
