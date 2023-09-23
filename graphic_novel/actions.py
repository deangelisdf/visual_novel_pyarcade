"""filename: actions.py
Implementation of ACTIONs.
The goal to reach is to drive the graphic novel
with those actions, defined in dialog tree

author: Domenico Francesco De Angelis
"""
from typing import Dict, Union
import arcade
import graphic_novel.constants as constants

class Action:
    """Generic class to define an Action
    Command Desing pattern implementation"""
    def __init__(self, graphic_novel):
        self.machine = graphic_novel
    def __call__(self, sprites:Dict[str,arcade.Sprite],
                 arg:str) -> int:
        pass

class MoveAction(Action):
    """Move a charachter around screen
    You can chose: two places: left and right"""
    def __call__(self, sprites:Dict[str,arcade.Sprite],
                 arg: str) -> int:
        state_name = sprites[constants.CHAR_SELECTED_KEY]
        self.machine._remove_pg_from_lists(sprites[state_name])
        if arg == constants.LEFT_TOKEN:
            self.machine.left_side_screen.append(sprites[state_name])
        elif arg == constants.RIGHT_TOKEN:
            self.machine.right_side_screen.append(sprites[state_name])
        return 0
class JmpAction(Action):
    """Jump to another label dialog,
    can be used for a loop or to reuse dialog leaf"""
    def __call__(self, sprite:Dict[str,arcade.Sprite], arg: str) -> int:
        self.machine.jmp_next_dialog(arg)
        return 0
class SetAlphaAction(Action):
    """Set alpha channel on character sprite"""
    def __call__(self, sprites:Dict[str,arcade.Sprite], arg: str) -> int:
        state_name = sprites[constants.CHAR_SELECTED_KEY]
        sprites[state_name].alpha = int(arg,10)
        return 0
class EventAction(Action):
    """Trigger an internal event
    The user can use it to add some game logic as quests or
    want work directly on screen"""
    def __call__(self, sprite:Dict[str,arcade.Sprite], arg: str) -> int:
        if arg in self.machine.event_table:
            return self.machine.event_table[arg](self.machine)
        return 0
class ShakeAction(Action):
    """Should be implemented.
    The idea is to shake the character sprite selected with arg
    or arg is the time or is the intensity (Should be decided)"""
    def __call__(self, sprite:Dict[str,arcade.Sprite], arg: str) -> int:
        assert arg in self.machine.__dict_char #TODO
        return 0
class RestartAction(Action):
    """This command reset internal video queues"""
    def __call__(self, sprite:Dict[str,arcade.Sprite], arg: str) -> int:
        self.machine.left_side_screen.clear()
        self.machine.right_side_screen.clear()
        del self.machine.video_filters
        self.machine.set_color_text(constants.DEFAULT_COLOR_TEXT)
        return 0

class SetBackground(Action):
    """This command can change the background"""
    def __call__(self, sprite:Dict[str,arcade.Sprite], arg: str) -> int:
        self.machine.background_texture = arcade.load_texture(arg)
        return 0

class ChangeCharSprite(Action):
    """This action change sprite selected for the character"""
    def __call__(self, sprites:Dict[str,arcade.Sprite], arg:str) -> int:
        if arg in sprites:
            sprites[constants.CHAR_SELECTED_KEY] = arg

__author__ = "dfdeangelis"
