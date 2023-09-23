"""filename: __init__.py
Graphic novel (per arcade python)
View implementation to simplify the dialog system
in "graphic novel" way

author: Domenico Francesco De Angelis
"""
from typing import List, Dict, Callable
import arcade
from arcade.gui import UIManager, UIBoxLayout, UIAnchorWidget
from arcade.gui import UIFlatButton, UIOnClickEvent
from arcade.gui.widgets import UITextArea, UILabel, UIBorder, UIInputText
from graphic_novel.dlg_parser import parser_dialog
from graphic_novel.dlg_parser import ast_dialog
import graphic_novel.constants as constants
import graphic_novel.actions as actions
from graphic_novel import input_handler
from graphic_novel.character_vn import CharacterVN

class UITypingTextArea(UITextArea):
    """UI TextArea specialized in a typing animation"""
    def __init__(self, x:float = 0, y:float = 0, width:float = 400, height:float = 40,
                 text: str = "", font_name = ('Arial',), font_size: float = 12,
                 text_color:arcade.Color = (255,255,255,255), multiline: bool = True,
                 scroll_speed:float = None, size_hint=None, size_hint_min=None,
                 size_hint_max=None, style=None, **kwargs):
        super().__init__(x, y, width, height, text, font_name, font_size, text_color,
                         multiline, scroll_speed, size_hint, size_hint_min,
                         size_hint_max, style, **kwargs)
        self.__text_to_write:str = ""
        self.__delay_typing = constants.DELAY_WRITING_TIME
        self.__last_delay_typing:float = 0.0
        self.instant_write = False
        self.counter_char:int = 0
    @property
    def delay_typing(self):
        return self.__delay_typing
    @delay_typing.setter
    def delay_typing(self, x:float):
        if x == 0:
            self.instant_write = True
        self.__delay_typing = x
    def set_text(self, text: str) -> None:
        if self.instant_write:
            self.text = text
            self.__text_to_write = ""
        else:
            self.__text_to_write = str(text)
            self.text = ""
        self.counter_char = 0
        self.__last_delay_typing = 0.0
    def on_update(self, dt:float) -> None:
        if self.counter_char < len(self.__text_to_write):
            if self.__last_delay_typing >= self.__delay_typing:
                self.__last_delay_typing = 0.0
                self.counter_char += 1
                self.text = str(self.__text_to_write[:self.counter_char])
            else:
                self.__last_delay_typing += dt
        return super().on_update(dt)

class GraphicNovel(arcade.View):
    """This View is used to implement
    the essential graphic novel"""
    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()
        self._skip_dlg  = False
        self._not_skippable = True
        self._skip_time = 0.0
        self.manager = UIManager()
        self.dialog:ast_dialog.Node = None
        self.ptr_blocks = None
        self.history_labels:List[str] = []
        self.__jump_next: Dict[str,str] = {}
        self.text_area:  UITypingTextArea= None #conteinar text
        self.title_area: UILabel    = None #conteinar title
        self.input_text: UIInputText= None
        self.v_box   = UIBoxLayout() #container button for menu
        self.box_dlg = UIBoxLayout()
        self.hide_gui:bool = False

        self.background_texture: arcade.Texture = None
        self.left_side_screen:List[CharacterVN]  = []
        self.right_side_screen:List[CharacterVN] = []
        self.__dict_char:Dict[str, CharacterVN] = {}
        
        self.__events: Dict[str, Callable[['GraphicNovel'], int]] = {}
        self.input_text_check = constants.INPUT_CHECK_DEFAULT.copy()
        self.__dialog_end:bool = False
        self.__filter_video:list = []
        
        self.__strategy_action = {
            constants.MOVE_ACTION_TOKEN: actions.MoveAction(self),
            constants.ALPHA_TOKEN:       actions.SetAlphaAction(self),
            constants.EVENT_TOKEN:       actions.EventAction(self),
            constants.JUMP_TOKEN:        actions.JmpAction(self),
            constants.SHAKE_TOKEN:       actions.ShakeAction(self),
            constants.RESTART_TOKEN:     actions.RestartAction(self),
            constants.SET_BG_TOKEN:      actions.SetBackground(self),
            constants.SET_SPRITE_TOKEN:  actions.ChangeCharSprite(self) }
        self.input_handler = input_handler.InputHandler()

    def on_ended(self, context: 'GraphicNovel'):
        """This method represent the END of dialog"""
        pass
    
    def add_event(self, name_event: str,
                  event: Callable[['GraphicNovel'], int]) -> None:
        """Add event to active in dialog json"""
        self.__events[name_event] = event

    def add_filter_video(self, filter_video) -> None:
        """add GLS filters"""
        self.__filter_video.append(filter_video)
    @property
    def event_table(self) -> Dict[str, Callable[['GraphicNovel'], int]]:
        return self.__events
    @property
    def video_filters(self) -> list:
        return self.__filter_video
    @video_filters.deleter
    def video_filters(self) -> None:
        self.__filter_video.clear()

    @property
    def ended(self) -> bool:
        return self.__dialog_end
    @property
    def characters(self) -> Dict[str, Dict[str,arcade.Sprite]]:
        """Characters used in dialogs
        NAME: SPRITE"""
        return self.__dict_char

    @characters.setter
    def characters(self, dict_char: Dict[str, arcade.Sprite]) -> None:
        def __redim_sprite(w:int, h:int, spr:arcade.Sprite) -> None:
            if spr.width >= w:
                spr.scale = 0.5
            elif spr.height >= h:
                spr.scale = 0.5
        self.__dict_char = {}
        width = self.window.width //3
        height= self.window.height//3
        for name_char, char in dict_char.items():
            state = "idle"
            if isinstance(char, arcade.Sprite):
                __redim_sprite(width, height, char)
                char = {state:char}
            elif isinstance(char, dict):
                state = list(char.keys())[0]
                for sprite in char.values():
                    __redim_sprite(width, height, sprite)
            cvn = CharacterVN(name_char)
            cvn.sprites = char
            cvn.state = state
            self.__dict_char[name_char] = cvn

    def setup(self, path_dialog: str) -> None:
        """ Set up the game and initialize the variables. """
        self.manager.enable()
        self.left_side_screen.clear()
        self.right_side_screen.clear()
        self.history_labels.clear()
        self._not_skippable = True
        self.input_text_check = constants.INPUT_CHECK_DEFAULT.copy()
        arcade.set_background_color(arcade.color.AFRICAN_VIOLET)
        height_25perc  = (self.window.height * 25)/100
        self.text_area = UITypingTextArea(
                               width=self.window.width-10,
                               height=height_25perc,
                               text="")
        self.title_area= UILabel(width=self.window.width-10, height=30,
                                    text="")
        self.input_text = UIInputText(width=self.window.width-10,
                               height=height_25perc)
        self.box_dlg.add(UIBorder(self.title_area))
        self.box_dlg.add(self.text_area)
        self.manager.add(UIAnchorWidget(
                anchor_x="left", anchor_y="bottom", child=UIBorder(self.box_dlg)))
        self.manager.add(UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box))
        path_dialog = arcade.resources.resolve_resource_path(path_dialog)
        self.setup_dialog(path_dialog)
        self.set_color_text(constants.DEFAULT_COLOR_TEXT)
        self._next_step()

    def set_color_text(self, color: arcade.RGBA):
        self.text_area.doc.set_style(0, 12,
                                     dict(color=arcade.get_four_byte_color(color)))
        self.title_area.label.document.set_style(0,
                        len(self.title_area.text),
                        dict(color=arcade.get_four_byte_color(color)))
        self.input_text.doc.set_style(0, 12,
                                     dict(color=arcade.get_four_byte_color(color)))

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
        arcade.draw_texture_rectangle(self.window.width//2, self.window.height//2,
            self.window.width, self.window.height, self.background_texture)
        for idx, sprite_left in enumerate(self.left_side_screen):
            sprite_left.bottom = self.box_dlg.top
            sprite_left.left = 10 + idx*5
            sprite_left.draw()
        for idx, sprite_right in enumerate(self.right_side_screen):
            sprite_right.bottom = self.box_dlg.top
            sprite_right.right  = self.window.width - 10 - idx*5
            sprite_right.draw()
        if not self.hide_gui:
            self.manager.draw()
        if self._skip_dlg:
            arcade.draw_text("SKIPPING", 1, 1, font_size=15)
    def jmp_next_dialog(self, label:str)->None:
        """Generic implementation of jump action between a dialog block to another"""
        assert label in self.dialog.blocks
        self.history_labels.append(label)
        self.ptr_blocks = iter(self.dialog.blocks[label].block)
        self.v_box.clear()
    def __jump_next_dialog(self, event: UIOnClickEvent) -> None:
        jmp_label = self.__jump_next[event.source.text]
        self.jmp_next_dialog(jmp_label)
        self._next_step()

    def _remove_pg_from_lists(self, sprite: CharacterVN) -> None:
        if sprite in self.left_side_screen:
            self.left_side_screen.remove(sprite)
        elif sprite in self.right_side_screen:
            self.right_side_screen.remove(sprite)

    def __interpreting_action(self, sprite:CharacterVN, tok:List[str]) -> None:
        """Actions are defined with 2 words, action and argument"""
        assert len(tok) == 2
        assert tok[0] in self.__strategy_action
        self.__strategy_action[tok[0]](sprite, tok[1])

    def __action_video(self, name_pg:str, actions_char:List[str]) -> None:
        if name_pg not in self.__dict_char:
            sprite = None
        else:
            sprite = self.__dict_char[name_pg]
        for action in actions_char:
            tok = action.split()
            self.__interpreting_action(sprite, tok)

    def __generate_regular_menu(self, cases:ast_dialog.BlockInstr) -> None:
        for case in cases:
            button = UIFlatButton(text=case.label, width=200)
            self.__jump_next[case.label] = case.block[0].name
            self.v_box.add(button.with_space_around(bottom=1))
            button.on_click = self.__jump_next_dialog
            self.v_box.add(button)

    def __generate_request(self, req_node:ast_dialog.Request) -> None:
        self.box_dlg.remove(self.text_area)
        self.box_dlg.add(self.input_text)
        self._not_skippable = False
        self._skip_dlg      = False
        self.input_text_check["check"] = True
        self.input_text_check["evt"]   = req_node.event_name
        self.input_text_check["type"]  = req_node.type_request

    def _next_step(self) -> None:
        try:
            node_dlg = next(self.ptr_blocks)
        except StopIteration:
            self._not_skippable = False
            self.__dialog_end = True
            self.on_ended(self)
            return
        self._not_skippable = True
        if isinstance(node_dlg, ast_dialog.Dialog):
            self.title_area.text= node_dlg.char_name
            self.text_area.set_text(node_dlg.text)
            self.__action_video(node_dlg.char_name, node_dlg.action)
        elif isinstance(node_dlg, ast_dialog.Menu):
            self._skip_dlg = False
            self._not_skippable = False
            if node_dlg.type_menu != "regular":
                raise NotImplementedError(
                    f"{node_dlg.type_menu} menu is not implemented")
            self.__generate_regular_menu(node_dlg.cases)
        elif isinstance(node_dlg, ast_dialog.Request):
            self._skip_dlg = False
            self._not_skippable = False
            if node_dlg.type_request not in ["text", "int"]:
                raise NotImplementedError(
                    f"{node_dlg.type_request} request is not implemented")
            self.__generate_request(node_dlg)

    def update(self, delta_time: float) -> None:
        if self._skip_time<=constants.SKIP_TIME:
            self._skip_time += delta_time
        elif self._skip_dlg:
            self._next_step()
            self._skip_time = 0.0
        return super().update(delta_time)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol not in self.input_handler.command_layout:
            return
        self.input_handler.command_layout[symbol](self)

__author__ = "dfdeangelis"
