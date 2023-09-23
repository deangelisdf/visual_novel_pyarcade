"""Unit test graphic novel view
author: domenico francesco de angelis"""
import sys
import os
import unittest
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, src_path)

import graphic_novel # noqa: E402
from graphic_novel.dlg_parser import ast_dialog # noqa: E402

gn_view = graphic_novel.GraphicNovel()
class gn_testing(unittest.TestCase):
    def test_jmp_next_dialog(self):
        block = ast_dialog.BlockInstr("init", [ast_dialog.Dialog("e", "1", []),
                                               ast_dialog.Dialog("e", "2", [])])
        dialog_tree = ast_dialog.RootDialog("", [block])
        gn_view.dialog = dialog_tree
        gn_view.jmp_next_dialog("init")
        self.assertTrue(gn_view.history_labels == ["init"])
        dlg = next(gn_view.ptr_blocks)
        self.assertTrue(isinstance(dlg, ast_dialog.Dialog))
        self.assertTrue(dlg.text == "1" and
                        dlg.char_name == "e" and
                        dlg.action == [])
        dlg = next(gn_view.ptr_blocks)
        self.assertTrue(isinstance(dlg, ast_dialog.Dialog))
        self.assertTrue(dlg.text == "2" and
                        dlg.char_name == "e" and
                        dlg.action == [])

if __name__ == "__main__":
    unittest.main()
