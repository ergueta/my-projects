from sa_oop import *

class Main:
    def run(self,matrix):
        sa = SimulatedAnnealing(100,20,0.98,matrix,len(matrix))
        res = sa.Optimizer()
        return res

if __name__ == "__main__":
    matrix = [[0,1,2,3,4,5],[1,0,3,2,2,2],[5,5,0,1,3,4],[10,1,2,0,4,5],[1,5,3,2,0,2],[5,5,20,1,3,0]]
    output = Main().run(matrix)
    print(output)