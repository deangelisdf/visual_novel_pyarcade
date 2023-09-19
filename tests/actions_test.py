"""Unit test actions
author: domenico francesco de angelis"""
import sys
import os
import unittest
from unittest.mock import Mock
import arcade

src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, src_path)

import graphic_novel # noqa: E402
import graphic_novel.dlg_parser.ast_dialog as ast_dlg # noqa: E402
from graphic_novel import actions # noqa: E402

class StubText:
    """Used as Mock of arcade UIText and UILabel"""
    def __init__(self):
        self.text  = ""
        self.doc   = Mock()
        self.label = Mock()
    def set_text(self,txt):
        self.text = txt

#Global definition to enabling tests
window  = arcade.open_window(100, 100)
gn_view = graphic_novel.GraphicNovel()
gn_view.text_area = StubText()
gn_view.title_area= StubText()
gn_view.dialog = ast_dlg.RootDialog(
                        "dump",
                        [ast_dlg.BlockInstr("init", []),
                         ast_dlg.BlockInstr("label", [
                             ast_dlg.Dialog("title_label","txt_label", "")
                             ])])
texture:arcade.Texture = arcade.texture.make_circle_texture(30, arcade.color.AERO_BLUE)
dict_char = {"Me":arcade.Sprite(texture=texture)}
gn_view.characters = dict_char

#global variable test EVENT
called_event = False

#TESTs

class actions_testing(unittest.TestCase):
    def test_move(self):
        move_action = actions.MoveAction(gn_view)
        move_action(texture, "left")
        self.assertTrue(len(gn_view.left_side_screen)  == 1)
        self.assertTrue(len(gn_view.right_side_screen) == 0)
        self.assertTrue(gn_view.left_side_screen[0] is texture)
        move_action(texture, "right")
        self.assertTrue(len(gn_view.right_side_screen) == 1)
        self.assertTrue(len(gn_view.left_side_screen)  == 0)
        self.assertTrue(gn_view.right_side_screen[0] is texture)
        move_action(texture, "left")
        self.assertTrue(len(gn_view.left_side_screen)  == 1)
        self.assertTrue(len(gn_view.right_side_screen) == 0)
        self.assertTrue(gn_view.left_side_screen[0] is texture)
        move_action(texture, "asdf")
        self.assertTrue(len(gn_view.left_side_screen)  == 0)
        self.assertTrue(len(gn_view.right_side_screen) == 0)
    def test_jump(self):
        jmp = actions.JmpAction(gn_view)
        jmp(None, "label")
        self.assertTrue(gn_view.history_labels[-1] == "label")
        self.assertTrue(gn_view.title_area.text == "title_label")
        self.assertTrue(gn_view.text_area.text  == "txt_label")
    def test_alpha(self):
        except_ve = False
        alpha = actions.SetAlphaAction(gn_view)
        alpha(dict_char["Me"], "50")
        self.assertTrue(dict_char["Me"].alpha == 50)
        try:
            alpha(dict_char["Me"], "asdf")
        except ValueError:
            except_ve = True
        self.assertTrue(except_ve)
    def test_event(self):
        global called_event
        called_event = False
        def mock_ev1(gn: graphic_novel.GraphicNovel):
            global called_event
            called_event = True
            return 1
        evt = actions.EventAction(gn_view)
        gn_view.add_event("ev1", mock_ev1)
        t = evt(None, "ev1")
        self.assertTrue(t == 1)
        self.assertTrue(called_event)
    def test_RestartAction(self):
        restart = actions.RestartAction(gn_view)
        gn_view.add_filter_video(None)
        gn_view.left_side_screen.append(None)
        gn_view.right_side_screen.append(None)
        restart(None, "all")
        self.assertTrue(len(gn_view.left_side_screen)  == 0)
        self.assertTrue(len(gn_view.right_side_screen) == 0)
        self.assertTrue(len(gn_view.video_filters)     == 0)

if __name__ == "__main__":
    unittest.main()
