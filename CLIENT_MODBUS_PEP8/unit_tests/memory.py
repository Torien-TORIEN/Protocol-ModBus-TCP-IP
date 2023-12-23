#!/usr/bin/env python
# -*- coding: utf-8 -*-


NBCOILS = 500  # number of discrete inputs/outputs of our memory (bits)
NBREGISTERS = 300  # number of inputs/outputs registers of our memory (16 bits words)


class Memory:
    def __init__(self, nb_input_coils=NBCOILS, nb_registers=NBREGISTERS):
        self.coils = [0]*nb_input_coils
        self.registers = [0]*nb_registers
        self.min_address_coil = 0
        self.max_address_coil = nb_input_coils-1
        self.min_address_reg = 0
        self.max_address_reg = nb_registers-1

    # Test if the address corresponds to a correct discrete memory
    # return true if the address is correct, false otherwise
    # word_t i :    the address we want to test
    def is_valid_discrete_output(self, word_t):
        if self.min_address_coil <= word_t <= self.max_address_coil:
            return True
        else:
            return False

    # Test if the address corresponds to a correct register memory
    # return true if the address is correct, false otherwise
    # word_t i :    the address we want to test
    def is_valid_holding_register(self, word_t):
        if self.min_address_reg <= word_t <= self.max_address_reg:
            return True
        else:
            return False

    # Test if the address corresponds to a correct register memory
    # return true if the address is correct, false otherwise
    # word_t i :    the address we want to test
    def is_valid_input_register(self, word_t):
        # in this test class, input and holding registers are the same
        return self.is_valid_holding_register(word_t)

    # Test if the address corresponds to a correct discrete memory
    # return true if the address is correct, false otherwise
    # word_t i :    the address we want to test
    def is_valid_discrete_input(self, word_t):
        # in this test class, discrete inputs and outputs are the same
        return self.is_valid_discrete_output(word_t)

    # This function reads consecutive discrete outputs
    # return true if the reading succeed, false otherwise
    # word_t startingAddress :  the address of the first bit we want to read
    # word_t nbData :           the number of bits we want to read
    # bit_t * data :            the array where we want to put the read bits
    def read_discrete_outputs(self, starting_address, nb_data):
        data = [0]*nb_data
        # retval = False
        try:
            retval = self.is_valid_discrete_output(starting_address) and \
                     self.is_valid_discrete_output(starting_address + nb_data - 1)
            if retval:
                for i in range(0, nb_data):
                    data[i] = self.coils[i + starting_address]
        except IndexError:
            retval = False
        return retval, data

    # This function reads consecutive discrete inputs
    # return true if the reading succeed, false otherwise
    # word_t startingAddress :  the address of the first bit we want to read
    # word_t nbData :           the number of bits we want to read
    # bit_t * data :            the array where we want to put the read bits
    def read_discrete_inputs(self, starting_address, nb_data):
        # in this test class, discrete inputs and outputs are the same
        return self.read_discrete_outputs(starting_address, nb_data)

    # This function reads consecutive holding registers
    # return true if the reading succeed, false otherwise
    # word_t startingAddress :  the address of the first register we want to read
    # word_t nbData :           the number of registers we want to read
    # word_t * data :           the array where we want to put the read registers
    def read_holding_registers(self, starting_address, nb_data):
        data = [0]*nb_data
        try:
            retval = self.is_valid_holding_register(starting_address) and \
                     self.is_valid_holding_register(starting_address + nb_data - 1)
            for i in range(0, nb_data):
                data[i] = self.registers[i + starting_address]
        except IndexError:
            retval = False
        return retval, data

    # This function reads consecutive input registers
    # return true if the reading succeed, false otherwise
    # word_t startingAddress :  the address of the first register we want to read
    # word_t nbData :           the number of registers we want to read
    # word_t * data :           the array where we want to put the read registers
    def read_input_registers(self, starting_address, nb_data):
        # in this test class, input and holding registers are the same
        return self.read_holding_registers(starting_address, nb_data)

    # This function writes one discrete output
    # return true if the writing succeed, false otherwise
    # word_t address :          the address of the bit we want to write
    # bit_t value :             the value we want to write
    def write_single_output(self, address, value):
        retval = self.is_valid_discrete_output(address)
        try:
            self.coils[address] = value
        except IndexError:
            retval = False
        return retval

    # This function writes one holding register
    # return true if the writing succeed, false otherwise
    # word_t address :          the address of the register we want to write
    # word_t value :            the value we want to write
    def write_holding_register(self, address, value):
        retval = self.is_valid_holding_register(address)
        try:
            self.registers[address] = value
        except IndexError:
            retval = False
        return retval

    # This function writes consecutive discrete outputs
    # return true if the writing succeed, false otherwise
    # word_t address :          the address of the first bit we want to write
    # word_t nbData :           the number of bits we want to write
    # bit_t* data :             the values we want to write
    def write_multiple_outputs(self, address, nb_data, data):
        retval = self.is_valid_discrete_output(address) and self.is_valid_discrete_output(address + nb_data - 1)
        try:
            for i in range(0, nb_data):
                self.coils[address+i] = data[i]
        except IndexError:
            retval = False
        return retval

    # This function writes consecutive holding registers
    # return true if the writing succeed, false otherwise
    # word_t address :          the address of the first register we want to write
    # word_t nbData :           the number of registers we want to write
    # word_t* data :            the values we want to write
    def write_multiple_registers(self, address, nb_data, data):
        retval = self.is_valid_holding_register(address) and self.is_valid_holding_register(address + nb_data - 1)
        try:
            for i in range(0, nb_data):
                self.registers[address+i] = data[i]
        except IndexError:
            retval = False
        return retval
