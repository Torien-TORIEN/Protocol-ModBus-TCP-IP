#!/bin/python3

import unittest

from unit_tests.memory import Memory
from unit_tests.modbus_server import ModbusServer
from unit_tests.tcpipserver import TCPIPServer

import socket as socket
import global_variables as gv
import sys as sys

if len(sys.argv) == 2:
    import pathlib
    import importlib
    import fnmatch
    import os
    
    pattern = sys.argv[1]
    path = pathlib.Path("./STUDENT_FILES/").absolute()
    result = []
    for root, dirs, files in os.walk(path):
        if os.path.basename(root) != "__pycache__":
            for name in files:
                if fnmatch.fnmatch(name, f"*{pattern}*"):
                    result.append(name[:-3])
    if len(result) == 0:
        print("No student file match the pattern")
        exit()
    elif len(result) > 1:
        print("Too many files match the pattern")
        for r in result:
            print(r)
        exit()
    fct = importlib.import_module(f"STUDENT_FILES.{result[0]}")
    print(f"STUDENT : {result[0]}")
else:
    import functions as fct

try:
    from colorama import Fore, Style
    def message_ok(msg):
        print(Fore.GREEN + "\t[OK] " + msg + Style.RESET_ALL)


    def message_error(msg):
        print(Fore.RED + "\t[X ] " + msg + Style.RESET_ALL)


    def message_warning(msg):
        print(Fore.YELLOW + "\t[! ] " + msg + Style.RESET_ALL)

except ModuleNotFoundError:
    print("Colorama is not installed, you won't have the colors...")
    def message_ok(msg):
        print("\t[OK] " + msg)


    def message_error(msg):
        print("\t[X ] " + msg)


    def message_warning(msg):
        print("\t[! ] " + msg)


class TestFunctions(unittest.TestCase):

    nb_words = 400
    nb_bits = 500
    port = 5555
    W1B = 0
    WNB = 1
    W1W = 2
    WNW = 3
    RNB = 4
    RNW = 5
    notes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    serverTCPIP = None

    @classmethod
    def tearDownClass(cls):

        total = 0
        for i, val in enumerate(cls.notes):
            cls.notes[i] = max(val, 0)
            total += cls.notes[i]

        print("*********** NOTES *************")
        print(f"[{cls.notes[cls.RNB]}] Read N bits")
        print(f"[{cls.notes[cls.RNW]}] Read N words")
        print(f"[{cls.notes[cls.W1B]}] Write 1 bit")
        print(f"[{cls.notes[cls.W1W]}] Write 1 word")
        print(f"[{cls.notes[cls.WNB]}] Write N bits")
        print(f"[{cls.notes[cls.WNW]}] Write N words")
        print("-------------------------------")
        print(f"[{total}] Total")

        gv.MODBUS_SOCKET.close()
        cls.serverTCPIP.stop_server()

    @classmethod
    def tearDown(cls):
        gv.MODBUS_SOCKET.close()

    @classmethod
    def setUpClass(cls):

        try:
            cls.memory = Memory(nb_input_coils=cls.nb_bits, nb_registers=cls.nb_words)
            cls.server = ModbusServer(cls.memory)
            cls.serverTCPIP = TCPIPServer(cls.server)
            cls.serverTCPIP.set_port(cls.port)
            cls.serverTCPIP.callback = TestFunctions.server_callback
            cls.serverTCPIP.start_server()

            gv.MODBUS_SOCKET = socket.socket()
            gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), cls.port))
            gv.MODBUS_SOCKET.settimeout(1)
            # print("[CLIENT] connected")
            # print("... All done, ready to test!")
        except Exception as e:
            print(f"[ERROR] {e}")
            quit(0)

    @staticmethod
    def empty_buffer():
        try:
            gv.MODBUS_SOCKET.recv(gv.MAX_BUFFER)
            return True
        except socket.error:
            return False

    @staticmethod
    def server_callback(msg):
        pass
        # print(f"\t\t\t[SERVER] : {msg}")

    def setUp(self):
        self.memory.max_address_coil = self.nb_bits - 1
        self.memory.max_address_reg = self.nb_words - 1
        TestFunctions.empty_buffer()

    def test_write_1_bit_true(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Write 1 bit to True"
        note_id = self.W1B

        flag_error = False

        test = True
        add_test = 3

        self.memory.coils[add_test] = not test
        try:
            ok, *_ = fct.write1bit(add_test, test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            if self.memory.coils[add_test] != test:
                message_error(f"{function_name} : Error setting {test}")
                flag_error = True

            if not ok:
                message_warning(f"{function_name} : Wrong answer!")

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
            self.notes[note_id] += 0.5

    def test_write_1_bit_false(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Write 1 bit to False"
        note_id = self.W1B

        flag_error = False

        test = False
        add_test = 170

        self.memory.coils[add_test] = not test
        try:
            ok, *_ = fct.write1bit(add_test, test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            if self.memory.coils[add_test] != test:
                message_error(f"{function_name} : Error setting {test}")
                flag_error = True

            if not ok:
                message_warning(f"{function_name} : Wrong answer!")

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
            self.notes[note_id] += 0.5

    def test_write_1_bit_error(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Write 1 bit Error"
        note_id = self.W1B

        self.memory.max_address_coil = 2
        test = False
        add_test = self.memory.max_address_coil + 1

        flag_error = False

        try:
            ok, msg = fct.write1bit(add_test, test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            if ok:
                message_error(f"{function_name} : Error not processed!")
                flag_error = True

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
        else:
            message_error(f"{function_name}")
            self.notes[note_id] -= 0.25

    def test_write_1_word_1(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Write 1 word 1"
        note_id = self.W1W

        flag_error = False

        test = 0x12
        add_test = 9

        self.memory.registers[add_test] = 0
        try:
            ok, *_ = fct.write1word(add_test, test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            if self.memory.registers[add_test] != test:
                message_error(f"{function_name} : Error setting {test}")
                flag_error = True

            if not ok:
                message_warning(f"{function_name} : Wrong answer!")

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
            self.notes[note_id] += 0.5

    def test_write_1_word_2(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Write 1 word 2"
        note_id = self.W1W

        flag_error = False

        test = 0x8012
        add_test = 312

        self.memory.registers[add_test] = 0
        try:
            ok, *_ = fct.write1word(add_test, test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            if self.memory.registers[add_test] != test:
                message_error(f"{function_name} : Error setting {test}")
                flag_error = True

            if not ok:
                message_warning(f"{function_name} : Wrong answer!")

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
            self.notes[note_id] += 0.5

    def test_write_1_word_error(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        note_id = self.W1W
        function_name = "Write 1 word Error"

        flag_error = False

        self.memory.max_address_reg = 2
        test = 0x0
        add_test = self.memory.max_address_reg + 1

        try:
            ok, msg = fct.write1word(add_test, test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            if ok:
                message_error(f"{function_name} : Error not processed!")
                flag_error = True

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
        else:
            self.notes[note_id] -= 0.25

    def test_write_n_bits_1(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Write N bits 1"
        note_id = self.WNB

        flag_error = False
        test = [0, 1, 0, 0, 1, 1, 0]
        add_test = 18

        for i, _ in enumerate(test):
            self.memory.coils[add_test + i] = 0

        try:
            ok, *_ = fct.write_n_bits(len(test), add_test, test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            for i, t in enumerate(test):
                if t != self.memory.coils[add_test + i]:
                    message_error(f"{function_name} : Error setting {test}")
                    flag_error = True
                    break

            if not ok:
                message_warning(f"{function_name} : Wrong answer!")

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
            self.notes[note_id] += 0.5

    def test_write_n_bits_2(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Write N bits 2"
        note_id = self.WNB

        flag_error = False
        test = [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0,
                0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0]
        add_test = 300

        for i, _ in enumerate(test):
            self.memory.coils[add_test + i] = 0

        try:
            ok, *_ = fct.write_n_bits(len(test), add_test, test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            for i, t in enumerate(test):
                if t != self.memory.coils[add_test + i]:
                    message_error(f"{function_name} : Error setting {test}")
                    flag_error = True
                    break

            if not ok:
                message_warning(f"{function_name} : Wrong answer!")

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
            self.notes[note_id] += 0.5

    def test_write_n_bits_error(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Write N bits Error"
        note_id = self.WNB

        flag_error = False
        test = [0, 1, 0]

        self.memory.max_address_coil = 2
        add_test = self.memory.max_address_coil + 1

        try:
            ok, _ = fct.write_n_bits(len(test), add_test, test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            if ok:
                message_error(f"{function_name} : Error not processed !")
                flag_error = True

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True
        except ZeroDivisionError as zde:
            message_error(f"{function_name}: " + str(zde))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
        else:
            self.notes[note_id] -= 0.25

    def test_write_n_words_1(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Write N words 1"
        note_id = self.WNW

        flag_error = False
        test = [0x12, 0x12, 125, 3, 12, 0x12, 0x75]
        add_test = 2

        for i, _ in enumerate(test):
            self.memory.registers[add_test + i] = 0

        try:
            ok, *_ = fct.write_n_words(len(test), add_test, test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            for i, t in enumerate(test):
                if t != self.memory.registers[add_test + i]:
                    message_error(f"{function_name} : Error setting {test}")
                    flag_error = True
                    break

            if not ok:
                message_warning(f"{function_name} : Wrong answer!")

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
            self.notes[note_id] += 0.5

    def test_write_n_words_2(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Write N words 2"
        note_id = self.WNW

        flag_error = False
        test = [0x1208, 0xFF12, 2048, 0b1101010, 12, 0x12, 0x75, 0x1208, 0xFF12, 2048, 3, 12, 0x8812, 0x9875]
        add_test = 308

        for i, _ in enumerate(test):
            self.memory.registers[add_test + i] = 0

        try:
            ok, *_ = fct.write_n_words(len(test), add_test, test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            for i, t in enumerate(test):
                if t != self.memory.registers[add_test + i]:
                    message_error(f"{function_name} : Error setting {test}")
                    flag_error = True
                    break

            if not ok:
                message_warning(f"{function_name} : Wrong answer!")

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
            self.notes[note_id] += 0.5

    def test_write_n_words_error(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Write N words Error"
        note_id = self.WNW

        flag_error = False
        test = [12, 3, 12]

        self.memory.max_address_reg = 2
        add_test = self.memory.max_address_reg + 1

        try:
            ok, _ = fct.write_n_words(len(test), add_test, test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            if ok:
                message_error(f"{function_name} : Error not processed !")
                flag_error = True

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
        else:
            self.notes[note_id] -= 0.25

    def test_read_n_bits_1(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Read N bits 1"
        note_id = self.RNB

        flag_error = False
        test = [0, 1, 0, 0, 1, 1, 0]
        add_test = 1

        for i, t in enumerate(test):
            self.memory.coils[add_test + i] = t

        try:
            ok, bits, *_ = fct.read_n_bits(len(test), add_test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            for i, b in enumerate(bits):
                if b != test[i]:
                    message_error(f"{function_name} : Error reading {test} != {bits}")
                    flag_error = True
                    break

            if len(bits) != len(test):
                message_error(f"{function_name} : Error reading {test} (len)")
                flag_error = True

            if not ok:
                message_warning(f"{function_name} : wrong response...")

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
            self.notes[note_id] += 0.5

    def test_read_n_bits_2(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Read N bits 2"
        note_id = self.RNB

        flag_error = False
        test = [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0,
                0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0]
        add_test = 266

        for i, t in enumerate(test):
            self.memory.coils[add_test + i] = t

        try:
            ok, bits, *_ = fct.read_n_bits(len(test), add_test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            for i, b in enumerate(bits):
                if b != test[i]:
                    message_error(f"{function_name} : Error reading {test} != {bits}")
                    flag_error = True
                    break

            if len(bits) != len(test):
                message_error(f"{function_name} : Error reading {test} (len)")
                flag_error = True

            if not ok:
                message_warning(f"{function_name} : wrong response...")

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
            self.notes[note_id] += 0.5

    def test_read_n_bits_error(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Read N bits Error"
        note_id = self.RNB

        flag_error = False
        self.memory.max_address_coil = 2
        add_test = self.memory.max_address_coil + 1
        test = [0, 1, 0, 0, 1, 1, 0]

        try:
            ok, bits, *_ = fct.read_n_bits(len(test), add_test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            if ok:
                message_error(f"{function_name} : Error not processed !")
                flag_error = True

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
        else:
            self.notes[note_id] -= 0.25

    def test_read_n_words_1(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Read N words 1"
        note_id = self.RNW

        flag_error = False
        test = [0x12, 0b010101, 125, 3, 12, 0x12, 0x75]
        add_test = 7

        for i, t in enumerate(test):
            self.memory.registers[add_test + i] = t

        try:
            ok, words, *_ = fct.read_n_words(len(test), add_test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            for i, w in enumerate(words):
                if w != test[i]:
                    message_error(f"{function_name} : Error reading {test} != {words}")
                    flag_error = True
                    break

            if len(words) != len(test):
                message_error(f"{function_name} : Error reading {test} (len)")
                flag_error = True

            if not ok:
                message_warning(f"{function_name} : wrong response...")

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
            self.notes[note_id] += 0.5

    def test_read_n_words_2(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Read N words 2"
        note_id = self.RNW

        flag_error = False
        test = [0x1208, 0xFF12, 2048, 0b1101010, 12, 0x12, 0x75, 0x1208, 0xFF12, 2048, 3, 12, 0x8812, 0x9875]
        add_test = 198

        for i, t in enumerate(test):
            self.memory.registers[add_test + i] = t

        try:
            ok, words, *_ = fct.read_n_words(len(test), add_test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            for i, w in enumerate(words):
                if w != test[i]:
                    message_error(f"{function_name} : Error reading {test} != {words}")
                    flag_error = True
                    break

            if len(words) != len(test):
                message_error(f"{function_name} : Error reading {test} (len)")
                flag_error = True

            if not ok:
                message_warning(f"{function_name} : wrong response...")

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
            self.notes[note_id] += 0.5

    def test_read_n_words_error(self):
        gv.MODBUS_SOCKET.close()
        gv.MODBUS_SOCKET = socket.socket()
        gv.MODBUS_SOCKET.connect((socket.gethostbyname(socket.gethostname()), self.port))
        gv.MODBUS_SOCKET.settimeout(1)

        function_name = "Read N words Error"
        note_id = self.RNW

        flag_error = False
        self.memory.max_address_reg = 2
        test = [0x12, 0b010101, 125, 3, 12, 0x12, 0x75]
        add_test = self.memory.max_address_reg

        try:
            ok, words, *_ = fct.read_n_words(len(test), add_test)
            if TestFunctions.empty_buffer():
                message_warning(f"{function_name} : response not read...")

            if ok:
                message_error(f"{function_name} : Error not processed!")
                flag_error = True

        except NameError as ne:
            message_error(f"{function_name}: " + str(ne))
            flag_error = True
        except IndexError as ie:
            message_error(f"{function_name}: " + str(ie))
            flag_error = True
        except TypeError as te:
            message_error(f"{function_name}: " + str(te))
            flag_error = True
        except ValueError as ve:
            message_error(f"{function_name}: " + str(ve))
            flag_error = True
        except AttributeError as ae:
            message_error(f"{function_name}: " + str(ae))
            flag_error = True
        except socket.error as se:
            message_error(f"{function_name}: " + str(se))
            flag_error = True

        if not flag_error:
            message_ok(f"{function_name}")
        else:
            self.notes[note_id] -= 0.25


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'])

