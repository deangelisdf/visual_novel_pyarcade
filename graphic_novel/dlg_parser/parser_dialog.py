"""filename: parser_dialog.py
used to develop parse and generate the Dialog Tree.
author: Domenico Francesco De Angelis
"""
import json
from graphic_novel.dlg_parser import ast_dialog

MENU_TOKEN = "menu"
CHAR_TOKEN = "char"

def parsing(filename: str) -> ast_dialog.RootDialog:
    """Dialog system parser.
    args:
        filename: str - is the path of dialog tree described in json
    return:
        ast_dialog.RootDialog: dialog tree root
    """
    with open(filename, "r") as file:
        dialog_json = json.load(file)
    blocks = []
    for name_block, block in dialog_json.items():
        instr = []
        for instruction in block["block"]:
            if isinstance(instruction[1], dict):
                if MENU_TOKEN in instruction[1]:
                    menu_inst = ast_dialog.Menu()
                    for choice in instruction[1]["choice"]:
                        choice_dlg = ast_dialog.BlockInstr(choice["txt"],
                                                        ast_dialog.Jump(choice["jmp"]))
                        menu_inst.cases.append(choice_dlg)
                    instr.append(menu_inst)
            else: #[str, str]
                if len(instruction) == 2:
                    actions = []
                else:
                    actions = instruction[2:]
                instr.append(ast_dialog.Dialog(instruction[0], instruction[1], actions))
        blocks.append(ast_dialog.BlockInstr(name_block, instr))
    return ast_dialog.RootDialog(filename, blocks)

__author__ = "dfdeangelis"
