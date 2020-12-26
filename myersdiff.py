import copy 
import argparse
from enum import Enum
from os import path

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

# cli
def parse_args():
    parser = argparse.ArgumentParser(description='Myers Differ')

    parser.add_argument('left',  help='left file path or string')
    parser.add_argument('right', help='right file path or string')
    
    parser.add_argument('-t', 
        dest='type', 
        type=str,  
        default='str',
        choices=['file', 'str'],
        help='input type: file or string (default: %(default)s)')

    return parser.parse_args()

def read_files():
    if path.isfile(args.left) == False:
        print(f'Invalid file path: {args.left}')
        return ([], [])

    elif path.isfile(args.right) == False:
        print(f'Invalid file path: {args.right}')
        return ([], [])

    else:
        return ( open(args.left, 'r').read().splitlines(), 
                 open(args.right, 'r').read().splitlines()
                )

if __name__ == "__main__":
    args = parse_args()

    listX, listY = [], []

    if args.type == "str":
        listX = [x for x in args.left]
        listY = [x for x in args.right]

    elif args.type == "file":
        listX, listY = read_files()
    
    if len(listX) > 0 or len(listY) > 0:
        Myersdiffer(listX, listY).print_diff()