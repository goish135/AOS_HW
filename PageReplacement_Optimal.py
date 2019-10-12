# Optimal Page Replacement Algorithm

#fn_tc1 = 3 # Number of frames
#rs_tc1 = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]

fn_tc1 = 4
rs_tc1 = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]

hits_tc1 = 0 
misses_tc1 = 0

frame = []
cnt   = 0 # list's length
index = 0 # rs_tc1's index
page_fault = 0

while cnt <  fn_tc1 :
    frame.append(rs_tc1[index])
    index = index + 1
    cnt = cnt + 1
    page_fault = page_fault + 1  

#print(frame)
print(page_fault)
#print(index)
#print(rs_tc1[index])

while index <= (len(rs_tc1) - 1):
    max = -1
    flag = 0
    if rs_tc1[index] in frame:
        pass
    else:
        for i in range(len(frame)):
            if frame[i] in rs_tc1[index+1:len(rs_tc1)]:
                print('how far? ',rs_tc1[index+1:len(rs_tc1)].index(frame[i]))
                if rs_tc1[index+1:len(rs_tc1)].index(frame[i]) > max :
                    max = frame[i] 
                    print('max:',max)
            else:
                max = frame[i]
                flag = 1 
                break
        print('error:',max)
        
        print('be replaced:',frame[frame.index(max)])
           
        print('replaced by:',rs_tc1[index])        
        frame[frame.index(max)] = rs_tc1[index]
        page_fault = page_fault + 1
    index = index + 1

print('Final Page Fault:',page_fault)    


                    

        








