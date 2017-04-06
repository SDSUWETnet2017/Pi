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
            print('In first ret 0\n')
        return 0
   
    # convert string hex vals to int hex vals
    if len(rv) < 6:
        for i in range(2,len(rv)):
            try:
                rv[i] = int(rv[i],base=16)
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
        print('In 2nd ret 0\n')
        return 0


    
def read_start_seq(port):
    '''
    A function that lets the PI know when to start reading data from
    PIC
    '''
    print("\nWaiting to Pair with PIC")
    rv = ''
    while True:
        ch = port.read()
        rv += ch
        print(ch)
        #port.write(str.encode("U"))
        if "X" and 'U' in rv:
            return


