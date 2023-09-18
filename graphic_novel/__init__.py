import random
from typing import List, Dict, Callable
import arcade
from arcade.gui import UIManager, UIBoxLayout, UIAnchorWidget, UIFlatButton, UIOnClickEvent
from arcade.gui.widgets import UITextArea, UILabel, UIBorder
from graphic_novel.dlg_parser import parser_dialog
from graphic_novel.dlg_parser import ast_dialog
import graphic_novel.constants as constants

class UITypingTextArea(UITextArea):
    def __init__(self, x: float = 0, y: float = 0, width: float = 400, height: float = 40, 
                 text: str = "", font_name = ('Arial',), font_size: float = 12,
                 text_color: arcade.Color = (255,255,255,255), multiline: bool = True,
                 scroll_speed: float = None, size_hint=None, size_hint_min=None, size_hint_max=None,
                 style=None, **kwargs):
        super().__init__(x, y, width, height, text, font_name, font_size, text_color, multiline, scroll_speed, size_hint, size_hint_min, size_hint_max, style, **kwargs)
        self.__text_to_write:str = ""
        self.delay_typing = constants.DELAY_WRITING_TIME
        self.__last_delay_typing:float = 0.0
        self.instant_write = False
        self.counter_char:int = 0
    def set_text(self, text: str):
        if self.instant_write:
            self.text = text
            self.__text_to_write = ""
        else:
            self.__text_to_write = str(text)
            self.text = ""
        self.counter_char = 0
        self.__last_delay_typing = 0.0
    def on_update(self, dt):
        if self.counter_char < len(self.__text_to_write):
            if self.__last_delay_typing >= self.delay_typing:
                self.__last_delay_typing = 0.0
                self.counter_char += 1
                self.text = str(self.__text_to_write[:self.counter_char])
            else:
                self.__last_delay_typing += dt
        return super().on_update(dt)

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
        self.__jump_next: Dict[str,str] = {}
        self.text_area:  UITypingTextArea= None #conteinar text
        self.title_area: UILabel   = None #conteinar title
        self.v_box   = UIBoxLayout() #container button for menu
        self.box_dlg = UIBoxLayout()

        self.left_side_screen:List[arcade.Sprite]  = []
        self.right_side_screen:List[arcade.Sprite] = []
        
        self.__dict_char: Dict[str, arcade.Sprite] = {}
        
        self.__events: Dict[str, Callable[['GraphicNovel'], int]] = {}

        self.__dialog_end:bool = False
        self.__filter_video:list = []

    def on_ended(self):
        """This method represent the END of dialog"""
        pass

    def add_event(self, name_event: str, event: Callable[['GraphicNovel'], int]) -> None:
        """Add event to active in dialog json"""
        self.__events[name_event] = event

    def add_filter_video(self, filter) -> None:
        """add GLS filters"""
        self.__filter_video.append(filter)

    @property
    def ended(self) -> bool:
        return self.__dialog_end
    @property
    def characters(self) -> Dict[str, arcade.Sprite]:
        """Characters used in dialogs
        NAME: SPRITE"""
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
        arcade.set_background_color(arcade.color.AFRICAN_VIOLET)
        height_25perc  = (self.window.height * 25)/100
        self.text_area = UITypingTextArea(
                               width=self.window.width-10,
                               height=height_25perc,
                               text="")
        self.title_area= UILabel(width=self.window.width-10, height=30,
                                    text="")
        self.box_dlg.add(UIBorder(self.title_area))
        self.box_dlg.add(self.text_area)
        self.manager.add(UIAnchorWidget(
                anchor_x="left", anchor_y="bottom", child=UIBorder(self.box_dlg)))
        self.manager.add(UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box))
        self.setup_dialog(path_dialog)
        self.set_color_text(constants.DEFAULT_COLOR_TEXT)
        self.__next_step()

    def set_color_text(self, color: arcade.RGBA):
        self.text_area.doc.set_style(0, 12, dict(color=arcade.get_four_byte_color(color)))
        self.title_area.label.document.set_style(0, len(self.title_area.text), dict(color=arcade.get_four_byte_color(color)))

    def setup_dialog(self, path_dialog: str) -> None:
        self.dialog = parser_dialog.parsing(path_dialog)
        self.ptr_blocks = iter(self.dialog.blocks[constants.INIT_BLOCK].block)

    def on_draw(self) -> None:
        """ Draw everything """
        #self.clear()
        if len(self.__filter_video) > 0:
            for filter_video in self.__filter_video:
                filter_video.use()
                filter_video.clear()
            self.draw()
            self.window.use()
            self.window.clear()
            for filter_video in self.__filter_video:
                filter_video.draw()
        else:
            self.window.use()
            self.window.clear()
            self.draw()
    def draw(self):
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
        """Generic implementation of jump action between a dialog block to another"""
        assert(label in self.dialog.blocks)
        self.ptr_blocks = iter(self.dialog.blocks[label].block)
        self.v_box.clear()
        self.__next_step()
    def __jump_next_dialog(self, event: UIOnClickEvent) -> None:
        jmp_label = self.__jump_next[event.source.text]
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
            res = self.__events[arg](self)
            print(res) #TODO use for next action in same way
    def __shake_action(self, sprite:arcade.Sprite, arg:str) -> None:
        assert(arg in self.__dict_char)
        #TODO
        pass
    def __restart_action(self, sprite:arcade.Sprite, arg:str) -> None:
        self.left_side_screen.clear()
        self.right_side_screen.clear()
        self.__filter_video.clear()
        self.set_color_text(constants.DEFAULT_COLOR_TEXT)
    def __interpreting_action(self, sprite:arcade.Sprite, tok:List[str]) -> None:
        """Actions are defined with 2 words, action and argument"""
        strategy = {constants.MOVE_ACTION_TOKEN: self.__move_action,
                    constants.ALPHA_TOKEN: self.__set_alpha_action,
                    constants.EVENT_TOKEN: self.__event_action,
                    constants.JUMP_TOKEN:  self.__jmp_action,
                    constants.SHAKE_TOKEN: self.__shake_action,
                    constants.RESTART_TOKEN: self.__restart_action }
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
            self.on_ended()
            return
        if isinstance(node_dlg, ast_dialog.Dialog):
            self.title_area.text= node_dlg.char_name
            self.text_area.set_text(node_dlg.text)
            self.__action_video(node_dlg.char_name, node_dlg.action)
        elif isinstance(node_dlg, ast_dialog.Menu):
            for case in node_dlg.cases:
                button = UIFlatButton(text=case.label, width=200)
                self.__jump_next[case.label] = case.block.name
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
