SYNCH = 'f4f4' 
HALF_SYNCH = 'f4'
DATA_LENGTH = 6 # SIZE OF DATA IN MESSAGE IS THREE BYTES .

SAVE_LIST = [] #STORING THE DATA WE EXPORT FROM MESSAGE . 
END_WITH_SYCH_FLAG = 0 #IF THE SYNCH CODE ('f4f4') APPERS AT THE END OF MESSAGE, THE FLAG CHANGES TO 1.
END_WITH_HALF_SYCH_FLAG = 0#IF HLAF SYNCH CODE ('f4')APPERS AT THE END OF MESSAGE, THE FLAG CHANGES TO 1.
START_WITH_HALF_SYCH_FLAG = 0


def save_to_list(start,end,msg):
    #Created this function to avoid duplicate code
    #This function saves data to a list
    str_temp = "0xf4f4"+msg[start:end+DATA_LENGTH]
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
    global END_WITH_SYCH_FLAG,END_WITH_HALF_SYCH_FLAG,START_WITH_HALF_SYCH_FLAG,SAVE_LIST
    
    if END_WITH_SYCH_FLAG == 1:
        #In former message it ended with 'F4F4' then we should get the length of the offset
        END_WITH_SYCH_FLAG = 0
        extract_length(msg[2:],ofset)
        index = 2+ofset*2
        save_to_list(index,index,msg)
        
    if END_WITH_HALF_SYCH_FLAG == 1:#check the former message
        END_WITH_HALF_SYCH_FLAG = 0
        extract_length(msg[4:],ofset)
        index = 4+ofset*2
        save_to_list(index,index,msg)
        
        
    data_index = msg.find(SYNCH)#searching for 'f4f4'
    
    if data_index == -1:
        #it means there is no full SYNCH code so maybe there is half of it (just 'f4' and not 'f4f4').
        data_index = msg.find(HALF_SYNCH)#search for 'f4'
        if data_index == -1:
            print(SAVE_LIST)
            return #exit the function 
        elif msg.endswith('f4'):
            END_WITH_HALF_SYCH_FLAG = 1 #it means that we should look for 'f4' in the next message.
        if msg[2:4] == 'f4' :#message start with 'f4' then we should check if the former message ended with 'f4'
            #START_WITH_HALF_SYCH_FLAG = 1   
            if END_WITH_HALF_SYCH_FLAG == 1:#check the former message
                END_WITH_HALF_SYCH_FLAG = 0
                save_to_list(4,4,msg)
                
    else:   
        if msg[2:6] == 'f4f4':#appers at first of the message
            extract_length(msg[6:],ofset)
            index = data_index+4+ofset*2
            save_to_list(index,index,msg)
            
        if 'f4f4' in msg[4:-4]:
            #if there is in the middle of the message
            msg = msg[4:]
            data_index = msg.find('f4f4')
            extract_length(msg[data_index+4:],ofset)
            index = data_index+4+ofset*2
            save_to_list(index,index,msg)
            
        if msg.endswith('f4f4'):
            END_WITH_SYCH_FLAG = 1 #it means that we should save first 3bytes in the next message.
            temp_flag = 1
        #check if message ends with f4
        elif msg.endswith('f4'):
            END_WITH_HALF_SYCH_FLAG = 1 #it means that we should look for 'f4' in the next message.
            
    print(SAVE_LIST)

def main():

    exit_flag =1
    offset = input("Enter an offset byte:")
    
    while exit_flag == 1:
        message = input("Enter a message:\n")
        export_data(message,int(offset))
        exit_flag = int(input("To Continue Press 1: "))
        
   
   

if __name__ == '__main__':
    main()
