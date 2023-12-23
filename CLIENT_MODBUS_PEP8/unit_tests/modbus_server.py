#!/usr/bin/env python
# -*- coding: utf-8 -*-

# declaration of all the considered Modbus functions
MB_FCT_READ_DSCR_OUTPUTS = 0x01
MB_FCT_READ_DSCR_INPUTS = 0x02
MB_FCT_READ_HOLDING_REG = 0x03
MB_FCT_READ_INPUT_REG = 0x04
MB_FCT_WRITE_SING_OUTPUT = 0x05
MB_FCT_WRITE_SING_REG = 0x06
MB_FCT_WRITE_MULT_COILS = 0x0F
MB_FCT_WRITE_MULT_REGS = 0x10

# declaration of all the considered Modbus exceptions
MB_EXC_ILLEGAL_FUNCTION = 0x01
MB_EXC_ILLEGAL_DATA_ADDRESS = 0x02
MB_EXC_ILLEGAL_DATA_VALUE = 0x03
MB_EXC_SLAVE_FAILURE = 0x04

# The ModbusServer class allows to deal with Modbus pdu (protocol data unit).
# This implementation is based on the Modbus_Application_Protocol_V1_1b.pdf
# document (http://www.modbus.org/docs/Modbus_Application_Protocol_V1_1b.pdf).
# It requires a memory (an implementation of the MemInterface class).
# Note that the bit_t, byte_t, word_t types are defined in the MemInterface
# interface


class ModbusServer:
    # a memory is needed in the constructor
    # MemInterface* memory : an implementation of the MemInterface interface
    # (meminterface.h)
    def __init__(self, memory):
        self.memory = memory

    # function that processes the request modbus PDU
    # byte_t* mb_pdu :          the modbus request
    # unsigned int pdu_len :    the size of the modbus request (in bytes)
    # byte_t* mb_rsp :          the modbus response (if not defined, the modbus
    #                               request is used to store the response)
    # return the number of bytes of the modbus response.
    def process_pdu(self, pdu):
        if len(pdu) == 0:
            # the modbus pdu is empty, nothing to be done
            return []
        # we test the request function code
        if pdu[0] == MB_FCT_READ_DSCR_OUTPUTS:  # 0x01
            return self.read_discrete_outputs(pdu)
        elif pdu[0] == MB_FCT_READ_DSCR_INPUTS:  # 0x02
            return self.read_discrete_inputs(pdu)
        elif pdu[0] == MB_FCT_READ_HOLDING_REG:  # 0x03
            return self.read_holding_registers(pdu)
        elif pdu[0] == MB_FCT_READ_INPUT_REG:  # 0x04
            return self.read_input_registers(pdu)
        elif pdu[0] == MB_FCT_WRITE_SING_OUTPUT:  # 0x05
            return self.write_single_output(pdu)
        elif pdu[0] == MB_FCT_WRITE_SING_REG:  # 0x06
            return self.write_single_register(pdu)
        elif pdu[0] == MB_FCT_WRITE_MULT_COILS:  # 0x0F
            return self.write_multiple_outputs(pdu)
        elif pdu[0] == MB_FCT_WRITE_MULT_REGS:  # 0x10
            return self.write_multiple_registers(pdu)
        else:
            # the function is not handled
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_FUNCTION)

    # processing of the exception response
    @staticmethod
    def mb_exception(codefunction, codeerror):
        response = [codefunction | 0x80, codeerror]
        return response

    # ----------------------------------------------------------------------
    # Note that in all the following functions:
    # byte_t* mb_pdu :          the modbus pdu request
    # unsigned int pdu_len :    the modbus pdu request lenght
    # byte_t* mb_rsp :          the modbus pdu response
    # ----------------------------------------------------------------------

    # ----------------------------FUNCTION 0x01 ----------------------------
    #  Read Coils

    def read_discrete_outputs(self, pdu):
        # request expected data:
        # 1 byte Function code
        # 2 bytes Starting Address
        # 2 bytes Quantity of Coils
        if len(pdu) < 5:
            # the length of the request is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        quantity_outputs = ((pdu[3]) << 8) + pdu[4]
        if quantity_outputs < 0x0001 or quantity_outputs > 0x07D0:
            # quantity of requested output is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        starting_add = (pdu[1] << 8) + pdu[2]
        if not (self.memory.is_valid_discrete_output(starting_add)) or \
                not (self.memory.is_valid_discrete_output(starting_add+quantity_outputs-1)):
            # the addresses of the requested outputs are not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_ADDRESS)  # 0x02
        
        # the request is a valid request, we process it
        # i.e. we get the value of all the requested bits and
        # put them in the response array
        okflag, data = self.memory.read_discrete_outputs(starting_add, quantity_outputs)
        if not okflag:
            # Something went wrong while reading the data
            return self.mb_exception(pdu[0], MB_EXC_SLAVE_FAILURE)  # 0x04
        
        byte = 0
        bit = 0

        response = [pdu[0], 0]

        # to undestand how the bits are stored in the response, check the
        # modbus application protocol
        for i in range(0, quantity_outputs):
            if bit == 0:
                # we are starting a new byte, it is needed to be initialized to 0
                response.append(0x00)
                byte += 1
            response[1+byte] |= (data[i] << bit)
            bit += 1
            if bit == 8:
                # we need to start a new byte to store the next bit data
                bit = 0
        response[1] = byte
        return response  # 1 byte function code, 1 byte Byte count, N bytes
        # Coil Status
        # *N = Quantity of Coils / 8 (+1 if Qty%8 != 0)

    # ----------------------------FUNCTION 0x02 ----------------------------
    #  Read Discrete Inputs

    def read_discrete_inputs(self, pdu):
        # request expected data:
        # 1 byte Function code
        # 2 bytes Starting Address
        # 2 bytes Quantity of Coils
        if len(pdu) < 5:
            # the length of the request is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        quantity_outputs = ((pdu[3]) << 8) + pdu[4]
        if quantity_outputs < 0x0001 or quantity_outputs > 0x07D0:
            # quantity of requested output is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        starting_add = (pdu[1] << 8) + pdu[2]
        if not (self.memory.is_valid_discrete_input(starting_add)) or \
                not (self.memory.is_valid_discrete_input(starting_add+quantity_outputs-1)):
            # the addresses of the requested outputs are not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_ADDRESS)  # 0x02
        
        # the request is a valid request, we process it
        # i.e. we get the value of all the requested bits and
        # put them in the response array
        okflag, data = self.memory.read_discrete_inputs(starting_add, quantity_outputs)
        if not okflag:
            # Something went wrong while reading the data
            return self.mb_exception(pdu[0], MB_EXC_SLAVE_FAILURE)  # 0x04
        
        byte = 0
        bit = 0

        response = [pdu[0], 0]

        # to undestand how the bits are stored in the response, check the
        # modbus application protocol
        for i in range(0, quantity_outputs):
            if bit == 0:
                # we are starting a new byte, it is needed to be initialized to 0
                response.append(0x00)
                byte += 1
            response[1+byte] |= (data[i] << bit)
            bit += 1
            if bit == 8:
                # we need to start a new byte to store the next bit data
                bit = 0
        response[1] = byte
        return response  # 1 byte function code, 1 byte Byte count, N bytes
        #  Coil Status
        # *N = Quantity of Coils / 8 (+1 if Qty%8 != 0)

    # ----------------------------FUNCTION 0x03 ----------------------------
    #  Read Holding Registers

    def read_holding_registers(self, pdu):
        # request expected data:
        # 1 byte Function code
        # 2 bytes Starting Address
        # 2 bytes Quantity of Registers
        if len(pdu) < 5:
            # the length of the request is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        quantity_registers = ((pdu[3]) << 8) + pdu[4]
        if quantity_registers < 0x0001 or quantity_registers > 0x007D:
            # quantity of requested registers is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        starting_add = ((pdu[1]) << 8) + pdu[2]
        if not(self.memory.is_valid_holding_register(starting_add)) or \
                not(self.memory.is_valid_holding_register(starting_add+quantity_registers-1)):
            # the addresses of the requested registers are not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_ADDRESS)  # 0x02

        # the request is a valid request, we process it
        # i.e. we get the value of all the requested registers and
        # put them in the response array
        
        retval, data = self.memory.read_holding_registers(starting_add, quantity_registers)
        if not retval:
            # Something went wrong while reading the data
            return self.mb_exception(pdu[0], MB_EXC_SLAVE_FAILURE)  # 0x04

        response = [pdu[0], 0]

        for i in range(0, quantity_registers):
            response.append((data[i] & 0xFF00) >> 8)
            response.append(data[i] & 0x00FF)

        response[1] = quantity_registers*2
        return response  # 1 byte function code,
        # 1 byte Byte count, N bytes Register Values
        # N = Quantity of Registers *2

    # ----------------------------FUNCTION 0x04 ----------------------------
    #  Read Input Registers

    def read_input_registers(self, pdu):
        # request expected data:
        # 1 byte Function code
        # 2 bytes Starting Address
        # 2 bytes Quantity of Registers
        if len(pdu) < 5:
            # the length of the request is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        quantity_registers = ((pdu[3]) << 8) + pdu[4]
        if quantity_registers < 0x0001 or quantity_registers > 0x007D:
            # quantity of requested registers is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        starting_add = ((pdu[1]) << 8) + pdu[2]
        if not(self.memory.is_valid_input_register(starting_add)) or \
                not(self.memory.is_valid_input_register(starting_add+quantity_registers-1)):
            # the addresses of the requested registers are not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_ADDRESS)  # 0x02

        # the request is a valid request, we process it
        # i.e. we get the value of all the requested registers and
        # put them in the response array
        
        retval, data = self.memory.read_input_registers(starting_add, quantity_registers)
        if not retval:
            # Something went wrong while reading the data
            return self.mb_exception(pdu[0], MB_EXC_SLAVE_FAILURE)  # 0x04

        response = [pdu[0], 0]

        for i in range(0, quantity_registers):
            response.append((data[i] & 0xFF00) >> 8)
            response.append(data[i] & 0x00FF)

        response[1] = quantity_registers*2
        return response  # 1 byte function code,
        # 1 byte Byte count, N bytes Register Values
        # N = Quantity of Registers *2

    # ----------------------------FUNCTION 0x05 ----------------------------
    #  Write Single Coil

    def write_single_output(self, pdu):
        # request expected data:
        # 1 byte Function code
        # 2 bytes Output Address
        # 2 bytes Output Value
        if len(pdu) < 5:
            # the length of the request is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        output_value = ((pdu[3]) << 8) + pdu[4]
        if output_value != 0x0000 and output_value != 0xFF00:
            # output value not valide
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        address = ((pdu[1]) << 8) + pdu[2]
        if not self.memory.is_valid_discrete_output(address):
            # the address of the requested output is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_ADDRESS)  # 0x02

        val = 1
        if output_value == 0x0000:
            val = 0  # convert the requested value into bit_t

        if not self.memory.write_single_output(address, val):
            # Something went wrong while writing the data
            return self.mb_exception(pdu[0], MB_EXC_SLAVE_FAILURE)  # 0x04

        # format the response (must be the same as the request)
        return pdu

    # ----------------------------FUNCTION 0x06 ----------------------------
    #  Write Single Register

    def write_single_register(self, pdu):
        # request expected data:
        # 1 byte Function code
        # 2 bytes Register Address
        # 2 bytes Register Value
        if len(pdu) < 5:
            # the length of the request is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        register_value = ((pdu[3]) << 8) + pdu[4]
        if register_value < 0x0000 or register_value > 0xFFFF:
            # register value not valide
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        address = ((pdu[1]) << 8) + pdu[2]
        if not self.memory.is_valid_holding_register(address):
            # the address of the requested register is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_ADDRESS)  # 0x02

        val = ((pdu[3]) << 8) + pdu[4]

        if not self.memory.write_holding_register(address, val):
            # Something went wrong while writing the data
            return self.mb_exception(pdu[0], MB_EXC_SLAVE_FAILURE)  # 0x04

        # format the response (must be the same as the request)
        return pdu

    # ----------------------------FUNCTION 0x0F ----------------------------
    # Write Multiple Coils

    def write_multiple_outputs(self, pdu):
        # request expected data:
        # 1 byte    :   Function code
        # 2 bytes   :   Starting Address
        # 2 bytes   :   Quantity of Outputs
        # 1 byte    :   byte count
        # N bytes   :   Outputs value
        if len(pdu) < 5:
            # the length of the request is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        quantity_outputs = ((pdu[3]) << 8) + pdu[4]
        if quantity_outputs < 0x0001 or quantity_outputs > 0x07B0:
            # quantity of requested output is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        # we computer the number of bytes needed the store the bits
        n = int(quantity_outputs / 8)
        if quantity_outputs % 8 != 0:
            n += 1
        
        # and we check if it is consistant with the pdu
        if (n != pdu[5]) or (len(pdu) < 6 + pdu[5]):
            # the count in the pdu is not valid
            # or the length of the request is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        starting_add = ((pdu[1]) << 8) + pdu[2]
        if not self.memory.is_valid_discrete_output(starting_add) or \
                not self.memory.is_valid_discrete_output(starting_add+quantity_outputs-1):
            # the addresses of the requested outputs are not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_ADDRESS)  # 0x02
        # the request is a valid request, we process it
        data = []
        bit = 0
        byte = 0
        # we format the requested values into the array data
        for i in range(0, quantity_outputs):
            data.append((pdu[6+byte] >> bit) & 0x01)
            bit += 1
            if bit == 8:
                bit = 0
                byte += 1
        # we write the values
        if not self.memory.write_multiple_outputs(starting_add, quantity_outputs, data):
            # something went wrong while reading the data
            return self.mb_exception(pdu[0], MB_EXC_SLAVE_FAILURE)  # 0x04

        # format the response (the address and the number of coils)
        return pdu[:5]

    # ----------------------------FUNCTION 0x10 ----------------------------
    #  Write Multiple registers

    def write_multiple_registers(self, pdu):
        # request expected data:
        # 1 byte    :   Function code
        # 2 bytes   :   Starting Address
        # 2 bytes   :   Quantity of Registers
        # 1 byte    :   byte count
        # N bytes   :   Registers value
        if len(pdu) < 7:
            # the length of the request is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03
        quantity_registers = ((pdu[3]) << 8) + pdu[4]
        if quantity_registers < 0x0001 or quantity_registers > 0x007B:
            # quantity of requested registers is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        n = quantity_registers * 2
        if n != pdu[5] or len(pdu) < (6+pdu[5]):
            # the count in the pdu is not valid
            # or the length of the request is not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_VALUE)  # 0x03

        starting_add = (pdu[1] << 8) + pdu[2]
        if not self.memory.is_valid_holding_register(starting_add) or \
                not self.memory.is_valid_holding_register(starting_add+quantity_registers-1):
            # the addresses of the requested outputs are not valid
            return self.mb_exception(pdu[0], MB_EXC_ILLEGAL_DATA_ADDRESS)  # 0x02

        # the request is a valid request, we process it
        # we format the requested values into the array data
        data = []
        for i in range(0, quantity_registers):
            data.append(((pdu[6 + i*2]) << 8) + pdu[6 + i*2 + 1])
        # we write the values
        
        if not self.memory.write_multiple_registers(starting_add, quantity_registers, data):
            # Something went wrong while reading the data
            return self.mb_exception(pdu[0], MB_EXC_SLAVE_FAILURE)  # 0x04
        # format the response (the address and the number of registers)
        return pdu[:5]
