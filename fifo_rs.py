# Page Replacement Algorithms and Evaluation
## FIFO algorithm - algorithm(1)

# create queue
import queue



# Page 編號 : 1~500 
# Memory Reference 次數 : 至少 10,000 次
# physical memory 的 frame 數量 : 10, 20, 30, 40, 50, 60, 70, 80, 90, 100 
## Random : Arbitrarily pick one number for each reference. - Reference String(1)

 
myqueue_10 = queue.Queue(10)  
myqueue_20 = queue.Queue(20)
myqueue_30 = queue.Queue(30)
myqueue_40 = queue.Queue(40)
myqueue_50 = queue.Queue(50)
myqueue_60 = queue.Queue(60)
myqueue_70 = queue.Queue(70)
myqueue_80 = queue.Queue(80)
myqueue_90 = queue.Queue(90)
myqueue_100 = queue.Queue(100)

# Radom 產生 Reference String 
## 測試 小範圍 - Textbook FIFO example 1
"""
myqueue_3 = queue.Queue(3)
rs_ex1 = [7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]
page_fault_sum = 0
cnt = 0 
while myqueue_3.full()!=True :
    myqueue_3.put(rs_ex1[cnt])
    cnt = cnt + 1
    page_fault_sum = page_fault_sum + 1

print('page_fault_sum:',page_fault_sum)


# 塞滿了，要塞下一個 先看 page 是否在 queue 裡 
# 有 則 hit , 沒有 則 miss 

while cnt != len(rs_ex1) : 
    if rs_ex1[cnt] in myqueue_3.queue:    
        pass
    else:
        page_fault_sum = page_fault_sum + 1
        myqueue_3.get()
        myqueue_3.put(rs_ex1[cnt])
    cnt = cnt + 1
print('page_fault_sum:',page_fault_sum)
"""

## 測試 小範圍 - Textbook FIFO example 2
"""
myqueue_3 = queue.Queue(3)
rs_ex2 = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
page_fault_sum = 0
cnt = 0 
while myqueue_3.full()!=True :
    myqueue_3.put(rs_ex2[cnt])
    cnt = cnt + 1
    page_fault_sum = page_fault_sum + 1

print('page_fault_sum:',page_fault_sum)


# 塞滿了，要塞下一個 先看 page 是否在 queue 裡 
# 有 則 hit , 沒有 則 miss 

while cnt != len(rs_ex2) : 
    if rs_ex2[cnt] in myqueue_3.queue:    
        pass
    else:
        page_fault_sum = page_fault_sum + 1
        myqueue_3.get()
        myqueue_3.put(rs_ex2[cnt])
    cnt = cnt + 1
print('page_fault_sum:',page_fault_sum)
"""
"""
myqueue_4 = queue.Queue(4)
rs_ex2 = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
"""
frame_number = input("Number of frame: ") 
myqueue = queue.Queue(int(frame_number))

import random
len_rs = 100000
# randint(1,500) 1~500
random_rs = []
dw_set = [] # disk write set
for i in range(len_rs):
     random_rs.append(random.randint(1,500))
     dw_set.append(random.randint(0,1))
 

page_fault_sum = 0
interrupt = 0
disk_write = 0


cnt = 0 
while myqueue.full()!=True :
    myqueue.put(random_rs[cnt])
    cnt = cnt + 1
    page_fault_sum = page_fault_sum + 1

print('page_fault_sum:',page_fault_sum)



# 塞滿了，要塞下一個 先看 page 是否在 queue 裡 
# 有 則 hit , 沒有 則 miss 

while cnt != len(random_rs) : 
    if random_rs[cnt] in myqueue.queue:    
        pass
    else:
        interrupt = interrupt + 1
        page_fault_sum = page_fault_sum + 1
        if dw_set[random_rs.index(myqueue.get())] == 1 : # modify
            disk_write = disk_write + 1
        #myqueue_10.get()
        myqueue.put(random_rs[cnt])
    cnt = cnt + 1

print('page_fault_sum: ',page_fault_sum)
print('inteerrupt: ',interrupt)
print('disk write: ',disk_write)











