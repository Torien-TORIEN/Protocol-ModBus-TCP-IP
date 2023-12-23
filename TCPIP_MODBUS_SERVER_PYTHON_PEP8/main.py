#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tkinter as tk
from server_ui import ServerUI
from memory import Memory
from modbus_server import ModbusServer

memory = Memory()
modbus_server = ModbusServer(memory)

root = tk.Tk()
ui = ServerUI(root, modbus_server)

root.mainloop()
