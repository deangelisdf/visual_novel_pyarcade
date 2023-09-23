"""file: input_handler.py
To manage the possible inpyt to the system
"""
from typing import Dict
import arcade
from graphic_novel import layout_commands

class InputHandler:
    """
    command_layout is the internal table with association between
        Keyboard key and Command (to work with GraphicNovel view)
    """
    def __init__(self):
        self.command_layout:Dict[int, layout_commands.layout_command] = {
            arcade.key.ENTER: layout_commands.next_dlg_command(),
            arcade.key.TAB:   layout_commands.skip_dlg_command(),
            arcade.key.H:     layout_commands.hide_gui_command()
        }
    def change_key(self, name_action:str, new_key:int):
        """brief: must be used to change the command layout"""
        old_key = None
        for key, cmd in self.command_layout.items():
            if cmd.name == name_action:
                old_key = key
                break
        if old_key is None:
            raise NotImplementedError(f"{name_action} is no command in our layout")
        self.command_layout[new_key] = self.command_layout.pop(old_key)

__author__ = "dfdeangelis"
