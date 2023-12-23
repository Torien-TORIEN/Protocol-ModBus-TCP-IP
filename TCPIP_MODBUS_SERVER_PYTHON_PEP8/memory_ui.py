#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk


class MemoryUI:
    def __init__(self, master, memory):
        self.master = master
        self.memory = memory
        self.callback = None

        # BITS

        self.frame_bits = tk.LabelFrame(self.master, text="Memory State (bits)", borderwidth=2, relief=tk.GROOVE)
        self.frame_bits.pack(side=tk.TOP, padx=15, pady=15, expand="yes", fill="both")

        self.lb1 = tk.Label(self.frame_bits, text="Memory range: B" + str(self.memory.min_address_coil) +
                                                  " to B" + str(self.memory.max_address_coil))
        self.lb1.pack(expand="yes", fill="both")

        self.frame_bits_read = tk.LabelFrame(self.frame_bits, text="Read", borderwidth=2, relief=tk.GROOVE)
        self.frame_bits_read.pack(side=tk.TOP, padx=15, pady=15, expand="yes", fill="both")

        self.pb1 = tk.PanedWindow(self.frame_bits_read, orient=tk.HORIZONTAL)
        self.lb3 = tk.Label(self.pb1, text="B")
        self.txb_checkbit = tk.Entry(self.pb1, width=15)
        self.pb1.add(self.lb3)
        self.pb1.add(self.txb_checkbit)
        self.pb1.pack(expand="yes")

        self.pb2 = tk.PanedWindow(self.frame_bits_read, orient=tk.HORIZONTAL)
        self.lb4 = tk.Label(self.pb2, text="Value: ")
        self.value_bit = tk.StringVar() 
        self.value_bit.set("0")
        self.lb_bit = tk.Label(self.pb2, textvariable=self.value_bit, state=tk.DISABLED)
        self.pb2.add(self.lb4)
        self.pb2.add(self.lb_bit)
        self.pb2.pack(expand="yes")

        self.btn_readbit = tk.Button(self.frame_bits_read, text="Read", command=self.on_btn_readbit_pressed)
        self.btn_readbit.pack(expand="yes", fill="both")

        self.frame_bits_write = tk.LabelFrame(self.frame_bits, text="Write", borderwidth=2, relief=tk.GROOVE)
        self.frame_bits_write.pack(side=tk.TOP, padx=15, pady=15, expand="yes", fill="both")

        self.pb3 = tk.PanedWindow(self.frame_bits_write, orient=tk.HORIZONTAL)
        self.lb4 = tk.Label(self.pb3, text="B")
        self.txb_writebit_add = tk.Entry(self.pb3, width=15)
        self.lb5 = tk.Label(self.pb3, text=", value (0 or 1) ")
        self.txb_writebit_val = tk.Entry(self.pb3, width=15)
        self.pb3.add(self.lb4)
        self.pb3.add(self.txb_writebit_add)
        self.pb3.add(self.lb5)
        self.pb3.add(self.txb_writebit_val)
        self.pb3.pack(expand="yes")

        self.btn_writebit = tk.Button(self.frame_bits_write, text="Write", command=self.on_btn_writebit_pressed)
        self.btn_writebit.pack(expand="yes", fill="both")
        
        # ------------ WORDS ----------------------------

        self.frame_words = tk.LabelFrame(self.master, text="Memory State (words)", borderwidth=2, relief=tk.GROOVE)
        self.frame_words.pack(side=tk.TOP, padx=15, pady=15, expand="yes", fill="both")

        self.lw1 = tk.Label(self.frame_words, text="Memory range: W" + str(self.memory.min_address_reg) +
                                                   " to W" + str(self.memory.max_address_reg))
        self.lw1.pack(expand="yes", fill="both")

        self.frame_words_read = tk.LabelFrame(self.frame_words, text="Read", borderwidth=2, relief=tk.GROOVE)
        self.frame_words_read.pack(side=tk.TOP, padx=15, pady=15, expand="yes", fill="both")

        self.pw1 = tk.PanedWindow(self.frame_words_read, orient=tk.HORIZONTAL)
        self.lw1 = tk.Label(self.pw1, text="W")
        self.txb_checkword = tk.Entry(self.pw1, width=15)
        self.pw1.add(self.lw1)
        self.pw1.add(self.txb_checkword)
        self.pw1.pack(expand="yes")

        self.pw2 = tk.PanedWindow(self.frame_words_read, orient=tk.HORIZONTAL)
        self.lw2 = tk.Label(self.pw2, text="Value (10): ")
        self.value_word_10 = tk.StringVar() 
        self.value_word_10.set("0")
        self.lb_word_10 = tk.Label(self.pw2, textvariable=self.value_word_10, state=tk.DISABLED, width=15)
        self.pw2.add(self.lw2)
        self.pw2.add(self.lb_word_10)
        self.pw2.pack(expand="yes")

        self.pw3 = tk.PanedWindow(self.frame_words_read, orient=tk.HORIZONTAL)
        self.lw3 = tk.Label(self.pw3, text="Value (16): ")
        self.value_word_16 = tk.StringVar() 
        self.value_word_16.set("0x00")
        self.lb_word_16 = tk.Label(self.pw3, textvariable=self.value_word_16, state=tk.DISABLED, width=15)
        self.pw3.add(self.lw3)
        self.pw3.add(self.lb_word_16)
        self.pw3.pack(expand="yes")

        self.btn_readword = tk.Button(self.frame_words_read, text="Read", command=self.on_btn_readword_pressed)
        self.btn_readword.pack(expand="yes", fill="both")

        self.frame_words_write = tk.LabelFrame(self.frame_words, text="Write", borderwidth=2, relief=tk.GROOVE)
        self.frame_words_write.pack(side=tk.TOP, padx=15, pady=15, expand="yes", fill="both")

        self.pw4 = tk.PanedWindow(self.frame_words_write, orient=tk.HORIZONTAL)
        self.lw4 = tk.Label(self.pw4, text="W")
        self.txb_writeword_add = tk.Entry(self.pw4, width=15)
        self.lw5 = tk.Label(self.pw4, text=", value (16) ")
        self.txb_writeword_val = tk.Entry(self.pw4, width=15)
        self.pw4.add(self.lw4)
        self.pw4.add(self.txb_writeword_add)
        self.pw4.add(self.lw5)
        self.pw4.add(self.txb_writeword_val)
        self.pw4.pack(expand="yes")

        self.btn_writeword = tk.Button(self.frame_words_write, text="Write", command=self.on_btn_writeword_pressed)
        self.btn_writeword.pack(expand="yes", fill="both")

    def on_btn_readbit_pressed(self):
        try:
            intadd = int(self.txb_checkbit.get())
        except ValueError:
            self.callback("ERR: The bit address should be a number!")
            return
        retval, data = self.memory.read_discrete_outputs(intadd, 1)
        if retval is False:
            self.callback("ERR: Impossible to read the bit")
            return
        self.value_bit.set(str(data[0]))

    def on_btn_writebit_pressed(self):
        try:
            intadd = int(self.txb_writebit_add.get())
        except ValueError:
            self.callback("ERR: The bit address should be a number!")
            return
        try:
            intval = int(self.txb_writebit_val.get())
        except ValueError:
            self.callback("ERR: The bit value should be a number!")
            return
        if intval != 0 and intval != 1:
            self.callback("ERR: The bit value should be 0 or 1!")
            return

        retval = self.memory.write_single_output(intadd, intval)
        if retval is False:
            self.callback("ERR: Impossible to write the bit")
            return
        self.callback("INFO: The bit has been updated")

    def on_btn_readword_pressed(self):
        try:
            intadd = int(self.txb_checkword.get())
        except ValueError:
            self.callback("ERR: The word address should be a number!")
            return
        retval, data = self.memory.read_holding_registers(intadd, 1)
        if retval is False:
            self.callback("ERR: Impossible to read the word")
            return
        self.value_word_10.set(str(data[0]))
        self.value_word_16.set(hex(data[0]))

    def on_btn_writeword_pressed(self):
        try:
            intadd = int(self.txb_writeword_add.get())
        except ValueError:
            self.callback("ERR: The word address should be a number!")
            return
        try:
            intval = int(self.txb_writeword_val.get(), 16)
        except ValueError:
            self.callback("ERR: The word value should be a number in hexa!")
            return

        retval = self.memory.write_holding_register(intadd, intval)
        if retval is False:
            self.callback("ERR: Impossible to write the word")
            return
        self.callback("INFO: The word has been updated")
