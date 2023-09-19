"""Unit test dialog tree parser
author: domenico francesco de angelis"""
import sys
import os
import unittest

src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, src_path)

import graphic_novel # noqa: E402

class parser_testing(unittest.TestCase):
    def test_parsing_empty_dialog(self):
        tree = graphic_novel.parser_dialog._parsing_json("dump", {})
        self.assertTrue(isinstance(
                            tree,
                            graphic_novel.ast_dialog.RootDialog)
                        )
        self.assertTrue(len(tree.blocks) == 0)
    def test_parsing_init_dialog(self):
        dialog = {"init":{"block":[["a","1"],["b","2"]]}}
        tree = graphic_novel.parser_dialog._parsing_json("dump", dialog)
        self.assertTrue(isinstance(
                            tree,
                            graphic_novel.ast_dialog.RootDialog)
                        )
        self.assertTrue(len(tree.blocks) == 1)
        self.assertTrue(isinstance(
                            tree.blocks["init"],
                            graphic_novel.ast_dialog.BlockInstr)
                        )
        init_block:graphic_novel.ast_dialog.BlockInstr = tree.blocks["init"]
        self.assertTrue(len(init_block.block) == 2)
        self.assertTrue(init_block.label == list(dialog.keys())[0])
        for idx, dialog_msg in enumerate(dialog["init"]["block"]):
            self.assertTrue(isinstance(init_block.block[idx],
                            graphic_novel.ast_dialog.Dialog))
            self.assertTrue(dialog_msg[0] == init_block.block[idx].char_name)
            self.assertTrue(dialog_msg[1] == init_block.block[idx].text)
            self.assertTrue(isinstance(init_block.block[idx].action, list))
            self.assertTrue(len(init_block.block[idx].action) == 0)
    def test_parsing_exception(self):
        dialog = {"init":{}}
        except_done = False
        try:
            graphic_novel.parser_dialog._parsing_json("dump", dialog)
        except graphic_novel.parser_dialog.ParseExcept as parse_exept:
            self.assertTrue(parse_exept.what == "no block")
            self.assertTrue(parse_exept.label == "init")
            except_done = True
        self.assertTrue(except_done)
    def test_menu_parsing(self):
        menu = {
            "menu":"regular",
            "choice":[
                {"txt":"Am I?", "jmp":"am_i"},
                {"txt":"Are you?", "jmp":"are_you"}]
               }
        menu_node = graphic_novel.parser_dialog._parse_menu("dump", menu)
        self.assertTrue(isinstance(menu_node, graphic_novel.ast_dialog.Menu))
        self.assertTrue(menu_node.type_menu == menu["menu"])
        self.assertTrue(len(menu_node.cases) == 2)
        for idx, case in enumerate(menu_node.cases):
            self.assertTrue(case.label == menu["choice"][idx]["txt"])
            self.assertTrue(isinstance(case.block, list))
            self.assertTrue(case.block[0].name == menu["choice"][idx]["jmp"])
    def _except_menu_token(self, menu:dict, token:str):
        except_done = False
        try:
            graphic_novel.parser_dialog._parse_menu("dump", menu)
        except graphic_novel.parser_dialog.ParseExcept as parse_exept:
            self.assertTrue(parse_exept.what == f"{token} miss")
            self.assertTrue(parse_exept.label == "dump")
            except_done = True
        self.assertTrue(except_done)
    def _except_empty_choice(self, menu:dict):
        except_done = False
        try:
            graphic_novel.parser_dialog._parse_menu("dump", menu)
        except graphic_novel.parser_dialog.ParseExcept as parse_exept:
            self.assertTrue(parse_exept.what == "empty menu")
            self.assertTrue(parse_exept.label == "dump")
            except_done = True
        self.assertTrue(except_done)
    def test_except_menu(self):
        menu = {"menu":"regular"}
        self._except_menu_token(menu,
                                graphic_novel.parser_dialog.CHOICE_TOKEN)
        menu["choice"] = []
        self._except_empty_choice(menu)
        menu["choice"] = [{"jmp":"label"}]
        self._except_menu_token(menu,
                                graphic_novel.parser_dialog.TXT_MENU_TOKEN)
        menu["choice"] = [{"txt":"label"}]
        self._except_menu_token(menu,
                                graphic_novel.parser_dialog.JMP_MENU_TOKEN)
        

if __name__ == "__main__":
    unittest.main()
