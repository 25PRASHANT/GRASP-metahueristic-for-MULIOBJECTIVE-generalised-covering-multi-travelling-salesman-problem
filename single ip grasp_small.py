from gurobipy import*
import os
import xlrd
import numpy as np
from numpy import inf
from scipy import spatial
import numpy
from sklearn.metrics.pairwise import euclidean_distances
import math
import time

iteration = 1000
n_facility = 16         ####### 1 PLUS ACTUAL NO OF FACILITES
n_cust=35
maximum_distance=100
n_salesman=2
#limit=n_facility//3
limit=5
#break_limit=50

facility_cordinate={}
cust_cordinate={}

demand = np.ones((n_cust))

book = xlrd.open_workbook(os.path.join("1.xlsx"))
sh = book.sheet_by_name("Sheet1")

i = 1
l=0
for i in range(1,n_facility+1):  
    sp = sh.cell_value(i,1)
    sp2 = sh.cell_value(i,2)
    sp1=(sp,sp2)
    facility_cordinate[l]=(sp1)
    l=l+1
j=0
for i in range(n_facility+1,n_cust+1+n_facility):  
    sp = sh.cell_value(i,1)
    sp2 = sh.cell_value(i,2)
    sp1=(sp,sp2)
    cust_cordinate[j]=sp1  
    j=j+1

demand1=[]
j=0
for i in range(n_facility+1,n_cust+1+n_facility):  
    sp = sh.cell_value(i,1)
    sp2 = sh.cell_value(i,2)
    sp1=(sp,sp2)
    cust_cordinate[j]=sp1 
    sp3=sh.cell_value(i,3)
    demand1.append(sp3)
    j=j+1
demand=np.array(demand1) 
    
def calculate_dist(x1, x2):
    eudistance = spatial.distance.euclidean(x1, x2)
    return(eudistance)

f_dist=[]
     
for i in facility_cordinate:
    facility_dist=[]
#    a=facility_cordinate[i]
    for j in facility_cordinate:
        facility_dist.append(calculate_dist(facility_cordinate[i],facility_cordinate[j]))
    f_dist.append(facility_dist)
fac_dist=np.array(f_dist)    
customer_dist={}
for i in facility_cordinate:
    if i!=0:
        for j in cust_cordinate:
            customer_dist[i,j]=calculate_dist(facility_cordinate[i],cust_cordinate[j])

abc={}
for i in range(1,n_facility+1):
    j = 3
    xyz=[]
    while True:
        try:
            
            sp = sh.cell_value(i,j)
            xyz.append(sp)
            
            j = j + 1
            
        except IndexError:
            break
    abc[i-1]=xyz
    
final_aij=[]
for i in range(n_facility):
    a_ij=[]
    for j in range(n_facility,n_facility+n_cust):
        if j in abc[i]:
            a_ij.append(1)
        else:
            a_ij.append(0)
    final_aij.append(a_ij)
cust_dist=np.array(final_aij)
#
###
zx=[]

for i in range(n_cust):
    zx.append(i)
zx.sort()
#####################3
#######################

route_name=[]
for i in range(1,n_salesman+1):
    route_name.append("route"+str(i))
#    print(route_name)

for i in range(len(route_name)):
    a= np.ones((iteration,n_facility))
    route_name[i]=a       

local_search_route=[]
for i in range(1,n_salesman+1):
    local_search_route.append("route"+str(i))

for i in range(len(local_search_route)):
    a= np.ones((iteration,n_facility))
    local_search_route[i]=a


demand_satisfied_list=[]

for i in range(1,n_salesman+1):
    demand_satisfied_list.append("demand_satisfied_list"+str(i))
#    print(demand_satisfied_list)

for i in range(len(demand_satisfied_list)):
    a= []
    demand_satisfied_list[i]=a
    
overall_best_route=[]
for i in range(1,n_salesman+1):
    overall_best_route.append("overall_best_route"+str(i))

for i in range(len(overall_best_route)):
    a= []
    overall_best_route[i]=a

demand_satisfied_array=[]
for i in range(1,n_salesman+1):
    demand_satisfied_array.append("demand_satisfied_array"+str(i))
    
route_opt=[]
for i in range(1,n_salesman+1):
    route_opt.append("route_opt"+str(i))
    
distance_covered_list=[]
for i in range(1,n_salesman+1):
    distance_covered_list.append("distance_covered_list"+str(i))
    
for i in range(len(distance_covered_list)):
    a= []
    distance_covered_list[i]=a
    
new_distance_covered_list=[]
for i in range(1,n_salesman+1):
    new_distance_covered_list.append("new_distance_covered_list"+str(i))
    
for i in range(len(new_distance_covered_list)):
    a= []
    new_distance_covered_list[i]=a


distance_covered_array=[]
for i in range(1,n_salesman+1):
    distance_covered_array.append("demand_satisfied_array"+str(i))
    
no_of_cust_covered = np.zeros(n_facility)
dem_sat_array=np.zeros(n_facility)



#for num1 in range(n_facility):
#    s=0
#    dem_sat=0
#    for num2 in range(n_cust):
#        if cust_dist[num1,num2]==1:
#            s+=1
#            dem_sat+=demand[num2]
#    no_of_cust_covered[num1]=s
#    dem_sat_array[num1]=dem_sat
#
#dem_sat_array=dem_sat_array[1:n_facility]    
#distance_travelled_array=np.array(f_dist[0])
#
#demand_dist_ratio=dem_sat_array/distance_travelled_array
#demand_dist_ratio = np.nan_to_num(demand_dist_ratio)
#rough_demand_dist_ratio=np.copy(demand_dist_ratio)
#
#rough_demand_dist_ratio.sort()
#sorted_demand_dist_ratio_array=rough_demand_dist_ratio[::-1]
#cand_list=[]
#for i in range(limit):
#    cand_list.append(sorted_demand_dist_ratio_array[i])
#candidate_list=np.array(cand_list)
#
#cand_facility=[]
#for i in candidate_list:
#    cand_facility.append(np.argwhere(i==demand_dist_ratio))


def local_search(a,salesman,iterate):
#    print("iteration =", iterate)
    count=0
    num=-1
    for i in a:
        if i==1:    
            count+=1
            num+=1
        else:
            num+=1
        if count==3:
            break
        
#    print(num)
    
            ##################### TO CALCULATE INITIAL LENGTH OF PATH##########
    dist_cov=0            
    for v in range(n_facility-1):
        dist_cov= dist_cov+fac_dist[int(a[v])-1,int(a[v+1])-1]
#    print("total original dist =", dist_cov)
    
    if num>=4:
        flag=1
        loop_limit=0
        while(flag==1 and loop_limit<=10):
            flag=0
            for i in range(num-2):
                num1=int(a[i])-1
                num2=int(a[i+1])-1
#                print("num1",num1)
#                print("num2",num2)
               
                for j in range(i+2,num-1):
                    num3=int(a[j])-1
                    num4=int(a[j+1])-1
#                    print("num3",num3)
#                    print("num4",num4)
                    
                    if int(fac_dist[num1,num2])+int(fac_dist[num3,num4])> int(fac_dist[num1,num3])+ int(fac_dist[num2,num4]):
                        flag=1
#                        print("oohh yeeeahh")
#                        print("num1",num1)
#                        print("num2",num2)
#                        print("num3",num3)
#                        print("num4",num4)
#                        print("original dist =",int(fac_dist[num1,num2])+int(fac_dist[num3,num4]) )
#                        print("reduced dist =",int(fac_dist[num1,num3])+int(fac_dist[num2,num4] ))
                        temp=a[i+1]
                        a[i+1]=num3+1
                        a[j]=temp
#                        print(" new route is", a)
                        loop_limit+=1
                        flag=1
                        break
#                    else:
#                        print("ohh noo")
#                        print("num1",num1)
#                        print("num2",num2)
#                        print("num3",num3)
#                        print("num4",num4)
#            else:
#                print("fuck off")
#                flag=0
            
            dist_cov=0            
            for v in range(n_facility-1):
                dist_cov= dist_cov+fac_dist[int(a[v])-1,int(a[v+1])-1]
            print("total new dist =", dist_cov)
#            dist.append(float(dist_cov))
            new_distance_covered_list[salesman]=[float(dist_cov)]
        
    elif num==3:
        new_distance_covered_list[salesman]=[float(dist_cov)]
    else:
        new_distance_covered_list[salesman]=[0]
    print(a)
#    a[num-1]=cand_facility[0][0][0]+1
#    print(a)    
    
    return(a)
def route_length(a):
    count=0
    num=-1
    for i in a:
        if i==1:    
            count+=1
            num+=1
        else:
            num+=1
        if count==3:
            break
        
    return num        
              

overall_max_satisfied_cust=0
overall_minimum_dist_covered=1000000000
cost_matrix=np.zeros((iteration,1))
start_time = time.time()

for ite in range(iteration):
#    print("iterarion no =", ite)
    
#    for Q in range((len(route_name))):
#        W=np.ones((iteration,n_facility))
#        route_name[Q]=W
    alert=1000    
    for Z in range(len( demand_satisfied_list)):
        a=[]
        demand_satisfied_list[Z]=a
        
    for Z in range(len( distance_covered_list)):
        a=[]
        distance_covered_list[Z]=a
        
    
    for num1 in range(n_facility):
        s=0
        dem_sat=0
        for num2 in range(n_cust):
            if cust_dist[num1,num2]==1:
                s+=1
                dem_sat+=demand[num2]
        no_of_cust_covered[num1]=s
        dem_sat_array[num1]=dem_sat
#    print("demand sat array", dem_sat_array)
#dem_sat_array=dem_sat_array[1:n_facility]    
    distance_travelled_array=np.array(f_dist[0])
    
    demand_dist_ratio=dem_sat_array/distance_travelled_array
    demand_dist_ratio = np.nan_to_num(demand_dist_ratio)
    rough_demand_dist_ratio=np.copy(demand_dist_ratio)
    
    rough_demand_dist_ratio.sort()
    sorted_demand_dist_ratio_array=rough_demand_dist_ratio[::-1]
    cand_list=[]
    for i in range(limit):
        cand_list.append(sorted_demand_dist_ratio_array[i])
    candidate_list=np.array(cand_list)
    
    cand_facility=[]
    for i in candidate_list:
        cand_facility.append(np.argwhere(i==demand_dist_ratio))
#    print("cand facility=",cand_facility[temp_index][0][0])   
    
    
    
    demand_satisfied=0
    distance_covered=0
    unsatisfied_cust=[]
    satisfied_cust=[]
    temp_no_of_cust_covered=np.array(no_of_cust_covered)
    temp_dem_sat_array=np.array(dem_sat_array)
    
    temp_cust_distance=np.array(cust_dist)
    
    
    for u in range(n_salesman):
#        fac=zx[:]
        
        distance_covered=0
        if u>0:
            if flag_2==0:
                best_facility=1
            
            for k in range(n_cust):
                if (temp_cust_distance[best_facility-1,k]==1):
                    satisfied_cust.append(k)
               
#            for g1 in satisfied_cust:
#                fac.remove(g1)
#            unsatisfied_cust=fac

            for a in satisfied_cust:
                temp_cust_distance[:,a]=0
#
            for n1 in range(n_facility):
                s=0
                dem_sat=0
                for n2 in range(n_cust):
                    if temp_cust_distance[n1,n2]==1:
                        s+=1
                        dem_sat+=demand[n2]
                        
                temp_no_of_cust_covered[n1]=s
                temp_dem_sat_array[n1]=dem_sat
                
                
            temp_dist_travelled_array=np.array(f_dist[0])    
            temp_dist_travelled_array=np.nan_to_num(temp_dist_travelled_array)    
            demand_dist_ratio=temp_dem_sat_array/temp_dist_travelled_array
            demand_dist_ratio = np.nan_to_num(demand_dist_ratio)
            rough_demand_dist_ratio=np.copy(demand_dist_ratio)
            
            rough_demand_dist_ratio.sort()
            sorted_demand_dist_ratio_array=rough_demand_dist_ratio[::-1]
            cand_list=[]
            for i in range(limit):
                cand_list.append(sorted_demand_dist_ratio_array[i])
            candidate_list=np.array(cand_list)
            
            cand_facility=[]
            for i in candidate_list:
                cand_facility.append(np.argwhere(i==demand_dist_ratio))
            
#            print("candidate facility =",cand_facility)
        
        satisfied_cust=[]
        flag_2=0
        
        for j in range(n_facility-1):
            fac=zx[:]
#            print("j =",j)
            
            if (distance_covered<maximum_distance):
                if j>0 :
                    bahubali=[]             #to store facility which satisfies 0 customers
                    for n1 in range(n_facility):
                        s=0
                        dem_sat=0
                        for n2 in range(n_cust):
                            if temp_cust_distance[n1,n2]==1:
                                s+=1
                                dem_sat+=demand[n2]
                                
                        temp_no_of_cust_covered[n1]=s
                        temp_dem_sat_array[n1]=dem_sat
                        
#                    print("temp dem sat array =", temp_dem_sat_array)
                    
                    cur_loc = int(route_name[u][ite,j]-1) 
                    temp_dist_travelled_array=np.array(f_dist[cur_loc])
                    temp_dist_travelled_array=np.nan_to_num(temp_dist_travelled_array)
                    
#                    print(" temp dist travelled array =", temp_dist_travelled_array)
                    
                    demand_dist_ratio=temp_dem_sat_array/temp_dist_travelled_array
                    demand_dist_ratio = np.nan_to_num(demand_dist_ratio)
                    rough_demand_dist_ratio=np.copy(demand_dist_ratio)
                    
                    rough_demand_dist_ratio.sort()
                    sorted_demand_dist_ratio_array=rough_demand_dist_ratio[::-1]
                    cand_list=[]
                    for i in range(limit):
                        cand_list.append(sorted_demand_dist_ratio_array[i])
                    candidate_list=np.array(cand_list)
                    
                    cand_facility=[]
                    for i in candidate_list:
                        cand_facility.append(np.argwhere(i==demand_dist_ratio))
#                        print("cand facility=",cand_facility[0][0])
                        
                demand_satisfied=0
                distance_covered=0
                cum_prob = np.zeros(n_facility)
                cur_loc = int(route_name[u][ite,j]-1)
                total = np.sum(candidate_list)
                if total==0:
                    total=1
                    
                    
                probs = candidate_list/total
                cum_prob = np.cumsum(probs)
                r = np.random.random_sample()
                if np.all(cum_prob==0):
                    print("#########SHIT#########")
                    facility=1
                    route_name[u][ite,j+1] = facility
#                    print(" facility =", facility)
#                    print("route is" route_name[u])
#                if numpy.all(temp_cust_distance==0)==False)
#                    print("route name 1", route_name[u][ite])
                    
                else:
#                            print("cum_prob =", cum_prob)
                    temp_index = np.nonzero(cum_prob>r)[0][0]
#                    temp_value=candidate_list[temp_index]
##                    facility=np.where(int(temp_value) == demand_dist_ratio)+1
                    facility=cand_facility[temp_index][0][0]+1
#                    
#                    
#                    print("facility =", facility)
#
                route_name[u][ite,j+1] = facility
                
                for v in range(n_facility-1):
                   distance_covered= distance_covered+fac_dist[int(route_name[u][ite,v])-1,int(route_name[u][ite,v+1])-1]
#                print("dist covered in iteration", ite, "=",distance_covered)
                if distance_covered<maximum_distance:
                    print("blaaaaa")
                    for k in range(n_cust):
                        if (temp_cust_distance[facility-1,k]==1):
                           satisfied_cust.append(k)
                           
                    for g1 in satisfied_cust:
                        fac.remove(g1)
                    unsatisfied_cust=fac
    
                    for a in satisfied_cust:
                        temp_cust_distance[:,a]=0
                        
                    if numpy.all(temp_cust_distance==0):
                        print("rohit")
                        temp_dem_sat_array=np.zeros(n_facility)
                        if alert<u:
                            route_name[u][ite,j+1]=1
                        else:
                            alert=u
                        print("alert")
                        print("temp cust distance is",temp_cust_distance)
                        
                        
                        distance_covered=0
                        demand_satisfied=0
#                        if alert<u:
#                            route_name[u][ite,j+1]=1
                        for v in range(n_facility-1):
                            distance_covered= distance_covered+fac_dist[int(route_name[u][ite,v])-1,int(route_name[u][ite,v+1])-1]
                            
                        distance_covered_list[u].append(distance_covered)
                        
                        for b in satisfied_cust:
                            demand_satisfied+=np.sum(demand[b])
                            
                        demand_satisfied_list[u].append(demand_satisfied)
                        
#                        print("demand satisfied =", demand_satisfied)
#                        print("route name 2", route_name[u][ite])
                        break                        
                        
                else:
                    print("ooh yeaah")
                    distance_covered=0
                    demand_satisfied=0
                    route_name[u][ite,j+1]=1
                    for v in range(n_facility-1):
                        distance_covered= distance_covered+fac_dist[int(route_name[u][ite,v])-1,int(route_name[u][ite,v+1])-1]
                        
                    distance_covered_list[u].append(distance_covered)
                    
                    for b in satisfied_cust:
                        demand_satisfied+=np.sum(demand[b])
                        
                    demand_satisfied_list[u].append(demand_satisfied)
#                    print("end of salesman",u,"path in iteration", ite)
#                    print("demand satisfied =", demand_satisfied)
#                    print("route name 3", route_name[u][ite])

                    break
    
    ################### WE CAN CHECK OTHER COMBINATIONS OTHER THAN THE CHOOSEN FACILITY SO THAT WE MAY GET A FACILITY WHICH IF INCLUDED, THE DISTANCE TRAVELLED IS STILL < MAXIMUM DIST. IF NO SUCH COMB IS AVAILABLE THEN BREAK.
    #  $                  break
                    
            else:
                break                        
        
#        print("route is ",route_name[u][ite])
        local_search_route[u][ite]=local_search(route_name[u][ite],u,ite)
#        print("revised route is", route_name[u][ite])
#        print(" demand_sat_array is", temp_dem_sat_array)
#        print("num is", route_length(route_name[u][ite]))        
        local_search_dem_sat_list=[]
        local_search_facility=[]
#        p=[]
        
#        if np.all(temp_dem_sat_array)==0:
        if not np.any(temp_dem_sat_array):
#            print("prashant")
            route_name[u][ite]=local_search_route[u][ite]
        else:
            print(" mauka mauka  ")
#            local_search_dem_sat_list=[]
#            local_search_facility=[]
            for AA in range(limit):
                
#                print( "initial p =", p)
                route_name[u][ite]=local_search_route[u][ite]
                
                num=route_length(route_name[u][ite])
                route_name[u][ite][num-1]=cand_facility[AA][0][0]+1
                print("new route without local search", route_name[u][ite] )
                route_name[u][ite]=local_search(route_name[u][ite],u,ite)
                print("new route with local search", route_name[u][ite] )
#                path.append(route_name[u][ite])
                distance_covered=0
                for v in range(n_facility-1):
                    distance_covered= distance_covered+fac_dist[int(route_name[u][ite,v])-1,int(route_name[u][ite,v+1])-1]
                print("dist covered of new route is", distance_covered)
#                path.append(route_name[u][ite])
                if distance_covered > maximum_distance:
                    route_name[u][ite][num-1]=1
                    print("shit")
                else:
                    print("har har mahadev")
                    local_search_dem_sat_list.append(int(demand_satisfied_list[u][0])+ int(temp_dem_sat_array[cand_facility[AA][0][0]]))
                    print("new demand satisfied =", local_search_dem_sat_list)
                    local_search_facility.append(cand_facility[AA][0][0]+1)
                    print("new facility =", local_search_facility)
#                    p.append(route_name[u])
#                    print( "p =",p)
                    
                    
        if len(local_search_dem_sat_list)>0:
            flag_2=1
            print("finalllyyyy")
            best_facility_position=local_search_dem_sat_list.index(max(local_search_dem_sat_list))
            
            best_facility=local_search_facility[best_facility_position]
            print("best facility is", best_facility)
#            route_name[u][ite]=path[best_facility_position]
            route_name[u][ite]=local_search_route[u][ite]
            route_name[u][ite][num-1]=best_facility
            print("final facilities are", route_name[u][[ite]])
            route_name[u][ite]=local_search(route_name[u][ite],u,ite)
            print("final route is =", route_name[u][ite])
            demand_satisfied_list[u]=[local_search_dem_sat_list[best_facility_position]]
        else:
            new_distance_covered_list[u]=distance_covered_list[u]
#                
    for i in range(len(route_name)):
        route_opt[i]=np.array(route_name[i])
    for i in range(len(demand_satisfied_list)):
        demand_satisfied_array[i]=np.array(demand_satisfied_list[i])
    
    for i in range(len(new_distance_covered_list)):
#            distance_covered_array[i]=np.array(demand_satisfied_list[i])
        distance_covered_array[i]=np.array(new_distance_covered_list[i])
        
    overall_demand_satisfied_list=[sum(x) for x in zip(*demand_satisfied_list)]
    overall_distance_covered_list=[sum(x) for x in zip(*new_distance_covered_list)]
    
    overall_demand_satisfied_array=np.array(overall_demand_satisfied_list)
    overall_distance_covered_array=np.array(overall_distance_covered_list)
    print("overall distance satisfied in iteration", ite,"is", overall_distance_covered_array[0])
    
    if overall_demand_satisfied_array.size==0:
        dist_max_loc=0
        dist_max_cost=0

    cost_matrix[ite]=overall_max_satisfied_cust               ##BREAKING CRITERIA

#    if ite>break_limit:                                     ##BREAKING CRITERIA
#        out=0
#        for v in range(ite,ite-break_limit,-1):
#            if cost_matrix[v]==cost_matrix[v-1]:
#                out+=1
#        if out==break_limit:
#            break

#    if max_satisfied_cust > overall_max_satisfied_cust:
    if overall_demand_satisfied_array[0] > overall_max_satisfied_cust:         #!@#$%^!@#$
#        print("ooh yeeeeahh")
        overall_max_satisfied_cust=overall_demand_satisfied_array[0]           #!@#$%^%$#@!
        overall_minimum_dist_covered=overall_distance_covered_array[0]
        
        
        for A in range(len(overall_best_route)):
            overall_best_route[A]=route_name[A][ite]
        print("overall best route in iteration", ite," is", overall_best_route)
        
    if(( overall_demand_satisfied_array[0] == overall_max_satisfied_cust) and (overall_minimum_dist_covered>overall_distance_covered_array[0])):
        print(" hurraayyy ")
        overall_minimum_dist_covered= overall_distance_covered_array[0]
        overall_max_satisfied_cust=overall_demand_satisfied_array[0]

        
        for A in range(len(overall_best_route)):
            overall_best_route[A]=route_name[A][ite]
#        print("overall best route in iteration", ite," is", overall_best_route)
final_dist=0
for C in range(n_salesman):
    for v in range(n_facility-1):
        final_dist+= fac_dist[int(overall_best_route[C][v])-1,int(overall_best_route[C][v+1])-1]
    
#    total_time=time.time() - start_time  
total_time=time.time() - start_time

#print('route of all the ants at the end :')
#print(route_opt)
print()
print('best path :',overall_best_route)
#print('cost of the best path',int(dist_min_cost[0]) + fac_dist[int(best_route[-2])-1,0])  
print('maximum demand satisfied =',overall_max_satisfied_cust) 
print('distance travelled =',overall_minimum_dist_covered)        
print("total distance covered =",final_dist)
print("total time taken =",total_time)