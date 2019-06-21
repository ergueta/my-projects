from tabusearch import *

class Main:
    def run(self,matrix):
        ts = TS(len(matrix),200,5,matrix)
        res = ts.Optimizer()
        return res

if __name__ == "__main__":
    matrix = [[0,1,2,3,4,5],[1,0,3,2,2,2],[5,5,0,1,3,4],[10,1,2,0,4,5],[1,5,3,2,0,2],[5,5,20,1,3,0]]
    output = Main().run(matrix)
    print(output)