# 怪怪der because page fault in optimal is 4 + 3 = 7,but in block reading is 2
# block reading from secondary storage
# RS長度: 10 0000 ; frame 數 : 10 ~ 100 (interval:10)
# rs : 1 1 3 2 0 5 6 2 4 5

# if 不在 memory , page miss,then read a block of page to fill up memory frame
# if 在 memory , page hit

rs = [1,1,3,2,0,5,6,2,4,5]
fn = 4
frame = []
index = 0 # rs's index 
page_fault = 0

while index < len(rs):
    tmp = index 
    if rs[index] not in frame:
        page_fault = page_fault + 1
        print("not found: ",rs[index])

        first = 0
        while len(frame) < fn :
            first = 1

            if rs[tmp] not in frame:
                frame.append(rs[tmp])
                tmp = tmp + 1
            else:
                tmp = tmp + 1
        if first == 0 :
            print("index: ",index)        
            noReplace = []        
            for i in range(index,index+fn):
                if i >= len(rs):
                    print("de")
                    break

                if rs[i] in frame:
                    # nochange
                    noReplace.append(rs[i])
            """
            for i in range(fn):
                if tmp >= len(rs):
                    print("DE")
                    break
                if frame[i] not in noReplace:
                    print("tmp: ",tmp)
                    frame[i] = rs[tmp]
                    tmp = tmp + 1
            """
            j = 0 
            for i in range(index,index+fn):
                if i >= len(rs):
                    print("de")
                    break
                while j < fn:
                    print('loop?')
                    if frame[j] not in noReplace:
                        frame[j] = rs[i]
                        print(j," ",frame[j])
                        j = j + 1
                        break
                    else:
                        # no replacement
                        j = j + 1
                        break

                      
    else:
        pass            
    index = index + 1

print("page fault: ",page_fault)
              
