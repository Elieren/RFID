import RPi.GPIO as GPIO
import MFRC522
import signal
import time
from mfrc522 import SimpleMFRC522
from colorama import Fore, Style

banner = '''
██████╗ ███████╗██╗██████╗         ███████╗ ██████╗██████╗ ██╗██████╗ ████████╗
██╔══██╗██╔════╝██║██╔══██╗        ██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝
██████╔╝█████╗  ██║██║  ██║        ███████╗██║     ██████╔╝██║██████╔╝   ██║   
██╔══██╗██╔══╝  ██║██║  ██║        ╚════██║██║     ██╔══██╗██║██╔═══╝    ██║   
██║  ██║██║     ██║██████╔╝███████╗███████║╚██████╗██║  ██║██║██║        ██║   
╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   
                                                                               
'''

print(Fore.GREEN + banner)

print('[1] Read card')
print('[2] Write UID')
print('[3] Write sector')
print('[4] Clear card')
print('[5] Read text')
print('[6] Write text' + Style.RESET_ALL)

level = int(input(Fore.YELLOW + '\n: ' + Style.RESET_ALL))
print('\n')


def end_read(signal, frame):
    print("Ctrl+C captured, ending read.")
    GPIO.cleanup()
    exit()

if level == 1:
    print(Fore.YELLOW + 'Attach a card\n')
    sector_nom = []
    while True:
        signal.signal(signal.SIGINT, end_read)
        MIFAREReader = MFRC522.MFRC522()
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            print(Fore.GREEN + "Card detected\n" + Style.RESET_ALL)
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:
                print(Fore.YELLOW + f"Card read UID: {uid[0]}.{uid[1]}.{uid[2]}.{uid[3]}" + Style.RESET_ALL)
                key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                MIFAREReader.MFRC522_SelectTag(uid)
                text = MIFAREReader.MFRC522_DumpClassic1K(key, uid)
                sector_number = 0
                for x in text:
                    print(f'Sector {sector_number} {x[0]}')
                    sector_nom.append(x[0])
                    sector_number += 1
                MIFAREReader.MFRC522_StopCrypto1()
                GPIO.cleanup()
                break
        
        else:
            time.sleep(1)
    print()
    otv = str(input((Fore.YELLOW + 'Save in file (Y/n): ')))

    if otv.lower() == 'y':
        name = str(input('Name file: ' + Style.RESET_ALL))
        f = open(f'{name}.txt', 'w')
        for x in sector_nom:
            f.write(x + '\n')
        f.close()

    else:
        pass


elif level == 2:
    print('\nWrite the desired UID separated by commas')
    print('Example:178, 126, 88, 36\n')
    new_uid = str(input(': '))
    print(Fore.YELLOW + 'Attach a card\n' + Style.RESET_ALL)
    while True:
        signal.signal(signal.SIGINT, end_read)
        MIFAREReader = MFRC522.MFRC522()
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            print(Fore.GREEN + "Card detected\n" + Style.RESET_ALL)
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:
                print(Fore.YELLOW + f"Card read UID: {uid[0]}.{uid[1]}.{uid[2]}.{uid[3]}" + Style.RESET_ALL)
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                MIFAREReader.MFRC522_SelectTag(uid)
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 0, key, uid)
                print("\n")
                
                if status == MIFAREReader.MI_OK:
                    #--------------------------#
                    data_ex = []

                    text = MIFAREReader.MFRC522_Read(0)
                    data_ex = text[0].split(', ')
                    data_ex[-1] = data_ex[-1][:-1]

                    new_uid_t = new_uid.split(', ')
                    a = 0
                    for x in new_uid_t:
                        x = int(x)
                        data_ex[a] = x
                        a += 1

                    data = []
                    data = data_ex

                    a = 0
                    for x in data:
                        data[a] = int(x)
                        a += 1

                    #--------------------------#
                    print(Fore.YELLOW + "Sector 0 looked like this:")
                    text = MIFAREReader.MFRC522_Read(0)
                    print(f'Sector 0 {text[0]}')
                    print('\n')

                    MIFAREReader.MFRC522_Write(0, data)
                    print('\n')
                    print('Now it looks like this:')
                    text = MIFAREReader.MFRC522_Read(0)
                    print(f'Sector 0 {text[0]}' + Style.RESET_ALL)
                    MIFAREReader.MFRC522_StopCrypto1()
                    GPIO.cleanup()
                    break
        
        else:
            time.sleep(1)

elif level == 3:
    print()
    print(Fore.RED + '----------------------Disclaimer-----------------------')
    print('It is not recommended to change sectors 3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63, as this may lead to card failure.')
    print('-------------------------------------------------------' + Style.RESET_ALL)
    print()
    numder = int(input(Fore.YELLOW + 'Change sector values: '))
    not_num = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]
    if numder in not_num:
        print(Fore.RED + '\nYou have chosen an unsafe sector')
        print('Are you sure you want to continue?\n' + Style.RESET_ALL)
        status = str(input(Fore.YELLOW + 'Save in file (Y/n): '+ Style.RESET_ALL))
        if status.lower() == 'y':
            pass
        else:
            exit()
    print()
    data = []
    print('\nExample:12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0\n')
    print(f'Enter new values for sector {numder}')
    new_uid = str(input(': '))
    new_uid_t = new_uid.split(', ')
    for x in new_uid_t:
        x = int(x)
        data.append(x)
    
    print(Fore.YELLOW + '\nAttach a card\n' + Style.RESET_ALL)

    while True:
        signal.signal(signal.SIGINT, end_read)
        MIFAREReader = MFRC522.MFRC522()
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            print(Fore.GREEN + "Card detected\n" + Style.RESET_ALL)
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:
                print(Fore.YELLOW + f"Card read UID: {uid[0]}.{uid[1]}.{uid[2]}.{uid[3]}" + Style.RESET_ALL)
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                MIFAREReader.MFRC522_SelectTag(uid)
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, numder, key, uid)
                print("\n")

                if status == MIFAREReader.MI_OK:

                    print(Fore.YELLOW + f"Sector {numder} looked like this:" + Style.RESET_ALL)
                    text = MIFAREReader.MFRC522_Read(numder)
                    print(f'Sector {numder} {text[0]}')
                    print('\n')

                    MIFAREReader.MFRC522_Write(numder, data)
                    print('\n')
                    print(Fore.YELLOW + 'Now it looks like this:' + Style.RESET_ALL)
                    text = MIFAREReader.MFRC522_Read(numder)
                    print(f'Sector {numder} {text[0]}' + Style.RESET_ALL)
                    MIFAREReader.MFRC522_StopCrypto1()
                    GPIO.cleanup()
                    break

        else:
            time.sleep(1)

elif level == 4:
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    print(Fore.YELLOW + '\nAttach a card\n' + Style.RESET_ALL)

    while True:
        signal.signal(signal.SIGINT, end_read)
        MIFAREReader = MFRC522.MFRC522()
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            print(Fore.GREEN + "Card detected\n" + Style.RESET_ALL)
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:
                print(Fore.YELLOW + f"Card read UID: {uid[0]}.{uid[1]}.{uid[2]}.{uid[3]}" + Style.RESET_ALL)
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                MIFAREReader.MFRC522_SelectTag(uid)
                print("\n")
                    
                lev = 0
                not_num = [0, 3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63]
                
                while lev <= 63:
                    if lev not in not_num:
                        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, lev, key, uid)
                        if status == MIFAREReader.MI_OK:
                            MIFAREReader.MFRC522_Write(lev, data)
                            text = MIFAREReader.MFRC522_Read(lev)
                            print(f'Sector {lev} {text[0]}' + Style.RESET_ALL)
                        else:
                            print("Authentication error")
                    lev += 1
                    time.sleep(0.1)
                
                MIFAREReader.MFRC522_StopCrypto1()
                GPIO.cleanup()
                break

        else:
            time.sleep(1)

elif level == 5:
    reader = SimpleMFRC522()
    try:
        print(Fore.YELLOW + 'Attach a card\n' + Style.RESET_ALL)
        while True:
            id, text = reader.read()
            print(f'id: {id}')
            print(f'text: {text}')
    except:
        print(Fore.RED + 'Error' + Style.RESET_ALL)
    GPIO.cleanup()
    
elif level == 6:
    reader = SimpleMFRC522()
    try:
        while True:
            text = input('New data:')
            print("Now place your tag to write")
            reader.write(text)
            print(Fore.GREEN + "Written" + Style.RESET_ALL)
    except:
        print(Fore.RED + 'Error' + Style.RESET_ALL)
    GPIO.cleanup()
