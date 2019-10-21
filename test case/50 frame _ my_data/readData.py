f = open('my_data.txt')
#print(f.read())
str=f.read()
#print(type(str.split( )))
str = str.split( ) 
str = list(map(int, str))
print(str)

rs_tc1 = str
print(len(rs_tc1))
print(rs_tc1[0])
# Optimal Page Replacement Algorithm

#fn_tc1 = 3 # Number of frames
#rs_tc1 = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]

"""
import csv
with open('optimal_rrs.csv','a',newline='\n') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["numberof_Frame","Page Fault ","Interrupt","disk write"])
"""

import random
len_rs = 100000
# randint(1,500) 1~500
#random_rs = []
#rs_tc1 = []
dw_set = [] # disk write set
for i in range(len_rs):
    #rs_tc1.append(random.randint(1,500))
    dw_set.append(random.randint(0,1))

"""
fn_tc1 = 4
rs_tc1 = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
"""

for i in range(1):
    fn_tc1 = input("輸入frame數: ")
    fn_tc1 = int(fn_tc1)
    hits_tc1 = 0 
    misses_tc1 = 0

    frame = []
    frame_record = [] # 紀錄 未來出現情況
    # rs 每往前一步 距離-- , 只更新新進來的page 距離(不需重新計算)
    cnt   = 0 # list's length
    index = 0 # rs_tc1's index
    page_fault = 0
    interrupt  = 0
    dw = 0

    #max = 0 
    while cnt <  fn_tc1 :
        #print("index: ",index)
        #print(rs_tc1[index])
        frame.append(rs_tc1[index])
        frame_record.append(int(0))

        cnt = cnt + 1
        page_fault = page_fault + 1
        for i in range(len(frame)):      
            if frame[i] in rs_tc1[index+1:len(rs_tc1)]:
                frame_record[i] = rs_tc1[index+1:len(rs_tc1)].index(frame[i]) - index
            else:
                frame_record[i] = (100000+1) 
        index = index + 1              



    #print(frame)
    print(page_fault)
    #print(index)
    #print(rs_tc1[index])

    while index <= (len(rs_tc1) - 1):
        #print(index)
        #print("rs: ",index)
        #max = -1
        flag = 0
        if rs_tc1[index] in frame:
            index = index + 1
            #pass
        else:
            """
            for i in range(len(frame)):
                if frame[i] in rs_tc1[index+1:len(rs_tc1)]:
                    #print('how far? ',rs_tc1[index+1:len(rs_tc1)].index(frame[i]))
                    if rs_tc1[index+1:len(rs_tc1)].index(frame[i]) > max :
                        max = frame[i] 
                        #print('max:',max)
                else:
                    max = frame[i]
                    flag = 1 
                    break
            """
            # 挑一個 距離最遠的 => list 挑最小 # 記得 挑完 距離-- 
            victim_page_index = frame_record.index(max(frame_record))
            
            #print('error:',max)
            
            #print('be replaced:',frame[frame.index(max)])
            
            #print('replaced by:',rs_tc1[index])

            """ 
            for i in range(0,index):
                if rs_tc1[i] == max:
                    near_position = i

            if dw_set[near_position] == 1 :
                dw = dw + 1
            """
            if dw_set[rs_tc1.index(frame[victim_page_index])] == 1:
                dw = dw + 1

            for k in range(fn_tc1):
                frame_record[k] = frame_record[k] - 1

            frame[victim_page_index] = rs_tc1[index]
            # 計算新進來 的 page 的距離
            if frame[victim_page_index] in rs_tc1[index+1:len(rs_tc1)]:
                frame_record[victim_page_index] = rs_tc1[index+1:len(rs_tc1)].index(frame[victim_page_index]) - index
            else:
                frame_record[victim_page_index] = (100000+1)

            page_fault = page_fault + 1
            interrupt = interrupt + 1
            index = index + 1

    print('Final Page Fault: ',page_fault)
    print('interrupt: ',interrupt)
    print('disk write: ',dw)
    """
    with open('optimal_rrs.csv','a',newline='\n') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([fn_tc1,page_fault,interrupt,dw])
    """
