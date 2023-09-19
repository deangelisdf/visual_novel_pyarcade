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

if __name__ == "__main__":
    unittest.main()
