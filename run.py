######################################################
#            Pleas Enter the SYNCH                   #   
# OFFSET-> YOU SOHULD ENTER IT AT THE COMMAND WINDOW #                                               
######################################################
SYNCH = 'amit' #synchronization id 
DATA_LENGTH = 6 # SIZE OF DATA IN MESSAGE IS THREE BYTES .

SYNCH_LEN = len(SYNCH)
SYNCH_TEMP_INDEX = -1
SAVE_TEMP = ''
SAVE_LIST = [] #STORING THE DATA WE EXPORT FROM MESSAGE . 
END_WITH_SYCH_FLAG = 0 #IF THE SYNCH CODE APPERS AT THE END OF MESSAGE, THE FLAG CHANGES TO 1.
END_WITH_HALF_SYCH_FLAG = 0#IF SOME OF SYNCH CODE APPERS AT THE END OF MESSAGE, THE FLAG CHANGES TO 1.
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
    
def check_beginning_of_message(msg):
    #This Function check if the beginning of the new message contains the other half of synch code.
    global SYNCH_TEMP_INDEX
    len = SYNCH_LEN 
    synch_index = SYNCH_TEMP_INDEX
    strr = msg
    counter = 1
    
    for ch in strr:
        if ch == SYNCH[synch_index]:
            counter+=1
            synch_index+=1
    if synch_index == len - 1:
        SYNCH_TEMP_INDEX = -1
        print("temp is"+str(counter))
        return counter
    SYNCH_TEMP_INDEX = -1
    return -1


def check_last_of_message(msg):
    #This function checks if the last of message contains some of the synchronization code.
    #return 1->found any , 0->didnt find any
    global SYNCH_TEMP_INDEX 

    strr = msg[-1 * SYNCH_LEN:]#Getting last possible chars to check if it contains any of synch code.
    synch_index = -1
    for ch in strr:
        if ch == SYNCH[synch_index+1]:
            synch_index += 1
    if synch_index == -1:
        return -1 #didnt find any synch code at end of message
    SYNCH_TEMP_INDEX= synch_index +1 #This index help us check the beginning of the next message if it contains synch code.
    return 1#Found somthing    
    
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
    global END_WITH_SYCH_FLAG,END_WITH_HALF_SYCH_FLAG,START_WITH_HALF_SYCH_FLAG,SAVE_LIST,SAVE_TEMP,SYNCH_TEMP_INDEX
    global SYNCH_FLAG
    ofset_index = contains_offset(msg,ofset)
    if ofset in msg:
        ofset_found_flag = 1
        if SYNCH_FLAG == 1:
            SYNCH_FLAG = 0
            if SAVE_TEMP != '' and msg.find(SYNCH)==-1 and check_beginning_of_message(msg) == -1 and check_last_of_message(msg)== -1:
                #SYNCH_FLAG = 0
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
        #In former message it ended with SYNCH then we should get the length of the offset
        END_WITH_SYCH_FLAG = 0
        ofset_index = contains_offset(msg[2:],ofset)
        if ofset_index != -1: 
            end_index = ofset_index
            save_to_list(2,end_index,msg)
        else:
            SAVE_TEMP += msg[2:]
            return
        
        
    if END_WITH_HALF_SYCH_FLAG == 1:#check the former message
        END_WITH_HALF_SYCH_FLAG = 0
        temp = check_beginning_of_message(msg[2:2+SYNCH_LEN-1-SYNCH_TEMP_INDEX])
        if temp != -1:
            ofset_index = contains_offset(msg[2:],ofset) 
            if ofset_index != -1:
                start_index = 2
                end_index = ofset_index
                save_to_list(start_index,end_index,msg[2:])
            else:
                SAVE_TEMP += msg[2:]
                return
        
    data_index = msg.find(SYNCH)#searching for SYNCH
    
    if data_index == -1:
        #it means there is no full SYNCH code so maybe there is half of it or less or more but not complete synchronization
         if check_last_of_message(msg)==1:
            END_WITH_HALF_SYCH_FLAG = 1       
    else:   
        SYNCH_FLAG = 1
        if msg[2:2+SYNCH_LEN] == SYNCH:#appers at first of the message 
            if ofset_found_flag == 1:
                ofset_found_flag = 0
                start_index = data_index+SYNCH_LEN
                end_index = ofset_index
                save_to_list(start_index,end_index,msg)
            else:
                SAVE_TEMP += msg[data_index+SYNCH_LEN:]
                return
        if SYNCH in msg[2+SYNCH_LEN:-1 * SYNCH_LEN]:
            #if there is in the middle of the message
            msg = msg[SYNCH_LEN:]
            data_index = msg.find(SYNCH)
            ofset_index = contains_offset(msg[data_index+SYNCH_LEN:],ofset)
            if ofset_index != -1:
                start_index = data_index+SYNCH_LEN
                end_index = data_index+SYNCH_LEN+ofset_index
                save_to_list(start_index,end_index,msg)
            else:
                SAVE_TEMP += msg[data_index+SYNCH_LEN:]    
                return
            
        if msg.endswith(SYNCH):
            END_WITH_SYCH_FLAG = 1 #it means that we should save first 3bytes in the next message.
            temp_flag = 1
        if check_last_of_message(msg) == 1:
            END_WITH_HALF_SYCH_FLAG = 1 #it means that we should look for some of synch code in the next message.
            
        else:
            END_WITH_HALF_SYCH_FLAG = 0
    print(SAVE_LIST)
    

def main():

    exit_flag =1
    offset = input("Enter an OFFSET:(example:0x124d)")
    
    while exit_flag == 1:
        message = input("Enter a message:\n")
        export_data(message,offset[2:])
        print()
        exit_flag = int(input("To Continue Press 1: "))
        
   
   

if __name__ == '__main__':
    main()
