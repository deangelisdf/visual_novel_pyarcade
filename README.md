# graphic_novel_pyarcade
Little framework to create a graphic novel with python arcade https://github.com/pythonarcade/arcade
##
# Feature
 - character managment
 - event managment
 - dialog based on json format

##
# How to use
Steps:
1. Define characters. Those are defined by names (string) and an image (arcade.Sprite).
2. setup the view, you should give him, as parameter, the json dialog path.
3. define the events. If exist.
4. Set the new view and use it

Please look also the emample/simple_example.py

## How make a dialog
The objective of this framework is to achieve it as simple task.
What do you need?
1. Create a new json file and create an object insiede
2. The attributes of this first object must be see as LABEL. Well-Know: "init" is the dialog entry pointer
3. Each Label, contain an attribute called "block" (this is an array)
4. Each array element, Is composed always by:
     - name character, as a string (case sensitive)
     - message
         - can be a string (that mean what the character said)
         - can be a menu (an object)
     - actions (if the message type is not a menu)
         - Those are composed by two words: ACTION ARGUMENT
         - The actions implemented are: move, alpha, restart, jmp
      
How to write a menu?
The menu is an object composed by two attributes: "menu" (with only a value implemented: regular) and "choice" an array of objects composed as follow: "txt" is a string containing the text and "jmp" the label where you want to jump after the selection of choice
