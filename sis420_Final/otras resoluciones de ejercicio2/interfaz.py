import tkinter as tk
from Nodo import Nodo
from Rompecabezas import Tablero

moves = [[[1, 3], [0, 2, 6], [1, 3, 7], [2, 4, 8], [3, 9]],
         [[0, 6, 10], [1, 5, 7, 11], [2, 6, 8, 12], [3, 7, 9, 13], [4, 8, 14]],
         [[5, 11, 15], [6, 10, 12, 16], [7, 11, 13, 17], [8, 12, 14, 18], [9, 13, 19]],
         [[10, 16], [11, 15, 17], [12, 16, 18], [13, 17, 19], [14, 18]]]

class App(tk.Tk):
    def __init__(self, *args, **kargs):
        tk.Tk.__init__(self, *args, **kargs)
        self.geometry('850x700')
        self.container = tk.Frame(self, bg='red')
        self.container.place(relx=0, rely=0, relwidth=1, relheight=1)
        fTab = Frame_Rompecabezas(self.container, self)
        fTab.tkraise()

class Ficha:
    contador = 0
    def __init__(self, r, c, n, frame):
        self.frame = frame
        self.r = r
        self.c = c
        self.n = n
        self.contador = Ficha.contador
        Ficha.contador += 1
        if n != 0:
            self.button = tk.Button(self.frame, text=str(self.n), font=("Impact", 20), borderwidth=0.5, relief='solid', command=lambda: frame.move(self.contador, self.r, self.c))
        else:
            self.button = tk.Button(self.frame, text='', font=("Impact", 20), borderwidth=0.5, relief='solid', command=lambda: frame.move(self.contador, self.r, self.c))
        self.button.place(relx=1/26 + self.c*(4/13), rely=0.05 + self.r*(1/4), relheight=1/4, relwidth=4/13)

class Frame_Rompecabezas(tk.Frame):
    def __init__(self, parent, root):
        self.root = root
        tk.Frame.__init__(self, parent, bg='black')
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        b_solve = tk.Button(self, text='Resolver', command=lambda: self.solve(), background='green', fg='white', padx=10, pady=10)
        b_solve.place(relx=0.3, rely=0.85, relwidth=0.4, relheight=0.1)
        self.nums = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 0]]
        self.aux_Rompecabezas = Tablero(self.nums)

        self.fichas = []
        for ir, r in enumerate(self.nums):
            for ic, c in enumerate(r):
                aux = Ficha(ir, ic, c, self)
                self.fichas.append(aux)

    def move(self, icontador, fr, fc):
        er, ec = self.aux_Rompecabezas.empty()
        if icontador in moves[er][ec]:
            if er == fr:
                if fc < ec:
                    auxm = 'l'
                else:
                    auxm = 'r'
            else:
                if fr < er:
                    auxm = 'u'
                else:
                    auxm = 'd'

            self.aux_Rompecabezas.make_moves(auxm)
            self.actualizar(self.aux_Rompecabezas.nums)

    def actualizar(self, nums):
        aux = 0
        for ir, r in enumerate(nums):
            for ic, c in enumerate(r):
                if c != 0:
                    self.fichas[aux].button.config(text=str(c), background='black', fg='white', borderwidth=1, relief='solid')
                else:
                    self.fichas[aux].button.config(text='', background='white', bd=1, highlightcolor='white', borderwidth=1, relief='solid')
                aux += 1

if __name__ == '__main__':
    app = App()
    app.mainloop()
