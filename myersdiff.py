import copy 
from enum import Enum
from functools import reduce

class EditType(Enum):
    EQL = 0
    INS = 1
    DEL = 2

class Myersdiffer:
    def __init__(self, A, B):
        self.A = list(A)
        self.B = list(B)

    def _shortest_path(self):
        lenA, lenB = len(self.A), len(self.B)
        max_edit = lenA + lenB
        V = [0 for _ in range(2*max_edit+1)]
        T = []
        
        for D in range(max_edit+1):
            T.append(copy.deepcopy(V))
            for k in range(-D, D+1, 2):
                x = V[k+1] if (k == -D or (k != D and V[k-1]<V[k+1])) else V[k-1]+1
                y = x - k
                while (x < lenA and y < lenB and self.A[x] == self.B[y]):
                    x += 1
                    y += 1

                V[k] = x
                if x >= lenA and y >= lenB:
                    return T
        return T

    def _line_diff(self, x, y, x_prev, y_prev):
        #print((x_prev,y_prev), "=>", (x, y))
        if x == x_prev:
            return (-1, y_prev+1, EditType.INS)
        elif y == y_prev:
            return (x_prev+1, -1, EditType.DEL)
        else:
            return (x_prev+1, y_prev+1, EditType.EQL)


    def _backtrack(self, trace):
        x = len(self.A)
        y = len(self.B)

        for (D, v) in reversed(list(enumerate(trace))):
            k = x - y
            k_prev = k+1 if (k == -D or (k != D and v[k-1]<v[k+1])) else k-1
            x_prev = v[k_prev]
            y_prev = x_prev - k_prev

            while x > x_prev and y > y_prev:
                yield self._line_diff(x,y,x-1,y-1)
                x-=1
                y-=1

            if D > 0:
                yield self._line_diff(x,y,x_prev,y_prev)

            x = x_prev
            y = y_prev

    def diff(self):
        return self._backtrack(self._shortest_path())
    
    def print_diff(self):
        view = {
            EditType.EQL.value: (" ", "\033[39m"),
            EditType.INS.value: ("+", "\033[92m"),
            EditType.DEL.value: ("-", "\033[91m"),
        }
        
        result = ""
        for (old, new, editType) in self.diff():
            sign, color = view[editType.value]

            if editType == EditType.DEL:
                value = self.A[old-1]
            else:
                value = self.B[new-1]

            line = "{}{} {}\n".format(color, sign, value)
            result = line + result
        print(result + "\033[39m")

listX = [i for i in "ABCABBA"]
listY = [i for i in "CBABAC"]
differ = Myersdiffer(listX, listY)

for v in differ.diff():
    print(v)
differ.print_diff()