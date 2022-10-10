SYNCH = 'f4f4' 
HALF_SYNCH = 'f4'
DATA_LENGTH = 0 # SIZE OF DATA IN MESSAGE IS THREE BYTES .

SAVE_TEMP = ''
SAVE_LIST = [] #STORING THE DATA WE EXPORT FROM MESSAGE . 
END_WITH_SYCH_FLAG = 0 #IF THE SYNCH CODE ('f4f4') APPERS AT THE END OF MESSAGE, THE FLAG CHANGES TO 1.
END_WITH_HALF_SYCH_FLAG = 0#IF HLAF SYNCH CODE ('f4')APPERS AT THE END OF MESSAGE, THE FLAG CHANGES TO 1.
START_WITH_HALF_SYCH_FLAG = 0
F4F4_FLAG = 0

def contains_offset(msg,ofset):
    return msg.find(ofset)
    
def save_to_list(start,end,msg):
    #Created this function to avoid duplicate code
    #This function saves data to a list\
    global SAVE_TEMP
    str_temp = msg[start:end+DATA_LENGTH]+SAVE_TEMP
    SAVE_TEMP = '' 
    SAVE_LIST.append(str_temp)
    
def extract_length(msg,ofset):
    #This function help us detect Data Length
    #After we find the Length we should update DATA_LENGTH global var
    global DATA_LENGTH
    len = msg[(ofset*2)-2:ofset*2]
    DATA_LENGTH = int(len)*2#Updating data len
   
def export_data(msg,ofset):
    #This is function used to identify 'f4f4' and 'f4'
    
    temp_flag = 0
    ofset_found_flag = 0
    global END_WITH_SYCH_FLAG,END_WITH_HALF_SYCH_FLAG,START_WITH_HALF_SYCH_FLAG,SAVE_LIST,SAVE_TEMP
    global F4F4_FLAG
    ofset_index = contains_offset(msg,ofset)
    if ofset in msg:
        ofset_found_flag = 1
        if F4F4_FLAG == 1:
            F4F4_FLAG = 0
            if SAVE_TEMP != '' and msg.find('f4f4')==-1 and msg.find('f4') == -1:
                #F4F4_FLAG = 0
                #WE SAVED A STREAM BEFORE

                SAVE_TEMP += msg[2:ofset_index]
                str_temp = SAVE_TEMP
                ofset_found_flag=0
                print("str temp is:"+str_temp)
                SAVE_LIST.append(str_temp)
                SAVE_TEMP = ''
                print(SAVE_LIST)
                return
            
    if END_WITH_SYCH_FLAG == 1:
        #In former message it ended with 'F4F4' then we should get the length of the offset
        END_WITH_SYCH_FLAG = 0
        ofset_index = contains_offset(msg[2:],ofset)
        if ofset_index != -1:
            start_index = 4
            end_index = ofset_index
            save_to_list(start_index,end_index,msg)
        else:
            SAVE_TEMP += msg[2:]
            return
        
        
    if END_WITH_HALF_SYCH_FLAG == 1:#check the former message
        END_WITH_HALF_SYCH_FLAG = 0
        ofset_index = contains_offset(msg[2:],ofset)
        if ofset_index != -1:
            start_index = 2
            end_index = ofset_index
            save_to_list(start_index,end_index,msg[2:])
        else:
            SAVE_TEMP += msg[2:]
            return
        
    data_index = msg.find(SYNCH)#searching for 'f4f4'
    
    if data_index == -1:
        #it means there is no full SYNCH code so maybe there is half of it (just 'f4' and not 'f4f4').
        data_index = msg.find(HALF_SYNCH)#search for 'f4'
        if msg[2:4] == 'f4' :#message start with 'f4' then we should check if the former message ended with 'f4'
            #START_WITH_HALF_SYCH_FLAG = 1   
            if END_WITH_HALF_SYCH_FLAG == 1:#check the former message
                END_WITH_HALF_SYCH_FLAG = 0
                save_to_list(4,4,msg)
        if msg.endswith('f4'):
            END_WITH_HALF_SYCH_FLAG = 1 #it means that we should look for 'f4' in the next message.        
    else:   
        F4F4_FLAG = 1
        if msg[2:6] == 'f4f4':#appers at first of the message
            if ofset_found_flag == 1:
                ofset_found_flag = 0
                start_index = data_index+4
                end_index = ofset_index
                save_to_list(start_index,end_index,msg)
            else:
                SAVE_TEMP += msg[data_index+4:]
                return
        if 'f4f4' in msg[4:-4]:
            #if there is in the middle of the message
            msg = msg[4:]
            data_index = msg.find('f4f4')
            ofset_index = contains_offset(msg[data_index+4:],ofset)
            if ofset_index != -1:
                start_index = data_index+4
                end_index = data_index+4+ofset_index
                save_to_list(start_index,end_index,msg)
            else:
                SAVE_TEMP += msg[data_index+4:]    
                return
            
        if msg.endswith('f4f4'):
            END_WITH_SYCH_FLAG = 1 #it means that we should save first 3bytes in the next message.
            temp_flag = 1
        #check if message ends with f4
        elif msg.endswith('f4'):
            END_WITH_HALF_SYCH_FLAG = 1 #it means that we should look for 'f4' in the next message.
    print(SAVE_LIST)
    

def main():

    exit_flag =1
    offset = input("Enter an OFFSET:")
    
    while exit_flag == 1:
        message = input("Enter a message:\n")
        export_data(message,offset[2:])
        exit_flag = int(input("To Continue Press 1: "))
        
   
   

if __name__ == '__main__':
    main()
