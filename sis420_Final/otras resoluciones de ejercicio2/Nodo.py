from Rompecabezas import Tablero
from copy import deepcopy

class Nodo: 
    def __init__(self, father=None, nums=[], dir='l'):
        self.father = father
        if self.father == None:
            self.Rompecabezas = Tablero(nums)
        else:
            self.Rompecabezas = deepcopy(self.father.Rompecabezas)
            self.Rompecabezas.make_moves(dir=dir)

    def set_chids(self):
        self.childs = []
        for _dir in self.Rompecabezas.moves():
            auxN = Nodo(father=self, dir=_dir)
            self.childs.append(auxN)

    def breadth_first(root):
        agenda = [root]
        historial = []

        it = 0
        while True:
            it+=1

            if agenda[0].Tablero.isSolution():
                break
            else:
                agenda[0].set_chids()
                aux_childs = agenda[0].childs
                historial.append(agenda[0].Tablero.nums)
                agenda.pop(0)

                for ci in aux_childs:
                    if not is_in(historial, ci.Tablero.nums):
                        agenda += [ci]
                print('iteraciones: ', it, 'len agenda', len(agenda), 'len historial', len(historial))


        print(' solucion encontrada (', it, 'iteraciones)')
        return agenda[0]
    
    def solve(root):
        sol= breadth_first(root)

        steps = []
        aux= sol
        while True:
            steps.insert(0,aux)
            aux = aux.father
            if aux == None:
                break
        return steps