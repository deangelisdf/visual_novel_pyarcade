"""file: character_vn.py
A base class to implement the character in the VN
"""
from typing import Dict
import arcade

class CharacterVN:
    """Used to manage the character in visual novel."""
    def __init__(self, name:str):
        self.name:str = name
        self.__state = "idle"
        self.__sprites: Dict[str, Dict[str,arcade.Sprite]] = {}
        self.height: int = 0
        self.width: int = 0
    @property
    def state(self):
        return self.__state
    @property
    def sprites(self):
        return self.__sprites
    @sprites.setter
    def sprites(self, x: Dict[str, Dict[str,arcade.Sprite]]):
        self.__sprites = x
        if self.__state not in self.__sprites:
            self.__state = list(self.__sprites.keys())[0]
        self.height = self.__sprites[self.__state]._texture.height
        self.width = self.__sprites[self.__state]._texture.width
    @state.setter
    def state(self, x:str):
        if x not in self.__sprites.keys():
            return
        if self.__state in self.__sprites.keys():
            self.__sprites[x].center_y = self.__sprites[self.__state].center_y
            self.__sprites[x].center_x = self.__sprites[self.__state].center_x
        self.__state = x
        self.height = self.__sprites[x]._texture.height
        self.width = self.__sprites[x]._texture.width
    def draw(self):
        self.__sprites[self.__state].draw()
    @property
    def top(self) -> float:
        """Return the y coordinate of the top of the sprite."""
        return self.__sprites[self.__state].top
    @top.setter
    def top(self, x: float):
        """Set the location of the sprite based on the top y coordinate."""
        self.__sprites[self.__state].top = x
    @property
    def bottom(self) -> float:
        """Return the y coordinate of the bottom of the sprite."""
        return self.__sprites[self.__state].bottom
    @bottom.setter
    def bottom(self, amount: float):
        """Set the location of the sprite based on the bottom y coordinate."""
        self.__sprites[self.__state].bottom = amount
    @property
    def left(self):
        return self.__sprites[self.__state].left
    @left.setter
    def left(self, x:float):
        self.__sprites[self.__state].left = x
    @property
    def right(self):
        return self.__sprites[self.__state].right
    @right.setter
    def right(self, x:float):
        self.__sprites[self.__state].right = x

__author__ = "dfdeangelis"
