import numpy as np
from main import Main
from get_matrix import Matriz
from aux_methods import Separate_route,Separate_demand,\
                        Separate_time,Break_wait

n_vehicles = 0 
opt_route = []
opt_cost = 0
fobj = []
wait = []
limit_after_client = []    
truck_cap = []  # In Case of is there only one truck, write it in an array of one position, not as an integer

x = np.loadtxt("x_coord_r201.txt")
y = np.loadtxt("y_coord_r201.txt")
time_service = np.loadtxt("s_t_r201.txt")
demand = np.loadtxt("d_r201.txt")
begin_tw = np.loadtxt("begin_tw_r201.txt")
end_tw = np.loadtxt("end_tw_r201.txt")

z = Matriz(x,y)

mode = "time"
algorithm = "as"

start_op = 0
max_time_op = 1000
fleet = 100
    
for i in range(0,fleet):
    truck_cap.append(1000)
    
res = Main(z.D,z.Len,demand,begin_tw,end_tw,time_service,mode,algorithm,truck_cap,start_op,max_time_op,fleet)

##print(algorithm,"Custo da rota: ", res[0].custo)
##print(algorithm,"Veiculos usados: ",res[0].vehicles)
##print(algorithm,"Rota : ",res[0].caminho)
##print(algorithm,"Fins de Rota : ",res[0].limited) 
    
opt_route.append(res[0].caminho)
opt_cost = res[0].custo
n_vehicles = res[0].vehicles
limit_after_client = res[0].limited
fobj.append(res[1])
wait.append(res[2])

opt_route = sum(opt_route,[]) #unnest list
wait = sum(sum(wait,[]),[])   #unnest list
    
each_route = Separate_route(opt_route,limit_after_client)
each_demand = Separate_demand(each_route,demand)
each_wait = Break_wait(each_route,wait)
each_time = Separate_time(each_route,z.D,each_wait,time_service,z.Len)

print("Cada Rota : ",each_route)
print("Cada Demanda: ",each_demand)
print("Custo : ", round(opt_cost,2))    