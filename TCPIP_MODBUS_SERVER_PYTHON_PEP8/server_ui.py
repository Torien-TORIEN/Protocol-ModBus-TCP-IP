#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tcpipserver import TCPIPServer
from memory_ui import MemoryUI

DEFAULTPORT = 5020


class ServerUI:
    def __init__(self, master, myserver):
        self.master = master
        self.modbus = myserver
        self.server = TCPIPServer(self.modbus)

        self.server.callback = self.addlog

        self.menubar = tk.Menu(self.master)
        self.menubar.add_command(label="Memory Manager", command=self.show_memory_manager)
        self.master.config(menu=self.menubar)

        master.title("Modbus TCP/IP Server")

        # frame 1
        self.frame_server = tk.LabelFrame(self.master, text="Server", borderwidth=2, relief=tk.GROOVE)
        self.frame_server.pack(side=tk.TOP, padx=30, pady=30, expand="yes", fill="both")

        self.p1 = tk.PanedWindow(self.frame_server, orient=tk.HORIZONTAL)

        self.label1 = tk.Label(self.p1, text="Port:")
        self.txb_port = tk.Entry(self.p1, width=30)
        self.txb_port.delete(0, tk.END)
        self.txb_port.insert(0, str(DEFAULTPORT))

        self.btn_okport = tk.Button(self.p1, text="OK", command=self.on_btn_okport_pressed)

        self.value_port = tk.StringVar()
        self.port = self.server.port
        self.value_port.set(str(self.port))
        self.lb_port = tk.Label(self.p1, textvariable=self.value_port, state=tk.DISABLED)

        self.p1.add(self.label1)
        self.p1.add(self.txb_port)
        self.p1.add(self.btn_okport)
        self.p1.add(self.lb_port)
        self.p1.pack(expand="yes")

        self.btn_start = tk.Button(self.frame_server, text="Start", command=self.on_btn_start_pressed)
        self.btn_start.pack(expand="yes", fill="both")
        self.btn_stop = tk.Button(self.frame_server, text="Stop", command=self.on_btn_stop_pressed)
        self.btn_stop.pack(expand="yes", fill="both")

        self.frame_logs = tk.LabelFrame(self.master, text="Logs", borderwidth=2, relief=tk.GROOVE)
        self.frame_logs.pack(side=tk.BOTTOM, padx=30, pady=30, expand="yes", fill="both")

        # liste
        self.lw_logs = tk.Listbox(self.frame_logs)
        self.lw_logs.pack(expand="yes", fill="both")

        self.btn_clean = tk.Button(self.frame_logs, text="Clean Logs", command=self.on_btn_clean_pressed)
        self.btn_clean.pack(expand="yes", fill="both")

        self.memory_manager = None
        self.memory_ui = None

    def show_memory_manager(self):
        self.memory_manager = tk.Toplevel(self.master)
        self.memory_manager.title("Memory Manager")
        self.memory_ui = MemoryUI(self.memory_manager, self.modbus.memory)
        self.memory_ui.callback = self.addlog

    def on_btn_clean_pressed(self):
        self.lw_logs.delete(0, tk.END)

    def addlog(self, msg):
        self.lw_logs.insert(self.lw_logs.size(), msg)

    def on_btn_okport_pressed(self):
        try:
            self.port = int(self.txb_port.get())
        except ValueError:
            self.addlog("ERR : <Port> should be a number!")
            return

        self.server.set_port(self.port)
        self.value_port.set(str(self.server.port))

    def on_btn_start_pressed(self):
        try:
            self.server = TCPIPServer(self.modbus)
            self.server.callback = self.addlog
            self.server.set_port(self.port)
            self.server.start_server()
        except Exception as e:
            self.addlog(str(e))

    def on_btn_stop_pressed(self):
        self.server.stop_server()
