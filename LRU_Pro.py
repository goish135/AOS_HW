# LRU Pro
# example rs : 7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1
# frame number : 3
# LRUPro > page fault : 11
# Optimal > page fault : 9
# Fifo > page fault : 13 

"""
priority 1 : 使用間斷次數
priority 2 : FIFO
"""
rs = [7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]
fn = 3
page_fault = 0

frame = []
frame_record = []

index = 0
for i in range(fn):
    #print(rs[index])
    frame.append(rs[index])
    frame_record.append(1)
    index = index + 1
    page_fault = page_fault + 1

#print(len(frame))
#print(len(frame_record))
print(page_fault)
while index < len(rs):
    print(frame)
    print(">>>",frame_record)
    print("")
    if rs[index] in frame:
        frame_record[frame.index(rs[index])] = frame_record[frame.index(rs[index])] + 1

        tmp1=frame_record[frame.index(rs[index])]
        del frame_record[frame.index(rs[index])]
        frame_record.append(tmp1)

        tmp2 = frame[frame.index(rs[index])]
        del frame[frame.index(rs[index])]
        frame.append(tmp2)
         
    else:
        """       
        min = 100000+1
        multiple = []
        for i in range(fn):
            if frame_record[i] < min :
                
                min = frame_record[i]
            elif frame_record[i] == min    
        if len(multiple) > 1 :
            frame[multiple]
        """
        #multiple = []
        min_value = min(frame_record)
        
        """
        for i in range(fn):
            if frame_record[i] == min_value:
                multiple.append(i)
        """
        """
        for i in range(frame_record.index(min_value),fn):
            if i == (fn-1):
                frame_record[i] = 1
            else:
                frame_record[i] = frame_record[i+1]
        """

        #tmp3=frame_record[frame.index(rs[index])]


        frame.remove(frame[frame_record.index(min_value)])     
        frame.append(rs[index])
        del frame_record[frame_record.index(min_value)]
        frame_record.append(1)

        page_fault = page_fault + 1
    index = index + 1

print(frame)
print(frame_record)
print(page_fault)
        

                

        
        





