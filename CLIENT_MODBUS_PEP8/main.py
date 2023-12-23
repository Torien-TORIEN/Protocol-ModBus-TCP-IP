import os                   # to clean the screen
import functions as fct     # to access the functions

# To handle the clear screen
CLS = ""
if os.name == 'posix':
    # if the programming is running over GNU/Linux system
    CLS = 'clear'
else:
    # otherwise it is assumed to run on windows
    CLS = 'cls'

# For the ModBus client state
state = 0  # 0:disconnected, 1:connected

# To quit the application
bye_bye = 0

while not bye_bye:
    os.system(CLS)  # we clean the display
    fct.display_menu(state)  # display the menu
    choice = input(">> What do you want to do?")  # get the user choice

    # test of the user choice
    if (choice == "C" or choice == "c") and state == 0:
        state, msg = fct.connection()
        if state == 0:
            print(msg)
            input("Press enter to go back to the menu")
    elif (choice == "D" or choice == "d") and state == 1:
        state, msg = fct.disconnection()
        if state == 1:
            print(msg)
            input("Press enter to go back to the menu")
    elif choice == "Q" or choice == "q":
        bye_bye = 1
    # FUNCTIONS 1 ET 2
    elif (choice == "1" or choice == "2") and state == 1:
        print("FUNCTION ", choice)
        ok = False
        n = 0
        while not ok:
            ok = True
            try:
                n = int(input(">> Number of bit to read:"))
            except ValueError:
                ok = False
                print(" !! This is not a number !!")
        ok = False
        add_first = 0
        while not ok:
            ok = True
            try:
                add_first = int(input(">> Address of the first bit:"))
            except ValueError:
                ok = False
                print(" !! This is not a number !!")
        ok, bits, msg = fct.read_n_bits(n, add_first)
        if not ok:
            print(msg)
            input("Press enter to go back to the menu")
        else:
            for i in range(0, len(bits)):
                print("B[" + str(i + add_first) + "]:" + str(bits[i]))
            input("Press enter to go back to the menu")
    # FUNCTIONS 2 ET 3
    elif (choice == "3" or choice == "4") and state == 1:
        print("FUNCTION ", choice)
        ok = False
        n = 0
        while not ok:
            ok = True
            try:
                n = int(input(">> Number of registers to read:"))
            except ValueError:
                ok = False
                print(" !! This is not a number !!")
        ok = False
        add_first = 0
        while not ok:
            ok = True
            try:
                add_first = int(input(">> Address of the first register:"))
            except ValueError:
                ok = False
                print(" !! This is not a number !!")
        ok, words, msg = fct.read_n_words(n, add_first)
        if not ok:
            print(msg)
            input("Press enter to go back to the menu")
        else:
            for i in range(0, len(words)):
                print("W[" + str(i + add_first) + "]:" + str(words[i]))
            input("Press enter to go back to the menu")
    # FUNCTIONS 5
    elif (choice == "5") and state == 1:
        print("FUNCTION 5")
        ok = False
        add = 0
        while not ok:
            ok = True
            try:
                add = int(input(">> Bit address :"))
            except ValueError:
                ok = False
                print(" !! This is not a number !!")
        ok = False
        val = 0
        while not ok:
            ok = True
            try:
                val = int(input(">> Bit value:"))
            except ValueError:
                ok = False
                print(" !! This is not a number !!")
            if val != 1 and val != 0:
                ok = False
                print(" !! The value should be 0 or 1 !!")
        ok, msg = fct.write1bit(add, val)
        if not ok:
            print(msg)
            input("Press enter to go back to the menu")
        else:
            print(" -- Writing done -- ")
            input("Press enter to go back to the menu")
    # FUNCTIONS 6
    elif (choice == "6") and state == 1:
        print("FUNCTION 6")
        ok = False
        add = 0
        while not ok:
            ok = True
            try:
                add = int(input(">> Register address:"))
            except ValueError:
                ok = False
                print(" !! This is not a number !!")
        ok = False
        val = 0
        while not ok:
            ok = True
            try:
                val = int(input(">> Register value:"))
            except ValueError:
                ok = False
                print(" !! This is not a number !!")
            if val > 0xFFFF:
                ok = False
                print(" !! The value is too big !!")
        ok, msg = fct.write1word(add, val)
        if not ok:
            print(msg)
            input("Press enter to go back to the menu")
        else:
            print(" -- Writing done -- ")
            input("Press enter to go back to the menu")
    # FUNCTIONS 15
    elif (choice == "15") and state == 1:
        print("FUNCTION 15")
        ok = False
        add_first = 0
        while not ok:
            ok = True
            try:
                add_first = int(input(">> Address of the first bit:"))
            except ValueError:
                ok = False
                print(" !! This is not a number !!")
        ok = False
        nb_bits = 0
        while not ok:
            ok = True
            try:
                nb_bits = int(input(">> Number of bits:"))
            except ValueError:
                ok = False
                print(" !! This is not a number !!")

        values = []
        for i in range(0, nb_bits):
            ok = False
            val = 0
            while not ok:
                ok = True
                try:
                    val = int(input(">> value of B[" + str(i + add_first) + "]:"))
                except ValueError:
                    ok = False
                    print(" !! This is not a number !!")
                if val != 1 and val != 0:
                    ok = False
                    print(" !! The value should be 0 or 1 !!")
            values.append(val)

        ok, msg = fct.write_n_bits(nb_bits, add_first, values)
        if not ok:
            print(msg)
            input("Press enter to go back to the menu")
        else:
            print(" -- Writing done -- ")
            input("Press enter to go back to the menu")
    # FUNCTIONS 16
    elif (choice == "16") and state == 1:
        print("FUNCTION 16")
        ok = False
        add_first = 0
        while not ok:
            ok = True
            try:
                add_first = int(input(">> Address of the first register:"))
            except ValueError:
                ok = False
                print(" !! This is not a number !!")
        ok = False
        nb_words = 0
        while not ok:
            ok = True
            try:
                nb_words = int(input(">> Number of registers:"))
            except ValueError:
                ok = False
                print(" !! This is not a number !!")

        values = []
        for i in range(0, nb_words):
            ok = False
            val = 0
            while not ok:
                ok = True
                try:
                    val = int(input(">> value of W[" + str(i + add_first) + "]:"))
                except ValueError:
                    ok = False
                    print(" !! This is not a number !!")
            values.append(val)

        ok, msg = fct.write_n_words(nb_words, add_first, values)
        if not ok:
            print(msg)
            input("Press enter to go back to the menu")
        else:
            print(" -- Writing done -- ")
            input("Press enter to go back to the menu")
    else:
        print("This choice is not available")
        input("Press enter to go back to the menu")

print("Good bye")
