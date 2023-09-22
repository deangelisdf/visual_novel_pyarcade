"""filename: layout_commands.py
Implementation of keyboard commands.
The goal to reach decouple user command to View implementation

author: Domenico Francesco De Angelis
"""
from graphic_novel import constants

class layout_command:
    def __init__(self):
        self.name = "<N/A>"
class next_dlg_command(layout_command):
    def __init__(self):
        self.name = "Next Dialog"
    """Next Dialog"""
    def __call__(self, machine) -> None: # noqa: F821
        if machine.input_text_check["check"]:
            if machine.input_text_check["type"] == "int":
                try:
                    int(machine.input_text.text, 10)
                except ValueError:
                    machine.input_text.text = "0"
            machine.event_table[machine.input_text_check["evt"]](machine)
            machine.input_text_check = constants.INPUT_CHECK_DEFAULT.copy()
            machine.input_text.text  = ""
            machine._not_skippable   = True
            machine.box_dlg.remove(machine.input_text)
            machine.box_dlg.add(machine.text_area)
        machine._next_step()

class skip_dlg_command(layout_command):
    """Skip dialogs"""
    def __init__(self):
        self.name = "Skip dialog"
    def __call__(self, machine) -> None: # noqa: F821
        if machine._not_skippable:
            machine._skip_dlg = not machine._skip_dlg

class hide_gui_command(layout_command):
    """Hide gui"""
    def __init__(self):
        self.name = self.__doc__
    def __call__(self, machine) -> None:
        machine.hide_gui = not machine.hide_gui

__author__ = "dfdeangelis"
