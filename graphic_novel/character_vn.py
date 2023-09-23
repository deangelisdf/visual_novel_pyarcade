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
        self.sprites: Dict[str, Dict[str,arcade.Sprite]] = {}
    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, x:str):
        if x not in self.sprites.keys():
            return
        self.sprites[x].center_y = self.sprites[self.__state].center_y
        self.sprites[x].center_x = self.sprites[self.__state].center_x
        self.__state = x   
    def draw(self):
        self.sprites[self.state].draw()
    @property
    def bottom(self) -> float:
        """Return the y coordinate of the bottom of the sprite."""
        return self.sprites[self.state].bottom
    @bottom.setter
    def bottom(self, amount: float):
        """Set the location of the sprite based on the bottom y coordinate."""
        self.sprites[self.state].bottom = amount
    @property
    def left(self):
        return self.sprites[self.state].left
    @left.setter
    def left(self, x:float):
        self.sprites[self.state].left = x
    @property
    def right(self):
        return self.sprites[self.state]
    @right.setter
    def right(self, x:float):
        self.sprites[self.state] = x

__author__ = "dfdeangelis"
