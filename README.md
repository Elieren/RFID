# RFID_SCRIPT

#### The file 'MFRC522.py' was copied from '[MFRC522-python](https://github.com/mxgxw/MFRC522-python?ysclid=lcua5y63ss888039040)' and modified 'Elieren'

### __The program code has been rewritten from python 2 to python 3.__


# Install 
This code requires you to have SPI-Py installed from the following repository: https://github.com/lthiery/SPI-Py
```
git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py/
git checkout 8cce26b9ee6e69eb041e9d5665944b88688fca68
sudo python3 setup.py install
```
Enable SPI in raspberry pi
```
sudo nano /boot/config.txt

dtparam=spi=on
```
```
reboot
```
Install mfrc522
```
pip3 install mfrc522
```

# Pins

| Name | Pin # | Pin name   |
|:------:|:-------:|:------------:|
| SDA  | 24    | GPIO8      |
| SCK  | 23    | GPIO11     |
| MOSI | 19    | GPIO10     |
| MISO | 21    | GPIO9      |
| IRQ  | None  | None       |
| GND  | Any   | Any Ground |
| RST  | 22    | GPIO25     |
| 3.3V | 1 or 17    | 3V3        |

## Start program

```
sudo python3 RFID.py
```

## functional
1) Read card - read all sectors of the card.
2) Write UID - can overwrite the UID of the card (there is a 0 sector unlocked on the card).
3) Write sector - can overwrite the given sector with the given values.
4) Read text - reads the text written on the card.
5) Write text - Writes text to the card.