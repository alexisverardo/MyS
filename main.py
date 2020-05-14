from __future__ import print_function

import threading
from tkinter import *
import copy
import random
import itertools
import time
import os
from tkinter.ttk import Combobox
FINISH = False
INIT = False
UNIX = True  # Change if using Windows

clear = lambda: os.system('clear') if UNIX else os.system('cls')


class GameOfLife(object):

    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols

        row_life = lambda: [random.randint(0, 1) for n in range(self.cols)]
        self.game = [row_life() for n in range(self.rows)]

        self.life = 1
        self.dead = 1

    def __str__(self):

        table = ''
        for row in self.game:
            for cell in row:
                table += '▓ ' if cell else '░ '
            table += '\n'

        # table += "Life: {0} Dead: {1}".format(self.life, self.dead)
        return table

    def evaluate(self, row, col):

        distance = list(set(itertools.permutations([-1, -1, 1, 1, 0], 2)))
        into_table = lambda x, y: (x in range(self.rows) and y in range(self.cols))

        total = 0
        for r, c in distance:
            if into_table(r + row, c + col):
                total += self.game[r + row][c + col]
        return total

    def test(self):

        gameaux = copy.deepcopy(self.game)
        self.life = 0
        self.dead = 0

        for r in range(self.rows):
            for c in range(self.cols):
                total = self.evaluate(r, c)

                if (total < 2 or total > 3) and gameaux[r][c]:
                    gameaux[r][c] = 0
                    self.dead += 1
                elif total == 3 and not gameaux[r][c]:
                    gameaux[r][c] = 1
                    self.life += 1

        self.game = copy.deepcopy(gameaux)

window = Tk()
window.geometry('350x200')
window.title("JUEGO DE LA VIDA")
#FILAS
lblF = Label(window, text="FILAS ")

lblF.grid(column=0, row=0)

comboF = Combobox(window)

comboF['values']= (10,20,30,40,50,60,70,80,90, 100)

comboF.current(1) #set the selected item

comboF.grid(column=2, row=0)
#COLUMNAS
lblC = Label(window, text="COLUMNAS ")

lblC.grid(column=0, row=1)

comboC = Combobox(window)

comboC['values']= (10,20,30,40,50,60,70,80,90, 100)

comboC.current(1) #set the selected item

comboC.grid(column=2, row=1)
var = StringVar()
var.set('')
lbl = Label(window, textvariable=var)
lbl.grid(column=10, row=20)

def workGame():
    global FINISH
    global INIT
    rows, cols = int(comboF.get()), int(comboC.get())
    game = GameOfLife(rows, cols)
    iterations = 0
    while True:
        if FINISH:
            FINISH = False
            INIT = False
            break
        try:
            game.test()
            var.set(game)
            window.update_idletasks()
            time.sleep(1)
            iterations += 1

        except KeyboardInterrupt:
            FINISH = False
            INIT = False
            break
def clicked():
    global INIT
    global FINISH
    if INIT:
        FINISH = True
    time.sleep(1)
    t = threading.Thread(target=workGame)
    t.start()
    INIT = True
btn = Button(window, text="INICIAR", command=clicked)

btn.grid(column=2, row=3)

window.mainloop()



