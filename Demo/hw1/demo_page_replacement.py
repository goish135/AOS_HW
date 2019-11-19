# Driver Code #
import sys
import json

answer_PageFault = 0
answer_Interrupt = 0
answer_DiskWrite = 0

def judge_mode(num):
    if num == 1:
        #print("Random RS")
        return "random"
    elif num == 2:
        #print("Locality RS")
        return "locality"
    elif num == 3:
        #print("Custom RS")
        return "custom"
def input_rs(strstr):
    with open("input.json","r") as load_f:
        load_dict = json.load(load_f)

    if strstr=="random":
        return load_dict["random"]
    elif strstr=="locality":
        return load_dict["locality"]
    elif strstr=="custom":
        dict_custom = {}
        #dict_custom[10] = load_dict["custom_10"]
        frame_number = 10
        while frame_number <= 100:
            key = "custom_"+ str(frame_number)
            dict_custom[frame_number] = load_dict[key]
            frame_number = frame_number + 10
        return dict_custom    

def dw_ds():
    with open("input.json","r") as load_f:
        load_dict = json.load(load_f)
    return load_dict['dw_set']                      

def fifo(mode):
    print("FIFO X ",judge_mode(mode))
    custom_run = 0
    if judge_mode(mode) == "random":
        # read dict["random"]
        rs = input_rs("random")
        print(type(rs))
    elif judge_mode(mode) == "locality":
        rs = input_rs("locality")
        print(type(rs))
    elif judge_mode(mode) == "custom":
        rs_dict = input_rs("custom")
        custom_run = 1
        print(type(rs_dict))        
    dw_set = dw_ds()
    import queue
    if custom_run==1:
        frame_number = 10    
        #for i in range(10):
        while frame_number <= 100 :
            rs = rs_dict[frame_number]
            #frame_number = input("Number of frame: ")     
            myqueue = queue.Queue(int(frame_number))
            page_fault_sum = 0
            interrupt = 0
            disk_write = 0


            cnt = 0 
            while myqueue.full()!=True :
                myqueue.put(rs[cnt])
                cnt = cnt + 1
                page_fault_sum = page_fault_sum + 1

            print('page_fault_sum:',page_fault_sum)



            # 塞滿了，要塞下一個 先看 page 是否在 queue 裡 
            # 有 則 hit , 沒有 則 miss 

            while cnt != len(rs) : 
                if rs[cnt] in myqueue.queue:    
                    pass
                else:
                    interrupt = interrupt + 1
                    page_fault_sum = page_fault_sum + 1
                    if dw_set[rs.index(myqueue.get())] == 1 : # modify
                        disk_write = disk_write + 1
                    #myqueue_10.get()
                    myqueue.put(rs[cnt])
                cnt = cnt + 1

            print('page_fault_sum: ',page_fault_sum)
            print('inteerrupt: ',interrupt)
            print('disk write: ',disk_write)
            print("===============================")
            #answer_PageFault = page_fault_sum
            #answer_Interrupt = interrupt
            #answer_DiskWrite = disk_write            
            # 寫入 csv
            import csv
            with open('demo_statistic.csv','a',newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([argvlist[1],argvlist[2],frame_number,page_fault_sum,interrupt,disk_write])
            frame_number = frame_number + 10

    frame_number = 10    
    #for i in range(10):
    while frame_number <= 100 and custom_run==0:
        #frame_number = input("Number of frame: ")     
        myqueue = queue.Queue(int(frame_number))
        page_fault_sum = 0
        interrupt = 0
        disk_write = 0


        cnt = 0 
        while myqueue.full()!=True :
            myqueue.put(rs[cnt])
            cnt = cnt + 1
            page_fault_sum = page_fault_sum + 1

        print('page_fault_sum:',page_fault_sum)



        # 塞滿了，要塞下一個 先看 page 是否在 queue 裡 
        # 有 則 hit , 沒有 則 miss 

        while cnt != len(rs) : 
            if rs[cnt] in myqueue.queue:    
                pass
            else:
                interrupt = interrupt + 1
                page_fault_sum = page_fault_sum + 1
                if dw_set[rs.index(myqueue.get())] == 1 : # modify
                    disk_write = disk_write + 1
                #myqueue_10.get()
                myqueue.put(rs[cnt])
            cnt = cnt + 1

        print('page_fault_sum: ',page_fault_sum)
        print('inteerrupt: ',interrupt)
        print('disk write: ',disk_write)
        print("===============================")
        #answer_PageFault = page_fault_sum
        #answer_Interrupt = interrupt
        #answer_DiskWrite = disk_write        
                        
        # 寫入 csv
        import csv
        with open('demo_statistic.csv','a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([argvlist[1],argvlist[2],frame_number,page_fault_sum,interrupt,disk_write])
        frame_number = frame_number + 10    

def optimal(mode):
    print("Optimal X ",judge_mode(mode))
    custom_run = 0
    if judge_mode(mode) == "random":
        # read dict["random"]
        rs = input_rs("random")
        print(type(rs))
    elif judge_mode(mode) == "locality":
        rs = input_rs("locality")
        print(type(rs))
    elif judge_mode(mode) == "custom":
        rs_dict = input_rs("custom")
        custom_run = 1
        print(type(rs_dict))

    dw_set = dw_ds()
    if custom_run == 1:
        print("check*")
        frame_number = 10
        #for i in range(10):
        while frame_number <= 100 :
            rs = rs_dict[frame_number]
            #fn_tc1 = input("輸入frame數: ")
            fn_tc1 = int(frame_number)

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
                frame.append(rs[index])
                frame_record.append(int(0))

                cnt = cnt + 1
                page_fault = page_fault + 1
                for i in range(len(frame)):      
                    if frame[i] in rs[index+1:len(rs)]:
                        frame_record[i] = rs[index+1:len(rs)].index(frame[i]) - index
                    else:
                        frame_record[i] = (100000+1) 
                index = index + 1              



            #print(frame)
            print(page_fault)
            #print(index)
            #print(rs_tc1[index])

            while index <= (len(rs) - 1):
                #print("rs: ",index)
                #max = -1
                flag = 0
                if rs[index] in frame:
                    pass
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
                    """ graph
                    if dw_set[rs.index(frame[victim_page_index])] == 1:
                        dw = dw + 1
                    """
                    ###
                    for k in range(index-1,0,-1):
                        if rs[k] == frame[victim_page_index]:
                            if dw_set[k] == 1:
                                dw = dw + 1
                            break
                    ###     
                    for k in range(fn_tc1):
                        frame_record[k] = frame_record[k] - 1

                    frame[victim_page_index] = rs[index]
                    # 計算新進來 的 page 的距離
                    if frame[victim_page_index] in rs[index+1:len(rs)]:
                        frame_record[victim_page_index] = rs[index+1:len(rs)].index(frame[victim_page_index]) - index
                    else:
                        frame_record[victim_page_index] = (100000+1)

                    page_fault = page_fault + 1
                    interrupt = interrupt + 1
                index = index + 1

            print('Final Page Fault: ',page_fault)
            print('interrupt: ',interrupt)
            print('disk write: ',dw)
            print("=============================")
            #answer_PageFault = page_fault
            #answer_Interrupt = interrupt
            #answer_DiskWrite = dw
            # 寫入 csv
            import csv
            with open('demo_statistic.csv','a',newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([argvlist[1],argvlist[2],frame_number,page_fault,interrupt,dw]) 

            frame_number = frame_number + 10        
    frame_number = 10
    #for i in range(10):
    while frame_number <= 100 and custom_run==0:
        #fn_tc1 = input("輸入frame數: ")
        fn_tc1 = int(frame_number)

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
            frame.append(rs[index])
            frame_record.append(int(0))

            cnt = cnt + 1
            page_fault = page_fault + 1
            for i in range(len(frame)):      
                if frame[i] in rs[index+1:len(rs)]:
                    frame_record[i] = rs[index+1:len(rs)].index(frame[i]) - index
                else:
                    frame_record[i] = (100000+1) 
            index = index + 1              



        #print(frame)
        print(page_fault)
        #print(index)
        #print(rs_tc1[index])

        while index <= (len(rs) - 1):
            #print("rs: ",index)
            #max = -1
            flag = 0
            if rs[index] in frame:
                pass
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
                """
                if dw_set[rs.index(frame[victim_page_index])] == 1:
                    dw = dw + 1
                """
                ### update
                for k in range(index-1,0,-1):
                    if rs[k] == frame[victim_page_index]:
                        if dw_set[k] == 1:
                            dw = dw + 1
                        break
                ###
                for k in range(fn_tc1):
                    frame_record[k] = frame_record[k] - 1

                frame[victim_page_index] = rs[index]
                # 計算新進來 的 page 的距離
                if frame[victim_page_index] in rs[index+1:len(rs)]:
                    frame_record[victim_page_index] = rs[index+1:len(rs)].index(frame[victim_page_index]) - index
                else:
                    frame_record[victim_page_index] = (100000+1)

                page_fault = page_fault + 1
                interrupt = interrupt + 1
            index = index + 1

        print('Final Page Fault: ',page_fault)
        print('interrupt: ',interrupt)
        print('disk write: ',dw)
        print("=============================")
        #answer_PageFault = page_fault
        #answer_Interrupt = interrupt
        #answer_DiskWrite = dw
        
        # 寫入 csv
        import csv
        with open('demo_statistic.csv','a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([argvlist[1],argvlist[2],frame_number,page_fault,interrupt,dw])
        frame_number = frame_number + 10     

def esc(mode):
    custom_run = 0
    print("esc X ",judge_mode(mode))
    if judge_mode(mode) == "random":
        # read dict["random"]
        rs = input_rs("random")
        print(type(rs))
    elif judge_mode(mode) == "locality":
        rs = input_rs("locality")
        print(type(rs))
    elif judge_mode(mode) == "custom":
        rs_dict = input_rs("custom")
        custom_run = 1
        print(type(rs_dict))
        #print(rs[10])
        #print(rs[100])
        #print(type(rs[100]))
        #input("stop")

    frame_number = 10
    modify = dw_ds()
    Frame = {}    
    
    if custom_run == 1:
        while frame_number <= 100:
            #frame_number=input("輸入frame數量")
            frame_number = int(frame_number)
            index = 0
            page_fault = 0
            interrupt = 0
            dw = 0
            pointer = 0 
            rs = rs_dict[frame_number]

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
                                pointer = (pointer%(frame_number-1)) + 1
                                break # Loop1
                            else:
                                pointer = pointer + 1
                                
                            if pointer >= (frame_number-1):
                                pointer = (pointer%(frame_number-1)) + 1
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
                                    pointer = (pointer%(frame_number-1)) + 1
                                    break # Loop 2
                                else:
                                    #pointer = (pointer%4) + 1
                                    Frame[pointer]["r"] = 0
                                    pointer = pointer + 1
                                
                                if pointer >= (frame_number-1) :
                                    pointer = (pointer%(frame_number-1)) + 1
                                    #print("out_of_Loop2")
                                    break

                        if out_of_Loop2 == 1 :
                            break   # jump out While True == 不用再找下去

                    

            #for i in range(frame_number):
            #    print(Frame[i]["value"]," ",Frame[i]["r"]," ",Frame[i]["m"])
            print("total page fault ",page_fault)
            print("interrupt ",interrupt)
            print("dw ",dw)
            print("============================")
            #answer_PageFault = page_fault
            #answer_Interrupt = interrupt
            #answer_DiskWrite = dw            
                    
            # 寫入 csv
            import csv
            with open('demo_statistic.csv','a',newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([argvlist[1],argvlist[2],frame_number,page_fault,interrupt,dw]) 
            frame_number = frame_number + 10    

    frame_number = 10
    modify = dw_ds()
    Frame = {}
    #for k in range(10):
    while frame_number <= 100 and custom_run==0:
        #frame_number=input("輸入frame數量")
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
                            pointer = (pointer%(frame_number-1)) + 1
                            break # Loop1
                        else:
                            pointer = pointer + 1
                            
                        if pointer >= (frame_number-1):
                            pointer = (pointer%(frame_number-1)) + 1
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
                                pointer = (pointer%(frame_number-1)) + 1
                                break # Loop 2
                            else:
                                #pointer = (pointer%4) + 1
                                Frame[pointer]["r"] = 0
                                pointer = pointer + 1
                            
                            if pointer >= (frame_number-1) :
                                pointer = (pointer%(frame_number-1)) + 1
                                #print("out_of_Loop2")
                                break

                    if out_of_Loop2 == 1 :
                        break   # jump out While True == 不用再找下去

                

        #for i in range(frame_number):
        #    print(Frame[i]["value"]," ",Frame[i]["r"]," ",Frame[i]["m"])
        print("total page fault ",page_fault)
        print("interrupt ",interrupt)
        print("dw ",dw)
        print("============================")
        #answer_PageFault = page_fault
        #answer_Interrupt = interrupt
        #answer_DiskWrite = dw        
        
        # 寫入 csv
        import csv
        with open('demo_statistic.csv','a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([argvlist[1],argvlist[2],frame_number,page_fault,interrupt,dw])
            frame_number = frame_number + 10 
def lru_pro(mode):
    print("LRU_Pro X ",judge_mode(mode))
    custom_run = 0
    if judge_mode(mode) == "random":
        # read dict["random"]
        rs = input_rs("random")
        print(type(rs))
    elif judge_mode(mode) == "locality":
        rs = input_rs("locality")
        print(type(rs))
    elif judge_mode(mode) == "custom":
        rs_dict = input_rs("custom")
        custom_run = 1
        print(type(rs_dict))
        #print(rs[10])
        #print(rs[100])
        #print(type(rs[100]))
        #input("stop")
    dw_set = dw_ds()
    if custom_run == 1:
        fn = 10
        #for z in range(10):
        while fn <= 100 :
            rs = rs_dict[fn]
            #fn = input("輸入frame數: ")
            fn = int(fn)
            page_fault = 0
            dw = 0
            interrupt = 0

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
                #print(frame)
                #print(">>>",frame_record)
                #print("")
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

                    for k in range(index-1,0,-1):
                        if rs[k] == frame[frame_record.index(min_value)]:
                            if dw_set[k] == 1 :
                                dw = dw + 1
                            break    
                    
                    frame.remove(frame[frame_record.index(min_value)])     
                    frame.append(rs[index])
                    del frame_record[frame_record.index(min_value)]
                    frame_record.append(1)
                    interrupt = interrupt + 1
                    page_fault = page_fault + 1

                index = index + 1
            print(page_fault)
            print(interrupt)
            print(dw)
            print("=====================")
            #answer_PageFault = page_fault
            #answer_Interrupt = interrupt
            #answer_DiskWrite = dw
            
            # 寫入 csv
            import csv
            with open('demo_statistic.csv','a',newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([argvlist[1],argvlist[2],fn,page_fault,interrupt,dw])
            fn = fn + 10                 
    fn = 10
    #for z in range(10):
    while fn <= 100 and custom_run==0:
        #fn = input("輸入frame數: ")
        fn = int(fn)
        page_fault = 0
        dw = 0
        interrupt = 0

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
            #print(frame)
            #print(">>>",frame_record)
            #print("")
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

                for k in range(index-1,0,-1):
                    if rs[k] == frame[frame_record.index(min_value)]:
                        if dw_set[k] == 1 :
                            dw = dw + 1
                        break    
                
                frame.remove(frame[frame_record.index(min_value)])     
                frame.append(rs[index])
                del frame_record[frame_record.index(min_value)]
                frame_record.append(1)
                interrupt = interrupt + 1
                page_fault = page_fault + 1

            index = index + 1
        print(page_fault)
        print(interrupt)
        print(dw)
        print("=====================")
        #answer_PageFault = page_fault
        #answer_Interrupt = interrupt
        #answer_DiskWrite = dw
        
        # 寫入 csv
        import csv
        with open('demo_statistic.csv','a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([argvlist[1],argvlist[2],fn,page_fault,interrupt,dw])
        fn = fn + 10                 
if __name__ == "__main__":
    argvlist = sys.argv
    if len(sys.argv) == 2 :
        if argvlist[1] == "--help":
            print("Format :")
            print("python demo_page_replacement.py algo? input_type?")
    elif len(sys.argv) == 3:
        if argvlist[1] == "-f" and argvlist[2]=="-r":
            fifo(1)
        elif argvlist[1] == "-f" and argvlist[2]=="-l":
            fifo(2)
        elif argvlist[1] == "-f" and argvlist[2]=="-c":
            fifo(3)
        elif argvlist[1] == "-o" and argvlist[2]=="-r":
            optimal(1)
        elif argvlist[1] == "-o" and argvlist[2]=="-l":
            optimal(2)
        elif argvlist[1] == "-o" and argvlist[2]=="-c":
            optimal(3)
        elif argvlist[1] == "-e" and argvlist[2]=="-r":
            esc(1)
        elif argvlist[1] == "-e" and argvlist[2]=="-l":
            esc(2)
        elif argvlist[1] == "-e" and argvlist[2]=="-c":
            esc(3)
        elif argvlist[1] == "-lp" and argvlist[2]=="-r":
            lru_pro(1)
        elif argvlist[1] == "-lp" and argvlist[2]=="-l":
            lru_pro(2)
        elif argvlist[1] == "-lp" and argvlist[2]=="-c":
            lru_pro(3)
        else:
            print("Format :")
            print("python demo_page_replacement.py algo? input_type?")
    else:
        print("Format :")
        print("python demo_page_replacement.py algo? input_type?")
    """    
    print(answer_PageFault)
    print(answer_Interrupt)
    print(answer_DiskWrite)

    # 寫入 csv
    import csv
    with open('demo_statistic.csv','a',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([argvlist[1],argvlist[2],answer_PageFault,answer_Interrupt,answer_DiskWrite])
    """

    # 繪圖 | FIFO x LRU Pro x Optimal
                 





