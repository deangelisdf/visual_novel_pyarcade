"""Unit test graphic novel view
author: domenico francesco de angelis"""
import sys
import os
import unittest
from unittest import mock
import arcade.application

src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, src_path)

import graphic_novel # noqa: E402
from graphic_novel.dlg_parser import ast_dialog # noqa: E402

def get_dummy_shader_program():
    """
    Provide a dummy getter to monkeypatch getters for default shaders.

    By default, batchable objects create or re-use a default shader
    program. This is usually done through a ``get_default_shader``
    function on their implementing module. If no GL context exists,
    calling that function creates one, which risks non-drawing tests
    failing or running slower than optimal.

    Avoid that by passing this fixture to local monkey patching fixtures
    in module-specific single test files or conftest.py instances for
    test modules::

        # Example from ./shapes/conftest.py

        @fixture(autouse=True)  # Force this to be used for every test in the module
        def monkeypatch_default_shape_shader(monkeypatch, get_dummy_shader_program):
            monkeypatch.setattr(
                'pyglet.shapes.get_default_shader',
                 get_dummy_shader_program)

    """
    # A named function instead of a lambda for clarity in debugger views.
    def _get_dummy_shader_program(*args, **kwargs):
        return mock.MagicMock()

    return _get_dummy_shader_program

arcade.application._window = get_dummy_shader_program()
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
