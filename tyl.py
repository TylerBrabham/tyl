import sys

"""
TODO
  - No support for '?'
  - Add support for special symbol to indicate the end of the stack, in case one
    doesn't want to deal with the extra zeros.
  - Pad each line to be 80 characters wide. Add rows to make it 25 characters.
"""

class Tyl(object):

  def __init__(self, filename):
    self.board = self._build_board(filename)
    self.pc = '>'
    self.position = (0, 0)
    self.stack = []
    self.string_mode = False

  def __str__(self):
    string = ""
    for row in self.board:
      string += ''.join(row) + '\n'
    return string

  def _toggle_string_mode(self):
    self.string_mode = not self.string_mode

  def read(self, x, y):
    # First we should check that it exists in the board.
    return self.board[x][y]

  def _build_board(self, filename):
    unpadded_board = self._parse_file(filename)
    return self._pad_board(unpadded_board)

  def _pad_board(self, unpadded_board):
    padded_board = []
    for row in unpadded_board:
      padded_row = row + [' '] * (80 - len(row))
      padded_board.append(padded_row)

    if len(padded_row) < 25:
      for i in range(25- len(padded_row)):
        padded_board.append([' '] * 25)

    return padded_board

  def _parse_file(self, filename):
    i = 0
    board = []
    with open(filename) as f:
      for line in f:
        row = list(line.rstrip())[:80]
        board.append(row)
        i += 1
        if i == 25:
          break
    return board

  def _check_filename(self, filename):
    pass

  def _display_top(self, symbol):
    if symbol == ',':
      print str(unichr(self._pop()))
    else:
      print int(self._pop())

  def _update(self):
    if self.string_mode:
      self._update_string_mode()
    else:
      self._update_regular_mode()

  def _update_string_mode(self):
    x, y = self._update_position()
    updated_symbol = self.read(x, y)
    self._push_ascii(updated_symbol)
    return updated_symbol

  def _update_regular_mode(self):
    x, y = self._update_position()

    updated_symbol = self.read(x, y)

    if updated_symbol == '\"':
      self._toggle_string_mode()

    elif updated_symbol in "0123456789":
      self._push(int(updated_symbol))

    elif updated_symbol in "%*/+-":
      self._apply_math_operator(updated_symbol)

    elif updated_symbol in "^v<>":
      self.pc = updated_symbol

    elif updated_symbol in '.,':
      self._display_top(updated_symbol)

    elif updated_symbol == '$':
      self._pop()

    elif updated_symbol == ':':
      self._duplicate_top()

    elif updated_symbol in ',|_!':
      self._apply_boolean_operator(updated_symbol)

    elif updated_symbol == '\'':
      # This slash thing is probably wrong
      self._swap_elements()

    return updated_symbol

  def _update_position(self):
    x, y = self.position

    if self.pc == '>':
      y += 1
    elif self.pc == '<':
      y -= 1
    elif self.pc == '^':
      x -= 1
    else:
      x += 1

    x = x % 25
    y = y % 80

    self.position = x, y
    return self.position

  def _duplicate_top(self):
    a = self._pop()
    self._push(a)
    self._push(a)

  def _apply_math_operator(self, operator):
    a = self._pop()
    b = self._pop()
    if operator == '+':
      self._push(a + b)
    elif operator == '-':
      self._push(a - b)
    elif operator == '/':
      # This is not the way Befunge 93 does it
      if b == 0:
        self._push(0)
      else:
        self._push(a / b)
    elif operator == '*':
      self._push(a * b)
    elif operator == '%':
      # This is not the way Befunge 93 does it
      if b == 0:
        self._push(0)
      else:
        self._push(a % b)

  def _apply_boolean_operator(self, operator):
    if operator == '|':
      a = self._pop()
      if a == 0:
        self.pc = 'v'
      else:
        self.pc = '^'
      self._update_position()
    elif operator == '_':
      a = self._pop()
      if a == 0:
        self.pc = '>'
      else:
        self.pc = '<'
      self._update_position()
    elif operator == '!':
      a = self._pop()

      if a > 0:
        self._push(0)
      else:
        self._push(1)
    elif operator == '`':
      a = self._pop()
      b = self._pop()

      if b > a:
        self._push(1)
      else:
        self._push(0)

  def _swap_elements(self):
    a = self._pop()
    b = self._pop()

    self._push(b)
    self._push(a)

  def _pop(self):
    if len(self.stack) > 0:
      return self.stack.pop()
    else:
      return 0

  def _push_int(self, val):
    self.stack.append(val)

  def _push_ascii(self, val):
    self.stack.append(ord(val))

  def _push(self, val):
    # Make sure val is an int
    self._push_int(val) 

  def run(self):
    current_symbol = self.read(self.position[0], self.position[1])
    i = 0
    while current_symbol != '@' and i < 100:
      print self.stack
      current_symbol = self._update()
      i += 1

def main(argv):
  filename = argv[1]
  tyl = Tyl(filename)
  tyl.run()

if __name__ == "__main__":
  main(sys.argv)