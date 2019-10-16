# Enhanced Second Chance
rs =    [0,1,3,6,2,4,5,2,5,0,3,1,2,5,4,1,0] # reference string 
modify= [0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0] 
Frame = {}
frame_number = 4
index = 0

# Roud 1 - fill in
for i in range(frame_number): 
    if modify[index] == 1:
        Frame[i] = {"value":rs[index],"r":1,"m":1}
    else:
        Frame[i] = {"value":rs[index],"r":1,"m":0}   

    index = index + 1 

#print(Frame)

# Round 2 - judge whether page fault
"""
(r,m)
Loop 1 : search (0,0)
if not find,go Loop2
Loop 2 : search (0,1),Set the use bit to zero for all frames bypassed
* If step 2 failed, all use bits will now be zero and repetition of steps 1 and 2 are guaranteed to find a frame for replacement
"""




