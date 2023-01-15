import RPi.GPIO as GPIO
import MFRC522
import signal

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
print('3) Write all')
print('4) Read text')
print('5) Write text')

level = int(input(': '))


def end_read(signal, frame):
    print("Ctrl+C captured, ending read.")
    GPIO.cleanup()

if level == 1:
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
            for x in text:
                print(x[0])
            MIFAREReader.MFRC522_StopCrypto1()

elif level == 2:
    signal.signal(signal.SIGINT, end_read)
    MIFAREReader = MFRC522.MFRC522()
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

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
                data_ex = []

                print('Rewrite the values of the 0 sector separated by a space')
                text = str(input(': '))
                data = text.split()

                print('Write the desired UID separated by a space')
                new_uid = str(input(': '))
                new_uid_t = new_uid.split()
                a = 0
                for x in new_uid_t:
                    data[a] = x
                    a += 1
                
                data = []

                for x in data_ex:
                    x = int(x)
                    f = ('%X' % x)
                    if len(f) == 1:
                        f = '0' + f
                    f = '0x' + f
                    data.append(f)

                print("Sector 0 looked like this:")
                MIFAREReader.MFRC522_Read(0)

                MIFAREReader.MFRC522_Write(0, data)
                print('Now it looks like this:')
                text = MIFAREReader.MFRC522_Read(0)
                print(text[0])
                MIFAREReader.MFRC522_StopCrypto1()

elif level == 3:
    signal.signal(signal.SIGINT, end_read)
    MIFAREReader = MFRC522.MFRC522()
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    if status == MIFAREReader.MI_OK:
        print("Card detected")
        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK:
            data = []
            xe = True
            sector = 0
            print('Rewrite all sectors line by line.')
            print('Write end to exit')
            print('Example:12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0')
            while xe:
                hex_text = []
                text1 = str(input(f'Sector {sector}: '))
                if text1 == 'end':
                    xe = False
                else:
                    code = text1.split(', ')
                    for x in code:
                        x = int(x)
                        f = ('%X' % x)
                        if len(f) == 1:
                            f = '0' + f
                        f = '0x' + f
                        hex_text.append(f)
                    data.append(hex_text)
                sector += 1


            print(f"Card read UID: {uid[0]}.{uid[1]}.{uid[2]}.{uid[3]}")
            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
            MIFAREReader.MFRC522_SelectTag(uid)

            #Full entry per tag
            try:
                MIFAREReader.MFRC522_WriteClassic1K(key, uid, data)
                print('Written')
            except:
                print('Error')

elif level == 4:
    reader = MFRC522.SimpleMFRC522()
    try:
        id, text = reader.read()
        print(f'id: {id}')
        print(f'text: {text}')
    except:
        print('Error')
    GPIO.cleanup()
    
elif level == 5:
    reader = MFRC522.SimpleMFRC522()
    try:
        text = input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
    except:
        print('Error')
    GPIO.cleanup()
