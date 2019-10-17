# Enhanced Second Chance
rs =    [0,1,3,6,2,4,5,2,5,0,3,1,2,5,4,1,0] # reference string 
modify= [0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0] 
Frame = {}
frame_number = 4
index = 0
page_fault = 0

# Roud 1 - fill in
for i in range(frame_number): 
    if modify[index] == 1:
        Frame[i] = {"value":rs[index],"r":1,"m":1}
    else:
        Frame[i] = {"value":rs[index],"r":1,"m":0}   
    page_fault = page_fault + 1
    index = index + 1 



# Round 2 - judge whether page fault
"""
(r,m)
Loop 1 : search (0,0) -- step1
if not find,go Loop2
Loop 2 : search (0,1),Set the use bit to zero for all frames bypassed -- step2
* If step 2 failed, all use bits will now be zero and repetition of steps 1 and 2 are guaranteed to find a frame for replacement 
"""

while index < len(rs):
    for i in range(frame_number):
        print(Frame[i]["value"]," ",Frame[i]["r"]," ",Frame[i]["m"])

    #print('index',index)
    # check whether in frame
    exist = 0
    for i in range(frame_number):
        if rs[index] == Frame[i]["value"]:
            
            exist = 1
            index = index + 1
            break
            
    if exist == 0 :
        run3= -1
        while True:
            if run3 == 1:
                for i in range(frame_number):
                    Frame[i]["r"] = 0

            # run Loop 1
            run2 = 1
            for i in range(0,frame_number):
                if Frame[i]["r"] == 0 and Frame[i]["m"] == 0: # (0,0)
                    print("loop1_replace by: ",rs[index])
                    print("loop1_be replaced ",Frame[i]["value"])
                    print("")
                    Frame[i]["value"] = rs[index]
                    if modify[index] == 1:
                        Frame[i]["m"] = 1
                    else:
                        Frame[i]["m"] = 0
                    Frame[i]["r"] = 1
                    page_fault = page_fault + 1
                    index = index + 1
                    run2 = 0    
                    break
            #print('run2:',run2)
            if run2 == 0 :
                #print('bye')
                break    
            # run Loop 2
            run3 = 1
            if run2 == 1:
                for  i in  range(0,frame_number): 
                    if Frame[i]["r"] == 0 and Frame[i]["m"] == 1: # (0,1)
                        Frame[i]["value"] = rs[index]
                        page_fault = page_fault + 1
                        
                        if modify[index] == 1 :
                            Frame[i]["m"] = 1
                        else:
                            Frame[i]["m"] = 0
                        Frame[i]["r"] = 1    
                        run3 = 0
                        index = index + 1
                        #break
                    else:
                        Frame[i]["r"] = 0
            if run3 ==0 :
                break   

        
    

print("total page fault ",page_fault)
        

