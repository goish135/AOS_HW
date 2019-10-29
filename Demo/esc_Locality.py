# Enhanced Second Chance
import random
len_rs = 100000
# randint(1,500) 1~500
rs = []
modify = [] # disk write set

"""
for i in range(len_rs):
    rs.append(random.randint(1,500))
    modify.append(random.randint(0,1))
"""
while len(rs) < len_rs: 
     
    begin = random.randint(1,500)
    maxApend = 500 - begin 
    if maxApend >= 2:
        add = random.randint(1,maxApend) # 還可放幾個的扣打
        # to be continue
        if len(rs) >= len_rs :
            break 
        rs.append(begin)
        modify.append(random.randint(0,1)) 
        for i in range(add):
            begin = begin + 1
            if len(rs) >= len_rs:
                break
            rs.append(begin)
            modify.append(random.randint(0,1))
    elif maxApend==2:
        if len(rs) >= len_rs:
            break
        rs.append(499)
        modify.append(random.randint(0,1))
        if len(rs) >= len_rs:
            break
        rs.append(500)
        modify.append(random.randint(0,1))
    else:
        rs.append(500)
        modify.append(random.randint(0,1))

print(len(rs))
print(len(modify))

#rs =    [0,1,3,6,2,4,5,2,5,0,3,1,2,5,4,1,0] # reference string 
#modify= [0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0] 
Frame = {}
#frame_number = 4 # 手動輸入10次

import csv
with open('esc_lrs.csv','a',newline='\n') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["numberof_Frame","Page Fault ","Interrupt","disk write"])

for k in range(10):
    frame_number=input("輸入frame數量")
    frame_number = int(frame_number)
    index = 0
    page_fault = 0
    interrupt = 0
    dw = 0
    pointer = 0 

    # Roud 1 - fill in
    for i in range(frame_number): 
        if modify[index] == 1:
            Frame[i] = {"value":rs[index],"r":0,"m":1}
        else:
            Frame[i] = {"value":rs[index],"r":0,"m":0}   
        page_fault = page_fault + 1
        index = index + 1 

    print("fill in ",page_fault)

    # one cycle back to position 0 : point to 0
    # pointer = 0 


    # Round 2 - judge whether page fault
    """
    (r,m)
    Loop 1 : search (0,0) -- step1
    if not find,go Loop2
    Loop 2 : search (0,1),Set the use bit to zero for all frames bypassed -- step2
    * If step 2 failed, all use bits will now be zero and repetition of steps 1 and 2 are guaranteed to find a frame for replacement 
    """

    while index < len(rs):
        #print("index: ",index)
        frame_status = []
        status       = []

         
        for i in range(frame_number):
            # 印出目前狀況
            #print(Frame[i]["value"]," ",Frame[i]["r"]," ",Frame[i]["m"])
            frame_status.append(Frame[i]["value"])
            status.append([Frame[i]["r"],Frame[i]["m"]])
        #print(frame_status)
        #print(status)
        #print("")

        # check whether in frame
        exist = 0 # default is not found

        for i in range(frame_number): 
            if rs[index] == Frame[i]["value"]:
                Frame[i]["r"] = 1            
                exist = 1 # found
                index = index + 1
                break # break search

        # page fault 發生 shift to next page 
        # or page survive shift to next page        
        if exist == 0 :
            
            while True: # cycle frame list
                
                #print('pointer: ',pointer)
                out_of_Loop1 = 0  
                # run Loop 1
                while True:  
                    #print("index_00: ",index)
                    #print("index: ",index) # loop occur 
                    #pointer = pointer%4

                    if Frame[pointer]["r"] == 0 and Frame[pointer]["m"] == 0: # (0,0)
                        #print("00")
                        #print("loop1_replace by: ",rs[index])
                        #print("loop1_be replaced ",Frame[pointer]["value"])
                        #print('Loop1: ',index)
                        #print("")
                        Frame[pointer]["value"] = rs[index]
                        """
                        if modify[index] == 1:
                            Frame[i]["m"] = 1
                        else:
                            Frame[i]["m"] = 0
                        """
                        Frame[pointer]["m"] = modify[index]
                        Frame[pointer]["r"] = 0                    
                        page_fault = page_fault + 1
                        interrupt = interrupt + 1
                        index = index + 1
                        out_of_Loop1 = 1
                        pointer = (pointer%4) + 1
                        break # Loop1
                    else:
                        pointer = pointer + 1
                        
                    if pointer >= (frame_number-1):
                        pointer = (pointer%4) + 1
                        #print("exit")
                        break # Loop1

                    

                
                if out_of_Loop1 == 1 :
                    #print("out_of_Loop1")
                    break    # jump out While True == 不用再找下去

                # run Loop 2
                out_of_Loop2 = 0 
                if out_of_Loop1 == 0:
                    while True:  
                        #print("index_01: ",index)
                        #pointer = pointer%4
                        

                        if Frame[pointer]["r"] == 0 and Frame[pointer]["m"] == 1: # (0,1)
                            #print("11")
                            #print("Lopp2: ",index)
                            Frame[pointer]["value"] = rs[index]
                            page_fault = page_fault + 1
                            interrupt = interrupt + 1
                            dw = dw + 1
                            Frame[pointer]["m"] = modify[index]
                            Frame[pointer]["r"] = 0
                            out_of_Loop2 = 1
                            index = index + 1
                            #pointer = (pointer%4) + 1
                            pointer = (pointer%4) + 1
                            break # Loop 2
                        else:
                            #pointer = (pointer%4) + 1
                            Frame[pointer]["r"] = 0
                            pointer = pointer + 1
                        
                        if pointer >= (frame_number-1) :
                            pointer = (pointer%4) + 1
                            #print("out_of_Loop2")
                            break

                if out_of_Loop2 == 1 :
                    break   # jump out While True == 不用再找下去

            

    #for i in range(frame_number):
    #    print(Frame[i]["value"]," ",Frame[i]["r"]," ",Frame[i]["m"])
    print("total page fault ",page_fault)
    print("interrupt ",interrupt)
    print("dw ",dw)
    with open('esc_lrs.csv','a',newline='\n') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([frame_number,page_fault,interrupt,dw])        

