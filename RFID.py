import RPi.GPIO as GPIO
import MFRC522
import signal

banner = '''

'''

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
            MIFAREReader.MFRC522_DumpClassic1K(key, uid)
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
            status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
            print("\n")
            
            if status == MIFAREReader.MI_OK:
                data = []

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

                print("Sector 0 looked like this:")
                MIFAREReader.MFRC522_Read(0)

                MIFAREReader.MFRC522_Write(0, data)
                print('Now it looks like this:')
                MIFAREReader.MFRC522_Read(0)
                MIFAREReader.MFRC522_StopCrypto1()

elif level == 3:
    pass

elif level == 4:
    reader = MFRC522.SimpleMFRC522()
    try:
        id, text = reader.read()
        print(id)
        print(text)
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
