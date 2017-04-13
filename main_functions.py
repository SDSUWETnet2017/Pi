import time
def read_data(port):
    '''
    A function that reads data from the serial port and returns
    a split list of the data
    '''

    rv = ''
    while True:
        ch = port.read()
        print(ch)
        if ch =='U' or len(rv) > 30:
            break
        else:
            rv += ch
    # split data string into an array by looking for spaces
    rv = rv.split(' ')
    print(rv)
    # if supernode data don't convert first element to int
    try:
        if rv[1] == 'END':
            pass
        else:
            rv[1] == int(rv[1][-1],base=10) #int(rv[0],base=10)
    except:
        with open('Error_Log.txt','a') as f_obj:
            print('could not store data due to corrupted packet \n')
            msg = '- ' + time.strftime('%Y-%m-%d %H:%M',time.localtime())
            msg += ' could not store data due to corrupted packet \n'
            f_obj.write(msg)
            f_obj.close()
            #print('In first ret 0\n')
        return 0
   
    # convert string hex vals to int hex vals
    if len(rv) < 6:
        for i in range(2,len(rv)):
            try:
                rv[i] = float(rv[i])
            except ValueError:
                # if hex element has corrupted val then wrie ffff to
                # element subnode subclasswill will wrie to log that this val
                # lost
                rv[i] = 0xFFFF
                
        return rv[1:]
    elif rv[1] == 'END':
        for i in range(2,len(rv)):
            try:
                rv[i] = int(rv[i],base=16)
            except ValueError:
                # if hex element has corrupted val then wrie ffff to
                # element subnode subclasswill will wrie to log that this val
                # lost
                rv[i] = 0xFFFF
        return rv[1:]
    else:
        #print('In 2nd ret 0\n')
        return 0


    
def read_start_seq(port):
    '''
    A function that lets the PI know when to start reading data from
    PIC
    '''
    print("\nWaiting to Pair with PIC")
    node = 2
    comparison = "Node " + str(node) + " Paired" #Node %c Paired" sent from pic
    rv = ''
    while True:
        ch = port.read()
        rv += ch
        #print(ch)
        #port.write(str.encode("U"))
        
        if comparison in rv:
            print(comparison +"\n")
            writeLog(comparison)
            node += 1
            comparison = "Node " + str(node) + " Paired" #Node %c Paired" sent from pic
            if node == 6:
                return

            

def get_time_stamp():
    '''
    A function that generates a timestamp in the form
    MM/DD/YYYY HH:mm if a number is less than 10 it will
    not be 0 padded 
    '''
    
    time_struct = time.localtime()
    timestamp = str(time_struct[1]) + '/' +str(time_struct[2])+'/'
    timestamp += str(time_struct[0]) + ' ' + str(time_struct[3])
    timestamp += ':' + str(time_struct[4])
    return timestamp

def sync_PIC(port,period_end,period=10):
    """
    This function compares the end cycle given from pic to PI time and
    sends a + or - to the PIC over UART if the PI needs to adjust its clock.
    If pic time is correct no signal will be sent.

    If end period is 1s over then the pic clock will be adjusted by 0.5s
    """

    # get time of end cycle and compare it to 10 minutes
    # delta_t is time difference between 10 minutes what the pic is
    delta_t = time.time() - period_end - (period * 60)
    
    if abs(delta_t) < 1:
        return
    elif delta_t > 0:
        #print('subtracting from pic clk')
        port.write(str.encode('-'))
        return
    elif delta_t < 0:
        #print('adding to pic clk')
        port.write(str.encode('+'))
        return
    return
        
def writeLog(msg):
    log = '--' + time.strftime('%Y-%m-%d %H:%M')
    log += ' ' + msg
    with open('log.txt', 'a') as f_obj:
	f_obj.write(log)
	f_obj.close()
    
    
    
