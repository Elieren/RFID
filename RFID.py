import RPi.GPIO as GPIO
import MFRC522
import signal
import time
from mfrc522 import SimpleMFRC522

banner = '''
██████╗ ███████╗██╗██████╗         ███████╗ ██████╗██████╗ ██╗██████╗ ████████╗
██╔══██╗██╔════╝██║██╔══██╗        ██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝
██████╔╝█████╗  ██║██║  ██║        ███████╗██║     ██████╔╝██║██████╔╝   ██║   
██╔══██╗██╔══╝  ██║██║  ██║        ╚════██║██║     ██╔══██╗██║██╔═══╝    ██║   
██║  ██║██║     ██║██████╔╝███████╗███████║╚██████╗██║  ██║██║██║        ██║   
╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   
                                                                               
'''

print(banner)

print('1) Read card')
print('2) Write UID')
print('3) Write sector')
print('4) Write all')
print('5) Read text')
print('6) Write text')

level = int(input(': '))


def end_read(signal, frame):
    print("Ctrl+C captured, ending read.")
    GPIO.cleanup()
    exit()

if level == 1:
    while True:
        signal.signal(signal.SIGINT, end_read)
        MIFAREReader = MFRC522.MFRC522()
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            print("Card detected")
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:
                print(f"Card read UID: {uid[0]}.{uid[1]}.{uid[2]}.{uid[3]}")
                key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
                MIFAREReader.MFRC522_SelectTag(uid)
                text = MIFAREReader.MFRC522_DumpClassic1K(key, uid)
                sector_number = 0
                for x in text:
                    print(f'Sector {sector_number} {x[0]}')
                    sector_number += 1
                MIFAREReader.MFRC522_StopCrypto1()
                GPIO.cleanup()
                break
        
        else:
            time.sleep(1)

elif level == 2:
    data_ex = []

    print('Rewrite the values of the 0 sector separated by a space')
    text = str(input(': '))
    data_ex = text.split(', ')

    print('\nWrite the desired UID separated by a space')
    print('Example:178, 126, 88, 36\n')
    new_uid = str(input(': '))
    new_uid_t = new_uid.split(', ')
    a = 0
    for x in new_uid_t:
        x = int(x)
        data_ex[a] = x
        a += 1

    data = []
    data = data_ex

    while True:
        signal.signal(signal.SIGINT, end_read)
        MIFAREReader = MFRC522.MFRC522()
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            print("Card detected")
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:
                print(f"Card read UID: {uid[0]}.{uid[1]}.{uid[2]}.{uid[3]}")
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                MIFAREReader.MFRC522_SelectTag(uid)
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 0, key, uid)
                print("\n")
                
                if status == MIFAREReader.MI_OK:

                    print("Sector 0 looked like this:")
                    text = MIFAREReader.MFRC522_Read(0)
                    print(f'Sector 0 {x[0]}')
                    print('\n')

                    MIFAREReader.MFRC522_Write(0, data)
                    print('\n')
                    print('Now it looks like this:')
                    text = MIFAREReader.MFRC522_Read(0)
                    print(f'Sector 0 {x[0]}')
                    MIFAREReader.MFRC522_StopCrypto1()
                    GPIO.cleanup()
                    break
        
        else:
            time.sleep(1)

elif level == 3:
    print()
    print('----------------------Disclaimer-----------------------')
    print('It is not recommended to change sectors 3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63, as this may lead to card failure.')
    print('-------------------------------------------------------')
    print()
    numder = int(input('Change sector values: '))
    print()
    data = []
    print('Example:12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0\n')
    print(f'Enter new values for sector {numder}')
    new_uid = str(input(': '))
    new_uid_t = new_uid.split(', ')
    for x in new_uid_t:
        x = int(x)
        data.append(x)
    
    while True:
        signal.signal(signal.SIGINT, end_read)
        MIFAREReader = MFRC522.MFRC522()
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            print("Card detected")
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:
                print(f"Card read UID: {uid[0]}.{uid[1]}.{uid[2]}.{uid[3]}")
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                MIFAREReader.MFRC522_SelectTag(uid)
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, numder, key, uid)
                print("\n")

                if status == MIFAREReader.MI_OK:

                    print(f"Sector {numder} looked like this:")
                    text = MIFAREReader.MFRC522_Read(numder)
                    print(f'Sector {numder} {x[0]}')
                    print('\n')

                    MIFAREReader.MFRC522_Write(numder, data)
                    print('\n')
                    print('Now it looks like this:')
                    text = MIFAREReader.MFRC522_Read(numder)
                    print(f'Sector {numder} {x[0]}')
                    MIFAREReader.MFRC522_StopCrypto1()
                    GPIO.cleanup()
                    break

        else:
            time.sleep(1)


elif level == 4:
    print()
    print('1) Write down the received code.')
    print('2) Copy the code from the card.')
    print()

    level = int(input(': '))

    if level == 1:
        data = []
        xe = True
        sector = 0
        print('\nRewrite all sectors line by line.')
        print('Write (end) to exit')
        print('Example:12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0\n')
        while xe:
            hex_text = []
            text1 = str(input(f'Sector {sector}: '))
            if text1 == 'end':
                xe = False
            else:
                code = text1.split(', ')
                data.append(code)
            sector += 1

        while True:
            signal.signal(signal.SIGINT, end_read)
            MIFAREReader = MFRC522.MFRC522()
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            if status == MIFAREReader.MI_OK:
                print("\nCard detected")
                (status, uid) = MIFAREReader.MFRC522_Anticoll()

                if status == MIFAREReader.MI_OK:
                    print(f"Card read UID: {uid[0]}.{uid[1]}.{uid[2]}.{uid[3]}")
                    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                    MIFAREReader.MFRC522_SelectTag(uid)

                    #Full entry per tag
                    try:
                        MIFAREReader.MFRC522_WriteClassic1K(key, uid, data)
                        print('\nWritten')
                    except:
                        print('\nError')
                    GPIO.cleanup()
                    break
            
            else:
                time.sleep(1)

    elif level == 2:
        while True:
            signal.signal(signal.SIGINT, end_read)
            MIFAREReader = MFRC522.MFRC522()
            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

            if status == MIFAREReader.MI_OK:
                print("\nCard detected")
                (status, uid) = MIFAREReader.MFRC522_Anticoll()

                if status == MIFAREReader.MI_OK:
                    print(f"Card read UID: {uid[0]}.{uid[1]}.{uid[2]}.{uid[3]}")
                    data = []
                    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                    MIFAREReader.MFRC522_SelectTag(uid)
                    data = MIFAREReader.MFRC522_DumpClassic1K(key, uid)
                    MIFAREReader.MFRC522_StopCrypto1()
                    print('The card has been recorded.')
                    print('Remove the card and press Enter.\n')
                    input('Press Enter')
                    print('\nAttach a card.')
                    
                    while True:
                        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

                        if status == MIFAREReader.MI_OK:
                            print("\nCard detected")
                            (status, uid) = MIFAREReader.MFRC522_Anticoll()

                            if status == MIFAREReader.MI_OK:
                                print(f"Card read UID: {uid[0]}.{uid[1]}.{uid[2]}.{uid[3]}")
                                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                                MIFAREReader.MFRC522_SelectTag(uid)

                                try:
                                    MIFAREReader.MFRC522_WriteClassic1K(key, uid, data)
                                    print('\nWritten')
                                except:
                                    print('\nError')
                                GPIO.cleanup()
                                exit()
                        
                        else:
                            time.sleep(1)

            
            else:
                time.sleep(1)

elif level == 5:
    reader = SimpleMFRC522()
    try:
        while True:
            id, text = reader.read()
            print(f'id: {id}')
            print(f'text: {text}')
    except:
        print('Error')
    GPIO.cleanup()
    
elif level == 6:
    reader = SimpleMFRC522()
    try:
        while True:
            text = input('New data:')
            print("Now place your tag to write")
            reader.write(text)
            print("Written")
    except:
        print('Error')
    GPIO.cleanup()
