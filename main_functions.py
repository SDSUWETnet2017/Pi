def read_data(port):
    '''
    A function that reads data from the serial port and returns
    a split list of the data
    '''

    rv = ''
    while True:
        ch = port.read()
        print(ch)
        if ch =='U':
            break
        else:
            rv += ch
    # split data string into an array by looking for spaces
    rv = rv.split(' ')
    print(rv)
    # if supernode data don't convert first element to int
    if rv[0] == 'END':
        pass
    else:
        rv[0] == int(rv[0],base=10)
        
    # convert string hex vals to int hex vals 
    for i in range(1,len(rv)):
        rv[i] = int(rv[i],base=16)
    return rv
