SYNCH = 'f4f4' 
HALF_SYNCH = 'f4'
DATA_LENGTH = 6 # SIZE OF DATA IN MESSAGE IS THREE BYTES .

SAVE_LIST = [] #STORING THE DATA WE EXPORT FROM MESSAGE . 
END_WITH_SYCH_FLAG = 0 #IF THE SYNCH CODE ('f4f4') APPERS AT THE END OF MESSAGE, THE FLAG CHANGES TO 1.
END_WITH_HALF_SYCH_FLAG = 0#IF HLAF SYNCH CODE ('f4')APPERS AT THE END OF MESSAGE, THE FLAG CHANGES TO 1.
START_WITH_HALF_SYCH_FLAG = 0

def export_data(msg):
    temp_flag = 0
    global END_WITH_SYCH_FLAG,END_WITH_HALF_SYCH_FLAG,START_WITH_HALF_SYCH_FLAG,SAVE_LIST
    if END_WITH_SYCH_FLAG == 1:
        END_WITH_SYCH_FLAG = 0
        str_temp = "0xf4f4"+msg[2:2+DATA_LENGTH]
        SAVE_LIST.append(str_temp)
        
    data_index = msg.find(SYNCH)#searching for 'f4f4'
    print('data index is:'+str(data_index))
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
                str_temp = "0xf4f4"+msg[4:4+DATA_LENGTH]
                SAVE_LIST.append(str_temp)
    else:
        if msg.endswith('f4f4'):
            END_WITH_SYCH_FLAG = 1 #it means that we should save first 3bytes in the next message.
            temp_flag = 1
            
        if msg[2:6] == 'f4f4':#appers at first of the message   
            str_temp = "0xf4f4"+msg[data_index+4:data_index+4+DATA_LENGTH]
            SAVE_LIST.append(str_temp)#adding the data to the list
            
        if 'f4f4' in msg[4:] and temp_flag==1:
            #There is two 'f4f4' in the message one in the middle and one in the end.
            msg = msg[4:-4]
            data_index = msg.find('f4f4')
            str_temp = "0xf4f4"+msg[data_index+4:data_index+4+DATA_LENGTH]
            SAVE_LIST.append(str_temp)#adding the data to the list
        else:
            str_temp = "0xf4f4"+msg[data_index+4:data_index+4+DATA_LENGTH]
            SAVE_LIST.append(str_temp)#adding the data to the list
            
    print(SAVE_LIST)

def main():

    exit_flag =1
    while exit_flag == 1:
        message = input("Enter a message:\n")
        export_data(message)
        exit_flag = int(input("To Continue Press 1: "))
        
   
   

if __name__ == '__main__':
    main()