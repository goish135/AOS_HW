import random
len_rs = 100000
# randint(1,500) 1~500
random_rs = []
dw_set = [] # disk write set
for i in range(len_rs):
    random_rs.append(random.randint(1,500))
    dw_set.append(random.randint(0,1))

locality_rs = []
while len(locality_rs) < len_rs: 
     
    begin = random.randint(1,500)
    maxApend = 500 - begin 
    if maxApend >= 2:
        add = random.randint(1,maxApend) # 還可放幾個的扣打
        # to be continue
        if len(locality_rs) >= len_rs :
            break 
        locality_rs.append(begin)
        #dw_set.append(random.randint(0,1)) 
        for i in range(add):
            begin = begin + 1
            if len(locality_rs) >= len_rs:
                break
            locality_rs.append(begin)
            #dw_set.append(random.randint(0,1))
    elif maxApend==2:
        if len(random_rs) >= len_rs:
            break
        locality_rs.append(499)
        #dw_set.append(random.randint(0,1))
        if len(random_rs) >= len_rs:
            break
        locality_rs.append(500)
        #dw_set.append(random.randint(0,1))
    else:
        locality_rs.append(500)
        #dw_set.append(random.randint(0,1))

"""
sum = 0
start = 10

while sum < len_rs:
    for i in range(1,50):
        custom_10.append(i)
        sum = sum + 1
    custom_10.append(start)
    start = start + 1
    sum = sum + 1
"""

dict_type = {}
#sum = 0
number = 10
while number <= 100:
    #sum = 0
    #print('frame 數: ',number)
    temp = []
    add = number
    while len(temp) < len_rs: 
        for i in range(1,number):
            if len(temp)>= len_rs:
                break
            temp.append(i)
            #sum = sum + 1
        if len(temp) >= len_rs:
            break    
        temp.append(add)
        add = add + 1
    key = 'custom_'+str(number)    
    dict_type[key] = temp
    #print(len(dict_type[key]))
    number = number + 10 


dict_type['random'] = random_rs
dict_type['locality'] = locality_rs
dict_type['dw_set'] = dw_set  

#print(len(random_rs))
#print(len(locality_rs))
#print(len(dw_set))
import json
with open("input.json","w") as f:
    json.dump(dict_type,f)
    print("寫入成功")

