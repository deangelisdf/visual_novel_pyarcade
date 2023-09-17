import random
from typing import List, Dict, Callable
import arcade
from arcade.gui import UIManager, UIBoxLayout, UIAnchorWidget, UIFlatButton, UIOnClickEvent
from arcade.gui.widgets import UITextArea, UILabel, UIBorder
from graphic_novel.dlg_parser import parser_dialog
from graphic_novel.dlg_parser import ast_dialog
import graphic_novel.constants as constants

class GraphicNovel(arcade.View):
    """ Our custom Window Class"""
    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()
        self._skip_dlg  = False
        self._skip_time = 0.0
        self.manager = UIManager()
        self.dialog:ast_dialog.Node = None
        self.ptr_blocks= None
        self.jump_next: Dict[str,str] = {}
        self.text_area:  UITextArea= None #conteinar text
        self.title_area: UITextArea= None #conteinar title
        self.v_box   = UIBoxLayout() #container button for menu
        self.box_dlg = UIBoxLayout()

        self.left_side_screen:List[arcade.Sprite]  = []
        self.right_side_screen:List[arcade.Sprite] = []
        
        self.__dict_char: Dict[str, arcade.Sprite] = {}
        
        self.__events: Dict[str, Callable[[], int]] = {}

        self.__dialog_end:bool = False
        arcade.set_background_color(arcade.color.AMAZON)

    def add_event(self, name_event: str, event: Callable[[], int]) -> None:
        self.__events[name_event] = event

    @property
    def ended(self) -> bool:
        return self.__dialog_end
    @property
    def characters(self) -> Dict[str, arcade.Sprite]:
        return self.__dict_char

    @characters.setter
    def characters(self, dict_char: Dict[str, arcade.Sprite]) -> None:
        self.__dict_char = dict_char
        for char in self.__dict_char.values():
            if char.width >= self.window.width/3:
                char.scale = 0.5
            elif char.height >= self.window.height/3:
                char.scale = 0.5
        
    def setup(self, path_dialog: str) -> None:
        """ Set up the game and initialize the variables. """
        self.manager.enable()
        self.left_side_screen.clear()
        self.right_side_screen.clear()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        height_25perc  = (self.window.height * 25)/100
        self.text_area = UITextArea(
                               width=self.window.width-10,
                               height=height_25perc,
                               text="", text_color=(0, 0, 0, 255))
        self.title_area= UILabel(width=self.window.width-10, height=30,
                                    text="", text_color=(0, 0, 0, 255))
        self.box_dlg.add(UIBorder(self.title_area))
        self.box_dlg.add(self.text_area)
        self.manager.add(UIAnchorWidget(
                anchor_x="left", anchor_y="bottom", child=UIBorder(self.box_dlg)))
        self.manager.add(UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box))
        self.setup_dialog(path_dialog)
        self.__next_step()

    def setup_dialog(self, path_dialog: str) -> None:
        self.dialog = parser_dialog.parsing(path_dialog)
        self.ptr_blocks = iter(self.dialog.blocks[constants.INIT_BLOCK].block)

    def on_draw(self) -> None:
        """ Draw everything """
        self.clear()
        for idx, sprite_left in enumerate(self.left_side_screen):
            sprite_left.bottom = self.box_dlg.top
            sprite_left.left = 10 + idx*5
            sprite_left.draw()
        for idx, sprite_right in enumerate(self.right_side_screen):
            sprite_right.bottom = self.box_dlg.top
            sprite_right.right  = self.window.width - 10 - idx*5
            sprite_right.draw()
        self.manager.draw()
        if self._skip_dlg:
            arcade.draw_text("SKIPPING", 1, 1, font_size=15)
    
    def __jmp_next_dialog(self, label:str)->None:
        assert(label in self.dialog.blocks)
        self.ptr_blocks = iter(self.dialog.blocks[label].block)
        self.v_box.clear()
        self.__next_step()
    def __jump_next_dialog(self, event: UIOnClickEvent) -> None:
        jmp_label = self.jump_next[event.source.text]
        self.__jmp_next_dialog(jmp_label)

    def __remove_pg_from_lists(self, sprite:arcade.Sprite) -> None:
        if sprite in self.left_side_screen:
            self.left_side_screen.remove(sprite)
        elif sprite in self.right_side_screen:
            self.right_side_screen.remove(sprite)

    def __move_action(self, sprite:arcade.Sprite, arg:str) -> None:
        self.__remove_pg_from_lists(sprite)
        if arg == constants.LEFT_TOKEN:
            self.left_side_screen.append(sprite)
        elif arg == constants.RIGHT_TOKEN:
            self.right_side_screen.append(sprite)
    def __jmp_action(self, sprite:arcade.Sprite, arg:str) -> None:
        self.__jmp_next_dialog(arg)
    def __set_alpha_action(self, sprite:arcade.Sprite, arg:str) -> None:
        sprite.alpha = int(arg,10)
    def __event_action(self, sprite:arcade.Sprite, arg:str) -> None:
        if arg in self.__events:
            res = self.__events[arg]()
            print(res) #TODO use for next action in same way
    def __shake_action(self, sprite:arcade.Sprite, arg:str) -> None:
        assert(arg in self.__dict_char)
        #TODO
        pass
    def __interpreting_action(self, sprite:arcade.Sprite, tok:List[str]) -> None:
        strategy = {constants.MOVE_ACTION_TOKEN: self.__move_action,
                    constants.ALPHA_TOKEN: self.__set_alpha_action,
                    constants.EVENT_TOKEN: self.__event_action,
                    constants.JUMP_TOKEN:  self.__jmp_action,
                    constants.SHAKE_TOKEN: self.__shake_action }
        assert(len(tok) == 2)
        assert(tok[0] in strategy)
        strategy[tok[0]](sprite, tok[1])

    def __action_video(self, name_pg:str, actions:List[str]) -> None:
        if not name_pg in self.__dict_char:
            sprite = None
        else:
            sprite = self.__dict_char[name_pg]
        for action in actions:
            tok = action.split()
            self.__interpreting_action(sprite, tok)

    def __next_step(self) -> None:
        try:
            node_dlg = next(self.ptr_blocks)
        except StopIteration:
            self.__dialog_end = True
            return
        if isinstance(node_dlg, ast_dialog.Dialog):
            self.title_area.text= node_dlg.char_name
            self.text_area.text = node_dlg.text
            self.__action_video(node_dlg.char_name, node_dlg.action)
        elif isinstance(node_dlg, ast_dialog.Menu):
            for case in node_dlg.cases:
                button = UIFlatButton(text=case.label, width=200)
                self.jump_next[case.label] = case.block.name
                self.v_box.add(button.with_space_around(bottom=1))
                button.on_click = self.__jump_next_dialog
                self.v_box.add(button)

    def update(self, delta_time: float) -> None:
        if self._skip_time<=constants.SKIP_TIME:
            self._skip_time += delta_time
        elif self._skip_dlg:
            self.__next_step()
            self._skip_time = 0.0
        return super().update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.TAB:
            self._skip_dlg = not self._skip_dlg
        elif symbol == arcade.key.ENTER:
            self.__next_step()
