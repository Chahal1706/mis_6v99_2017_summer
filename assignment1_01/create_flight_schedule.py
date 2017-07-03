# coding: utf-8

# In[98]:

#!/usr/bin/python
import numpy as num

from datetime import datetime
from datetime import timedelta







'''This function returns the military time from any given time
    input : any time
    output : time in military time for eg: 06:00 hrs will be : 360 
'''

def milTime(x):
    
        hrs = [datetime.strptime(x, "%H:%M:%S").hour]
        minu = [datetime.strptime(x, "%H:%M:%S").minute]
        return (hrs[0]*60)+(minu[0])


# In[120]:
'''
we now create a numpy array with 1 rowws and 6 elements 
we populate the array with name of 6 planes
'''

Tail_Numbers = num.zeros((1,6),dtype=object)
Tail_Numbers = ['T1','T2','T3','T4','T5','T6']

numofiterations=0


'''
this line created a numpy array with 6 rows and 3 elements per rowk
the array is named as : flight_time2
This array contains the flight time between the two cities
'''
flight_time2 = num.array([['AUS','DAL',50],['AUS','HOU',45],['DAL','HOU',65],['DAL','AUS',50],['HOU','AUS',45],['HOU','DAL',65]])

'''
This line is creating another numpy array which is of the same size as flight_time2 and using a loop to copy the elements
of flight_time2 into another array flight_time

'''
   
flight_time = num.copy(flight_time2)
    
'''
this line of code create a numpy array : ground_time2 which is an array of 3 rows and 3 elements
then copy the ground_time2 value to ground_time array
equavalant to : ground_time =num.copy(ground_time2)
the content of each array is : ['city','number of terminals','ground time']

'''

ground_time2 = num.array([['AUS',1,25],['DAL',2,30],['HOU',3,35]])

ground_time=num.copy(ground_time2)





#print("tail numbers are :",Tail_Numbers)
#print("flight_time are :",flight_time)
#print("ground_time are :",ground_time)


'''
we are creating a list of time from 6 in the morning till 22 in the night and we are selecting a time interval of 5 
the reason being 5 is the LCD of the ground time

'''


rep_temp = [str(datetime(1900, 1, 1, hr, min, 0).time()) 
            for hr in range(6,22) 
            for min in range(0,60,5)]

'''
we only get values till 21:55:00 , therefore we will add the value of 22:00:00 to the list

'''
rep_temp.append('22:00:00')




#print(num.shape(rep_temp)[0])
'''
this line is calculating the nubmer of time slots that we have , our final array will have this many rows
'''

num_timeslots=num.shape(rep_temp)[0]

'''
we have 6 gates
g1, g2, g3,g4,g5,g6
'AUS',1,25],['DAL',2,30],['HOU',3,35
g1 -> g2
g1 -> g3
g1 ->g4
g1->g5
g1->g6
g2 -> g4
g2->g5
g2->g6
g3 -> g4
g3 ->g5
g3 -> g6


11
11 -> unique combination of gates
193 ->  number of time slots
14 = 11 (combination of gates) + 1(military time) + 1 flight number + 1 (actual time)


'''

'''
open your file here 
header : tail_number,origin,destination,departure_time,arrival_time \n

with open("create_flight_schedule.csv", 'w') as f:

        header = "tail_number,origin,destination,departure_time,arrival_time \n"
        f.write(header)
        #for item in create_flight_schedule:
            #temp = item.tail_no + "," + item.startpoint + "," + item.endpoint + "," + convert_time( item.starttime) + "," + convert_time( item.arrivaltime) + '\n'
            #f.write(temp)
    #f.close()
'''
with open("E:\\assignment\\create_flight_schedule.csv", 'w') as f:
    header = "tail_number,origin,destination,departure_time,arrival_time \n"
    f.write(header)
    
    rep = num.zeros((num_timeslots,14),dtype=object)

#print("rep initially",rep)

    '''
    This line is copying the time along with military time into the array
    this is the final array .
    '''

    for i in range (0,num_timeslots):
        rep[i,0] = rep_temp[i]
        rep[i,1] = milTime(rep_temp[i])

    
#print(rep[192])
    
    
    
    '''
    this line will create the arrya of zeros for 6 rows and 4 columns and fill each one with zeros

    '''
    currep = num.zeros((6,4),dtype=object)



    '''
    This line is adding the value of T to the 0th index of this arry
    '''

    for t in range(0,6):
        currep[t,0] = Tail_Numbers[t]
        
    

#print("current valeu of currep is : ",currep[0])

    


    '''
    this line of code is defining a function assigned having values dep1, tail, from, to and gate
    '''

    def assigned(dep1,tail,fro,to,gate):
        #numofiterations += 1
        #print("number of iterations:",numofiterations)
        #print("variables to assigned")
        #print("dept : ",dep1)
        #print("tail ",tail)
        #print("fro ",fro)
        #print("to ",to)
        #print("gate ",gate)
        dep = '06:00:00' 
        f_time = 0 
        g_time = 0 
        
       
  
        '''
        this will take fro  value from i,0 th element of flight_time matrix and to value  i,1th element of same matix
        return the value of the flight time for the route
        '''
        for i in range(0,6): 
            #print (flight_time)
            if flight_time[i,0] == fro and flight_time[i,1] == to:
                f_time = int(flight_time[i,2])
                print("we found the flight time",f_time)
                break
            
        '''
        this line of code will match the elements of oth element n ground_time to to value
        and give the 2nd value from ground_time to g_time
        '''

        for i in range(0,3):     
            if ground_time[i,0] == to:
                g_time = int(ground_time[i,2])
                print("we found the ground time",g_time)
                break
            
            
            
    

        '''
        this code is stripping the value of the departure time  in the format : '1900-01-01 06:00:00' 
        the reason we are using this format is because we are using this format in milTime function
        '''
        dep_temp = datetime.strptime(dep,'%H:%M:%S')
   
    #print(dep_temp)

        '''
        here we are calling method timedelta which will sum up (flight and groound time) to departure time
        we calculate the arrival time as an output of this statemtn in the format : '1900-01-01 07:00:00'
        '''
        arrival = dep_temp + timedelta(minutes=f_time+g_time)
        
        actual_arrival_time=dep1+f_time
        dep1,tail,fro,to,gate
        temp = str(tail) + "," + str(fro) + "," + str(to) + "," + str(dep1) + "," + str(actual_arrival_time) + '\n'
    
        f.write(temp)
        
    
        ''' 
        this line is getting the arrival in: 07:00:00 format
        '''
        arrival = str(datetime.strptime(str(arrival),'%Y-%m-%j %H:%M:%S').time()) 
    #print(type(arrival))
    
        for i in range(0,193):
        
            if rep[i,1] == dep1:
                temp = i
                print("temp now is : ",temp)
                for k in range(0,round(f_time/5)+1):
                    if tail == 'T1':
                    #print("temp for this condition: ",temp)
                        if temp==193:
                            continue
                        else:
                            rep[temp,2] = tail
                            temp = temp+1
                    elif tail == 'T2':
                    #print("temp for this condition: ",temp)
                        if temp==193:
                            continue
                        else:
                            rep[temp,3] = tail
                            temp = temp+1 
                    elif tail == 'T3' :
                    #print("temp for this condition: ",temp)
                        if temp==193:
                            continue
                        else:
                            rep[temp,4] = tail
                            temp = temp+1 
                    elif tail == 'T4' :
                    #print("temp for this condition: ",temp)
                        if temp==193:
                            continue
                        else:
                            rep[temp,5] = tail
                            temp = temp+1 
                    elif tail == 'T5':
                    #print("temp for this condition: ",temp)
                        if temp==193:
                            continue
                        else:
                            rep[temp,6] = tail
                            temp = temp+1 
                    elif tail == 'T6':
                    #print("temp for this condition: ",temp)
                        if temp==193:
                            continue
                        else:
                            rep[temp,7] = tail
                            temp = temp+1
                    
                for j in range(0,round(g_time/5)):
                    try:
                        if gate == 'A1' :
                        #rint("temp for this condition: ",temp)
                            if temp==193:
                                continue
                            else:
                                rep[temp,8] = gate
                                temp = temp+1
                        elif gate == 'D1':
                        #print("temp for this condition: ",temp)
                            if temp==193:
                                continue
                            else:
                                rep[temp,9] = gate
                                temp = temp+1 
                        elif gate == 'D2' :
                        #print("temp for this condition: ",temp)
                            if temp==193:
                                continue
                            else:
                                rep[temp,10] = gate
                                temp = temp+1

                        elif gate == 'H1':
                        #print("temp for this condition: ",temp)
                            if temp==193:
                                continue
                            else:
                                rep[temp,11] = gate
                                temp = temp+1 
                        elif gate == 'H2' :
                        #print("temp for this condition: ",temp)
                            if temp==193:
                                continue
                            else:
                                rep[temp,12] = gate
                                temp = temp+1 
                        elif gate == 'H3':
                        #print("temp for this condition: ",temp)
                            if temp==193:
                                continue
                            else:
                                rep[temp,13] = gate
                                temp = temp+1
                    except Exception:
                        print("exception occurred while filling the ground time gates")
                    
        for l in range(0,6):
            if currep[l,0] == tail:
                currep[l,1] = gate
                currep[l,2] = int(dep1+f_time+g_time)
                currep[l,3] = to
    
    


    def firstfly():
        assigned(360,'T1','AUS','HOU','H2')
        assigned(360,'T2','HOU','DAL','D1')
        assigned(360,'T3','HOU','AUS','A1')
        assigned(360,'T4','DAL','HOU','H1')
        assigned(360,'T5','DAL','HOU','H3')
        assigned(360,'T6','HOU','DAL','D2')
    #tail_number,origin,destination,departure_time,arrival_time

    firstfly() 
    print(rep[180:,0:15])
    print(currep)


    #print("currep[0:5,2]",currep[0:5,2])

    rows_current_min=0
    def mincurtime():
        #print("this is what we get as currep: ",currep[0:5,2])
        tground = num.amin(currep[0:5,2])
        rows,cols = num.where(currep == tground)
        print("inside mincurrent , this is the current row",rows)
        #print rows,cols
        tailnum = currep[rows[:1],0]
        gatenum = currep[rows[:1],1]
        fro = currep[rows[:1],3]
        #print(tground)
        #print(tailnum)
        #print(gatenum)
        #print(fro)
        return tailnum,gatenum,tground,fro
        
    
    #mincurtime()


    def optim():
        #['AUS',1,25],['DAL',2,30],['HOU',3,35]
        #from part, departure details
        tailnum,gatenum,tground,fro = mincurtime() 
        #print(tailnum,gatenum,tground,fro)
        #print(num.where(ground_time == fro))
        #to part, destination details
        
        '''
        tailnum:'T3'
        gatenum : 'A1'
        tground : 430
        fro : 'AUS'
        '''
        gate_found=0
    
        gate_dict={'AUS':[8],'DAL':[9,10],'HOU':[11,12,13]}
        deptime = tground + 5
    
        row_g, col_g = num.where(ground_time == fro)
        #print("row_g:",row_g, "and col_g is :", col_g)
        dummy_row = num.zeros((1,3), dtype = object)
        dummy_row = ([0,1,2])
        row_g = num.where(dummy_row != row_g)
        print("row_g main now is :", row_g)
    
    
    
        l_row_g = row_g[0]
        #print("l_row_g main now is first : ",l_row_g)
    
        #print("this is where we are stuck")
        #print("experimenting: ",(ground_time[l_row_g,2]))
        '''
        list(map(int, ground_time[l_row_g,2])) is formng the list of minimum ground time
        '''
    
    
        l_ground_time_orig=list(map(int, ground_time[l_row_g,2]))
        l_ground_time=list(l_ground_time_orig)
        print("L GROUND TIME",l_ground_time)
        t_time=0
        print("efefe l_ground_time :",l_ground_time)
        actual_index=1
        to=fro
    
        while (gate_found !=1 ):
        
            time_of_arrival_at_dest=0
            if(len(l_ground_time)==0):
                l_ground_time=list(l_ground_time_orig)
                deptime+=10
                print("dept time is : ",deptime)
                if(deptime > 1320):
                    return
                
            else:
                minimumgt = num.amin(l_ground_time)
        
            print("list grond time before removal : ",l_ground_time)
            l_ground_time.remove(minimumgt)
            print("list grond time after removal : ",l_ground_time)
            row_g, col_g = num.where(ground_time == str(minimumgt))
            to = ground_time[row_g,0]
            for i in range(0,6):
                if flight_time[i,0] == fro[0] and flight_time[i,1] == to[0]:
                    t_time = int(flight_time[i,2])
                
            time_of_arrival_at_dest=int(deptime)+int(t_time)
            row_of_dest,column_of_dest=num.where(rep == time_of_arrival_at_dest )
            #gates = ground_time[row_g,1]
            gate_prefix=to[0]
            index_of_gates_possible = gate_dict[gate_prefix]
            '''
            this is the index of the gates for e.g : 1, 1,2 , 1,2,3 and so on
            '''
        
            for gateindex in index_of_gates_possible:
                if(rep[row_of_dest,gateindex]==0):
                    finalindexofgate=gateindex
                    gate_found=1
                    break
                else:
                    actual_index+=1
                    if(len(index_of_gates_possible) < actual_index):
                        break
                    else:
                        continue
                    
        
    #print("minimum gt in string is : ", str(minimumgt))
    #print("we will get teh element with minimum ground time:",num.where(ground_time == str(minimumgt)))
    
    #print row_g, col_g
    
        print("to now is : ", to)

    
    #print("gates is :",gates)
    
    #print ("final_printout:",fro,to,gates,minimumgt)
   ### print(type(str(flight_time[1,0])),type(str(fro)))
    #print("fro is : ",fro[0])
    
     
        #print("flight_time is :",flight_time[i,0])
        #print("flight time for fro : ",flight_time[i,1])
        #print("fro is : ",fro[0])
        #print("to is : ",to[0])
        
            #print("we got true state")
            
    #print ("t_time nos is : ",t_time)
    
    
            
          
 ###   print("to"+to)
    
        index_of_dept_time,col_of_value=num.where(rep==deptime)
    #print("i got the index of dept time",index_of_dept_time)
    #gate = num.array_str(gates)
    #print("gates is : ",gate)
        fro = fro[0]
    #print("fro now is : ",fro)
    #print("tground is : ",tground)
    #print("t_time nos is :",t_time)
    
    #print("time_of_arrival_at_dest:",time_of_arrival_at_dest)
    
    #print("row is dest is: " ,rep[row_of_dest])
    
    
    #print("Nubmer_of_gates_possible",index_of_gates_possible)
    
            #if(len(index_of_gates_possible)==actual_index):
                
    #print(finalindexofgate)
        gate=to[0][0]+str(actual_index)
    #print("this is the final gate",gate)
    #gate = to[2]+gate[2]
    #print("final gate is : ",gate)
    
  # print (deptime,tailnum[2:4],fro[2:5],to[2:5],gate)
    
 ###   print (type(deptime),type(tailnum),type(fro),type(to),type(gate))
    
    #with open('output.txt', 'w') as f: 
     #   f.write(type(deptime),type(tailnum),type(fro),type(to),type(gate))
    #assigned(deptime,tailnum[2:4],fro[2:5],to[2:5],gate)
        print("deptime is :",deptime)
        print("tailnum is :",tailnum)
        print("fro is :",fro)
        print("to is :",to)
        print("gate is :",gate)
        print('calling assigned')
        assigned(deptime,tailnum[0],fro,to[0],gate)
    
    optim()

 
    #print("rep after optim is : ",rep[0:70])


    def time_military(time):
    print(int(time))
    hours = str(int(int(time)/60))
    minutes = str(int(time)%60)
    return hours.zfill(2)+minutes.zfill(2)
    with open("flight_schedule.csv1", 'wt') as f1:
    csv_header = 'tail_number,origin,destination,departure_time,arrival_time'
    print(csv_header, file= f1)
    path = r'E:\assignment\flight_schedule.csv'
    with open(path, 'r') as f:
        for line in f.readlines():
            #print(line)
            arr =  line.strip().split(',')
            temp = []
            for item in arr:
                temp.append(item.strip())
            #print(arr)
            #print(arr1[3])
            temp[3] = time_military(temp[3])
            temp[4] = time_military(temp[4])
            print(','.join(temp), file=f1)


    for i in range(0,190):
        optim()
    
    print("rep is :",rep[0:70])
    
f.close()
