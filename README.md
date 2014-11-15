tyl
================================================================================

An interpreter for the language tyl. tyl is a dialect of befunge which allows for two stacks. The reason this is interesting is that a Push Down Automaton with two stacks can simulate the read/write head of a Turing Machine.

Initially, tyl should be able to run any Befunge-93 code. I may also remove the ability to use the 'p' and 'g' commands, forcing the user to store whatever they need in one of the two stacks.

Run tyl by typing:
  
  python tyl.py filename

I use the extension .ty for tyl programs.