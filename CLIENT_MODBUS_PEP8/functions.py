# -------------------------------------------------------------------------------
# Python version 3
# Advices:
# ---------
# * Use Bytearray to send and receive frame
# * gv.MODBUS_SOCKET.send(request), allows to send the 'request' bytearray to the modbus server
# * To get the response:
#       response = bytearray(gv.MODBUS_SOCKET.recv(max_buff))
#       with 'max_buff' the maximal size of the response
# -------------------------------------------------------------------------------

import global_variables as gv
import socket as socket


def display_menu(state):
    print("\n####################")
    print("-  MODBUS CLIENT -")
    if state == 0:
        print("- state: disconnected -")
        print("####################\n")
        print("[C]\t: Connect to the server")
        print("[Q]\t: Quit")
        print("-----------------")
    else:
        print("-  state: connected -")
        print("####################\n")
        print("[1,2]\t: Read N bits")
        print("[3,4]\t: Read N registers")
        print("[5] \t: Write 1 bit")
        print("[6] \t: Write 1 register")
        print("[15] \t: write N bits")
        print("[16] \t: Write N registers")
        print("[D]\t: Disconnect")
        print("[Q]\t: Quit")
        print("-----------------")


def connection():
    # recover the IP address
    i_ip = input("Server IP address (default: "+gv.MODBUS_SERVER_IP+")")
    if i_ip == "":
        i_ip = gv.MODBUS_SERVER_IP
    # recover the port number
    i_port = input("Server port number (default: "+str(gv.MODBUS_SERVER_PORT) + ")")
    if i_port == "":
        i_port = gv.MODBUS_SERVER_PORT
    else:
        i_port = int(i_port)
    try:
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((i_ip, i_port))
    except socket.error:
        return 0, str(socket.error)
    return 1, "OK"


def disconnection():
    try:
        gv.MODBUS_SOCKET.close()
    except socket.error:
        return 1, str(socket.error)
    return 0, "OK"


def read_n_bits(nb_bits, add_first):
    """
    Function to read N bits
    :param nb_bits: the number of consecutive bits to read 
    :param add_first: the address of the first bit
    :return: True of False, list of the bit values, a string message
    """
    # TODO
    try:
        #Variables
        code_fct=0x01
        size_of=6

        #READ N=nb_bits COILS(BIT)
        # id_tran(2) + id_proto(2)=0x0000 +size_of(2)+ id_server(1) + fct_code(1)=0x06 +@firstBit(2) +nb_bits_to_read(2)
        trame = bytearray([gv.ID_TRANSACTION>>8 & 0xFF, gv.ID_TRANSACTION & 0xFF, 0, 0, size_of // 256, size_of % 256, gv.ID_SERVER, code_fct, add_first // 256, add_first % 256,nb_bits // 256, nb_bits % 256])

        #Send Request
        gv.MODBUS_SOCKET.send(trame)

        #Response
        response=bytearray(gv.MODBUS_SOCKET.recv(gv.MAX_BUFFER))
        
        # Check the response for success
        if response[7] == code_fct:
            rep=list(response)[9:] #list of byte read
            print(rep)
            bits=[]
            for byte in rep:
                shift=0 #decalage =0...7
                while len(bits)<nb_bits and shift<8:
                    bits.append(byte>>shift & 0x01)
                    shift+=1;
            return True,bits, f"Read {nb_bits} bits successful"
        else:
            return False,[], f"Failed to read {nb_bitss} bits"

    except Exception as e:
        return False,[], str(e)


def read_n_words(nb_words, add_first):
    """
    Function to write N registers (words)
    :param nb_words: the number of consecutive words to read
    :param add_first: the address of the first word
    :return: True of False, list of the word values, a string message
    """
    # TODO
    try:
        #Variables
        code_fct=0x03
        size_of=6;

        #READ N=nb_words REGISTERS
        # id_tran(2) + id_proto(2)=0x0000 +size_of(2)+ id_server(1) + fct_code(1)=0x03 +@firstRegister(2) +nb_registers_to_read(2)
        trame = bytearray([gv.ID_TRANSACTION>>8 & 0xFF, gv.ID_TRANSACTION & 0xFF, 0, 0, size_of>>8, size_of&0xFF, gv.ID_SERVER, code_fct, add_first // 256, add_first % 256, nb_words //256, nb_words % 256])

        #Send Request
        gv.MODBUS_SOCKET.send(trame)

        #Response
        response=bytearray(gv.MODBUS_SOCKET.recv(gv.MAX_BUFFER))

        # Check the response for success
        if response[7] == code_fct:
            rep=list(response)[9:] #list of bytes read
            words=[]
            i=0
            while i<len(rep)-1:
                words.append((rep[i]<<8)+ (rep[i+1]&0x00FF) ) 
                i+=2
            return True,words, f"Read {nb_words} words successful"
        else:
            return False,[], f"Failed to read {nb_words} words"

    except Exception as e:
        return False,[], str(e)


def write1bit(add, val):
    """
    Function to write 1 bit
    :param add: address of the bit
    :param val: value of the bit (1 or 0)
    :return: True or False, a string message
    """
    # TODO
    try:
        #Variables
        code_fct=0x05
        
        assert val in [0, 1], "Value must be 0 or 1"
        assert 0<=add and add<=499, f"Address {add} not good"
        value={0 :0x0000 , 1:0xff00}

        #WRITE 1 COIL
        # id_tran(2) + id_proto(2)=0x0000 +size_of(2)+ id_server(1) + fct_code(1)=0x05 +@registre(2) +data(2)=[0xff00 or 0x0000]
        trame = bytearray([gv.ID_TRANSACTION>>8 & 0xFF, gv.ID_TRANSACTION & 0xFF, 0, 0, 0, 6, gv.ID_SERVER, code_fct,add//256, add%256, value[int(val)]>>8,value[int(val)] &0xFF])

        #Send request
        gv.MODBUS_SOCKET.send(trame)

        #Response
        response=bytearray(gv.MODBUS_SOCKET.recv(gv.MAX_BUFFER))

        # Check for an exception response from the server
        if response[7] & 0x80:
            return False, f"Exception response from server: Error code {response[8]}"

        # Check the response for success
        if response[7] == code_fct:
            return True, "Bit write successful"
        else:
            return False, "Failed to write bit"
    
    except Exception as e:
        return False, str(e)


def write1word(add, val):
    """
    A function to write one register
    :param add: the address of the register
    :param val: the value to write
    :return: True or False, a string message
    """
    # TODO
    try :
        #Variables
        code_fct=0x06
        
        #WRITE 1 REGISTER 
        # id_tran(2) + id_proto(2)=0x0000 +size_of(2)+ id_server(1) + fct_code(1)=0x06 +@registre(2) +word(2)
        trame = bytearray([gv.ID_TRANSACTION>>8 & 0xFF, gv.ID_TRANSACTION & 0xFF, 0, 0, 0, 6, gv.ID_SERVER, code_fct, add // 256, add % 256, val//256, val%256])

        #Send Request
        gv.MODBUS_SOCKET.send(trame)

        #Response
        response=bytearray(gv.MODBUS_SOCKET.recv(gv.MAX_BUFFER))
        
        # Check the response for success
        if response[7] == code_fct:
            return True, "Word write successful"
        else:
            return False, "Failed to write word"
    
    except Exception as e:
        return False, str(e)



def write_n_bits(nb_bits, add_first, values):
    """
    A function to write N consecutive bits
    :param nb_bits: the number of bits to write
    :param add_first: the address of the first bit to write
    :param values: a list with the values of the bits
    :return: True or False, a string message
    """
    # TODO
    try:
        import math
        #Variables
        code_fct=0x0F
        byte_count=math.ceil(nb_bits/8) #number of bytes we need for nb_bits : integer sup or egal
        size_of=7+byte_count

        #values=[x0,x1,x2,x3,x4,x5,x6,x7,x0,....,x7]
        data=[]
        i=0
        while i<len(values):
            val=0
            j=0
            shift=0
            while j<8 and i+j<len(values):
                val+=values[i+j]*2**shift
                shift+=1
                j+=1
            data.append(val)
            i+=8

        print("data", data)
        
        #WRITE N COILS (BITS)
        # id_tran(2) + id_proto(2)=0x0000 +size_of(2)+ id_server(1) + fct_code(1)=0x10 +@StartingAdresse(2) + quantity_of_Outputs(2)=N=nb_bits + byte_count(1)=N + OutputsValue(N)
        trame = bytearray([gv.ID_TRANSACTION>>8 & 0xFF, gv.ID_TRANSACTION & 0xFF, 0, 0, size_of//256, size_of%256, gv.ID_SERVER, code_fct, add_first // 256, add_first % 256, nb_bits // 256,nb_bits % 256,byte_count] +data)

        #SEND REQUEST
        gv.MODBUS_SOCKET.send(trame)

        #Response
        response=bytearray(gv.MODBUS_SOCKET.recv(gv.MAX_BUFFER))
        
        # Check the response for success
        if response[7] == code_fct:
            return True, f"Write {nb_bits} bits successful"
        else:
            return False, f"Failed to write {nb_bits} bits"
    
    except Exception as e:
        return False, str(e)


def write_n_words(nb_words, add_first, values):
    """
    A function to write N words
    :param nb_words: the number of words to write
    :param add_first: the address of the first word to write
    :param values: a list with the values of the word
    :return: True or False, a string message
    """
    # TODO
    try:
        #Variables
        code_fct=0x10
        byte_count=2*nb_words  #number of bytes of data
        size_of = 7+byte_count
        
        data=[]
        for val in values:
            data.append(val//256)
            data.append(val%256)
        
        

        #WRITE N REGISTERS(WORDS)
        # id_tran(2) + id_proto(2)=0x0000 +size_of(2)+ id_server(1) + fct_code(1)=0x10 +@firstRegister(2) + quantity_of_registers(2)=nb_words=N + byte_count(1)=2*nb_words + data(2*N)
        trame = bytearray([gv.ID_TRANSACTION>>8 & 0xFF, gv.ID_TRANSACTION & 0xFF, 0, 0, size_of//256, size_of%256, gv.ID_SERVER, code_fct, add_first // 256, add_first % 256, nb_words // 256,nb_words % 256,byte_count] +data)

        #SEND REQUEST
        gv.MODBUS_SOCKET.send(trame)

        #Response
        response=bytearray(gv.MODBUS_SOCKET.recv(gv.MAX_BUFFER))
        
        # Check the response for success
        if response[7] == code_fct:
            return True, f"Write {nb_words} words successful"
        else:
            return False, f"Failed to write {nb_words} words"
    
    except Exception as e:
        return False, str(e)
