"""filename: parser_dialog.py
used to develop parse and generate the Dialog Tree.
author: Domenico Francesco De Angelis
"""
import json
from typing import List
from graphic_novel.dlg_parser import ast_dialog

MENU_TOKEN    = "menu"
CHAR_TOKEN    = "char"
BLOCK_TOKEN   = "block"
CHOICE_TOKEN  = "choice"
TXT_MENU_TOKEN="txt"
JMP_MENU_TOKEN="jmp"

class ParseExcept(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.label = kwargs["label"]
        self.what  = kwargs["what"]

def _parse_menu(name_block:str, menu:dict) -> ast_dialog.Menu:
    menu_inst = ast_dialog.Menu()
    def __check_token(dc_menu:dict, key:str):
        if key not in dc_menu:
            raise ParseExcept(f"menu format in label: {name_block}",
                                label=name_block,
                                what=f"{key} miss")
    __check_token(menu, CHOICE_TOKEN)
    menu_inst.type_menu = menu[MENU_TOKEN]
    if len(menu[CHOICE_TOKEN]) == 0:
        raise ParseExcept(f"menu format in label: {name_block}",
                                label=name_block,
                                what="empty menu")
    for choice in menu[CHOICE_TOKEN]:
        __check_token(choice, TXT_MENU_TOKEN)
        __check_token(choice, JMP_MENU_TOKEN)
        choice_dlg = ast_dialog.BlockInstr(choice["txt"],
                                        [ast_dialog.Jump(choice["jmp"])])
        menu_inst.cases.append(choice_dlg)
    return menu_inst

def _parsing_json(filename:str, dialog_json:dict) -> ast_dialog.RootDialog:
    blocks:List[ast_dialog.BlockInstr] = []
    for name_block, block in dialog_json.items():
        instr:List[ast_dialog.Node] = []
        if BLOCK_TOKEN not in block:
            raise ParseExcept(f"No block attribute in {name_block} label",
                              label=name_block, what="no block")
        for instruction in block[BLOCK_TOKEN]:
            if isinstance(instruction[1], dict):
                if MENU_TOKEN in instruction[1]:
                    menu_inst = _parse_menu(name_block, instruction[1])
                    instr.append(menu_inst)
            else: #[str, str]
                if len(instruction) == 2:
                    actions = []
                else:
                    actions = instruction[2:]
                instr.append(ast_dialog.Dialog(instruction[0], instruction[1], actions))
        blocks.append(ast_dialog.BlockInstr(name_block, instr))
    return ast_dialog.RootDialog(filename, blocks)

def parsing(filename: str) -> ast_dialog.RootDialog:
    """Dialog system parser.
    args:
        filename: str - is the path of dialog tree described in json
    return:
        ast_dialog.RootDialog: dialog tree root
    """
    with open(filename, "r") as file:
        dialog_json = json.load(file)
    return _parsing_json(filename, dialog_json)

__author__ = "dfdeangelis"
