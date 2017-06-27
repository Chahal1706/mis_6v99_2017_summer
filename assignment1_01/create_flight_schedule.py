
# coding: utf-8

# In[98]:

def milTime(x):
    
        hrs = [datetime.strptime(x, "%H:%M:%S").hour]
        minu = [datetime.strptime(x, "%H:%M:%S").minute]
        return (hrs[0]*60)+(minu[0])


# In[99]:

#!/usr/bin/python
import numpy as num
Tail_Numbers = num.zeros((1,6),dtype=object)
Tail_Numbers = ['T1','T2','T3','T4','T5','T6']


flight_time2 = num.array([['AUS','DAL',50],['AUS','HOU',45],['DAL','HOU',65],['DAL','AUS',50],['HOU','AUS',45],['HOU','DAL',65]])
flight_time = n.zeros((6,3),dtype=object)
for i in range(0,6):
    flight_time[i,0] = flight_time2[i,0]
    flight_time[i,1] = flight_time2[i,1]
    flight_time[i,2] = flight_time2[i,2]

ground_time2 = num.array([['AUS',1,25],['DAL',2,30],['HOU',3,35]])
ground_time = n.zeros((3,3),dtype=object)
for i in range(0,3):
    ground_time[i,0] = ground_time2[i,0]
    ground_time[i,1] = ground_time2[i,1]
    ground_time[i,2] = ground_time2[i,2]

print(Tail_Numbers)
print(flight_time)
print(ground_time)

from datetime import datetime
rep_temp = [str(datetime(1900, 1, 1, hr, min, 0).time())
for hr in range(6,22)
for min in range(0,60,5)]

num.shape(rep_temp)

import numpy as n

rep = n.zeros((192,14),dtype=object)

for i in range (0,192):
    rep[i,0] = rep_temp[i]

for i in range (0,192):
    rep[i,0] = rep_temp[i]
    rep[i,1] = milTime(rep_temp[i])
    
currep = n.zeros((6,4),dtype=object)
    
for t in range(0,6):
    currep[t,0] = Tail_Numbers[t]


# In[93]:

def assigned(dep1,tail,fro,to,gate):
    
    dep = '06:00:00'
    f_time = 0
    g_time = 0    
    
    for i in range(0,6):     
        if flight_time[i,0] == fro and flight_time[i,1] == to:
            f_time = int(flight_time[i,2])
   
    for i in range(0,3):     
        if ground_time[i,0] == to:
            g_time = int(ground_time[i,2])
            
    #print (f_time,g_time)
    
    from datetime import datetime
    
    dep_temp = datetime.strptime(dep,'%H:%M:%S')
    
    import datetime
    arrival = dep_temp + datetime.timedelta(minutes=f_time+g_time)
    
    from datetime import datetime
    arrival = str(datetime.strptime(str(arrival),'%Y-%m-%j %H:%M:%S').time())
    #print(type(arrival))
    
    for i in range(0,191):
        
        if rep[i,1] == dep1:
            temp = i
            for k in range(0,round(f_time/5)+1):
                if tail == 'T1':
                    rep[temp,2] = tail
                    temp = temp+1
                elif tail == 'T2':
                    rep[temp,3] = tail
                    temp = temp+1 
                elif tail == 'T3' :
                    rep[temp,4] = tail
                    temp = temp+1 
                elif tail == 'T4' :
                    rep[temp,5] = tail
                    temp = temp+1 
                elif tail == 'T5':
                    rep[temp,6] = tail
                    temp = temp+1 
                elif tail == 'T6':
                    rep[temp,7] = tail
                    temp = temp+1
                    
            for j in range(0,round(g_time/5)):
                try:
                    if gate == 'A1' :
                        rep[temp,8] = gate
                        temp = temp+1
                    elif gate == 'D1':
                        rep[temp,9] = gate
                        temp = temp+1 
                    elif gate == 'D2' :
                        rep[temp,10] = gate
                        temp = temp+1

                    elif gate == 'H1':
                        rep[temp,11] = gate
                        temp = temp+1 
                    elif gate == 'H2' :
                        rep[temp,12] = gate
                        temp = temp+1 
                    elif gate == 'H3':
                        rep[temp,13] = gate
                        temp = temp+1
                finally:
                    break
    for l in range(0,6):
        if currep[l,0] == tail:
            currep[l,1] = gate
            currep[l,2] = int(dep1+f_time+g_time)
            currep[l,3] = to


# In[94]:

def firstfly():
    assigned(360,'T1','AUS','HOU','H2')
    assigned(360,'T2','HOU','DAL','D1')
    assigned(360,'T3','HOU','AUS','A1')
    assigned(360,'T4','DAL','HOU','H1')
    assigned(360,'T5','DAL','HOU','H3')
    assigned(360,'T6','HOU','DAL','D2')


# In[95]:

firstfly() 
#print(rep[0:70,0:15])
#print(currep)


# In[96]:

import numpy as n
def mincurtime():
    tground = n.amin(currep[0:5,2])
    rows,cols = n.where(currep == tground)
    #print rows,cols
    tailnum = currep[rows[:1],0]
    gatenum = currep[rows[:1],1]
    fro = currep[rows[:1],3]
    return tailnum,gatenum,tground,fro


# In[91]:

def optim():
    
    #from part, departure details
    tailnum,gatenum,tground,fro = mincurtime() 
    #print tailnum,gatenum,tground,fro
   
    #to part, destination details
    
    row_g, col_g = n.where(ground_time == fro)
    dummy_row = num.zeros((1,3), dtype = object)
    dummy_row = ([0,1,2])
    row_g = n.where(dummy_row != row_g)
    
    minimumgt = n.amin(ground_time[row_g,2])
    row_g, col_g = n.where(ground_time == minimumgt)
    #print row_g, col_g
    to = n.array_str(ground_time[row_g,0])

    gates = ground_time[row_g,1]
    
 ###   print (fro,to,gates,minimumgt)
   ### print(type(str(flight_time[1,0])),type(str(fro)))
    
    for i in range(0,6):     
        if flight_time[i,0] == fro[2:5] and flight_time[i,1] == to[2:5]:
            t_time = int(flight_time[i,2])
            print (t_time)
 ###   print("to"+to)
    deptime = tground + 5
    gate = n.array_str(gates)
    tailnum = n.array_str(tailnum)
    fro = n.array_str(fro)
    gate = to[2]+gate[2]
    
  # print (deptime,tailnum[2:4],fro[2:5],to[2:5],gate)
    
 ###   print (type(deptime),type(tailnum),type(fro),type(to),type(gate))
    
    #with open('output.txt', 'w') as f: 
     #   f.write(type(deptime),type(tailnum),type(fro),type(to),type(gate))
    assigned(deptime,tailnum[2:4],fro[2:5],to[2:5],gate)
    
optim()


# In[92]:

for i in range(0,190):
    optim()


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



