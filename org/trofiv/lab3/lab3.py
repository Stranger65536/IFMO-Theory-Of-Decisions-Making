# coding=UTF8
from copy import deepcopy
from tkinter import Button, Tk


class Board:
    """
    Represents gaming board
    """

    def __init__(self, other=None):
        self.player = 'X'
        self.opponent = 'O'
        self.empty = '.'
        self.size = 3
        self.fields = {}
        for y in range(self.size):
            for x in range(self.size):
                self.fields[x, y] = self.empty
        # copy constructor
        if other:
            self.__dict__ = deepcopy(other.__dict__)

    def move(self, x, y):
        """
        Returns board after applied movement
        :param x: row
        :param y: column
        :return: the same board after applied movement with current move
        set to the opposite player
        """
        board = Board(self)
        board.fields[x, y] = board.player
        (board.player, board.opponent) = (board.opponent, board.player)
        return board

    """
    Calculates the best movement of returns that game is 
    already won or tied
    :param player: True if calculate movement for PC, False for human
    """

    def _minimax(self, player):
        if self.won():
            if player:
                return -1, None
            else:
                return +1, None
        elif self.tied():
            return 0, None
        elif player:
            best = (-2, None)
            for x, y in self.fields:
                if self.fields[x, y] == self.empty:
                    value = self.move(x, y)._minimax(not player)[0]
                    if value > best[0]:
                        best = (value, (x, y))
            return best
        else:
            best = (+2, None)
            for x, y in self.fields:
                if self.fields[x, y] == self.empty:
                    value = self.move(x, y)._minimax(not player)[0]
                    if value < best[0]:
                        best = (value, (x, y))
            return best

    def best(self):
        """
        Returns the best movement by the minimax algo
        :return: tuple of the best movement
        """
        return self._minimax(True)[1]

    def tied(self):
        """
        Returns whether game is tied
        :return: True if game is tied, False otherwise
        """
        for (x, y) in self.fields:
            if self.fields[x, y] == self.empty:
                return False
        return True

    def won(self):
        """
        Returns winning positions on the board if there is,
        None otherwise
        :return: List of tuples represent winning stroke, None otherwise
        """
        # horizontal
        for y in range(self.size):
            winning = []
            for x in range(self.size):
                if self.fields[x, y] == self.opponent:
                    winning.append((x, y))
            if len(winning) == self.size:
                return winning
        # vertical
        for x in range(self.size):
            winning = []
            for y in range(self.size):
                if self.fields[x, y] == self.opponent:
                    winning.append((x, y))
            if len(winning) == self.size:
                return winning
        # diagonal
        winning = []
        for y in range(self.size):
            x = y
            if self.fields[x, y] == self.opponent:
                winning.append((x, y))
        if len(winning) == self.size:
            return winning
        # other diagonal
        winning = []
        for y in range(self.size):
            x = self.size - 1 - y
            if self.fields[x, y] == self.opponent:
                winning.append((x, y))
        if len(winning) == self.size:
            return winning
        # default
        return None

    def __str__(self):
        string = ''
        for y in range(self.size):
            for x in range(self.size):
                string += self.fields[x, y]
            string += "\n"
        return string


class GUI:
    """
    Describes UI state and binds actions to the Board
    """

    def __init__(self):
        self.app = Tk()
        self.app.title('TicTacToe')
        self.app.resizable(width=False, height=False)
        self.board = Board()
        self.buttons = {}
        for x, y in self.board.fields:
            button = Button(
                self.app,
                command=lambda f_x=x, f_y=y: self.move(f_x, f_y),
                width=2,
                height=1)
            button.grid(row=y, column=x)
            self.buttons[x, y] = button
        button = Button(
            self.app,
            text='reset',
            command=lambda: self.reset())
        button.grid(row=self.board.size + 1,
                    column=0,
                    columnspan=self.board.size,
                    sticky="WE")
        self.update()

    def reset(self):
        """
        Resets board to the initial state
        """
        self.board = Board()
        self.update()

    def move(self, x, y):
        """
        Performs move on board
        :param x: row
        :param y: column
        """
        self.app.config(cursor="watch")
        self.app.update()
        self.board = self.board.move(x, y)
        self.update()
        move = self.board.best()
        if move:
            self.board = self.board.move(*move)
            self.update()
        self.app.config(cursor="")

    def update(self):
        """
        Pre-render function
        """
        for (x, y) in self.board.fields:
            text = self.board.fields[x, y]
            self.buttons[x, y]['text'] = text
            self.buttons[x, y]['disabledforeground'] = 'black'
            if text == self.board.empty:
                self.buttons[x, y]['state'] = 'normal'
            else:
                self.buttons[x, y]['state'] = 'disabled'

        winning = self.board.won()
        if winning:
            for x, y in winning:
                self.buttons[x, y]['disabledforeground'] = 'red'
            for x, y in self.buttons:
                self.buttons[x, y]['state'] = 'disabled'
        for (x, y) in self.board.fields:
            self.buttons[x, y].update()

    def mainloop(self):
        """
        Main application loop
        """
        self.app.mainloop()


if __name__ == '__main__':
    GUI().mainloop()
