#!/usr/bin/python
# coding=utf-8

from __future__ import print_function
import serial, struct, sys, time, os
from pysqlite2 import dbapi2 as sqlite
import subprocess

os.system("/usr/bin/rdate 193.204.114.233")      # eseguo il sync della data/ora con il server NTP
# os.system("./mk_ramdisk.sh")                    # creo la ram disk x il DB sqlite.

ser = serial.Serial()
ser.port = sys.argv[1]
ser.baudrate = 9600

ser.open()
ser.flushInput()

byte, data = 0, ""

def dump_data(d):
    print(' '.join(x.encode('hex') for x in d))

def process_frame(d):
    # dump_data(d)
    r = struct.unpack('<HHxxBBB', d[2:])
    pm25 = r[0]/10.0
    pm10 = r[1]/10.0
    checksum = sum(ord(v) for v in d[2:8])%256
    print("PM 2.5: {} ug/m^3  PM 10: {} ug/m^3 CRC={}".format(pm25, pm10, "OK" if (checksum==r[2] and r[3]==0xab) else "NOK"))
	# Leggo i valori dal sensore di pressione
    proc = subprocess.Popen(['./BME280_tst'],stdout=subprocess.PIPE)
    BMEout = proc.stdout.readline().rstrip().split(',')
    print( BMEout)
    # Mi collego al DB
    connection = sqlite.connect('/media/data/SDS011Data.sqlite')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS samples (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                                                        date TEXT, \
                                                        time TEXT, \
                                                        temp REAL, \
                                                        press REAL, \
                                                        umid REAL, \
                                                        pm25 REAL, \
                                                        pm10 REAL)')
    cursor.execute('INSERT INTO samples VALUES (null, date("now","localtime"),\
                                                      time("now","localtime"),\
                                                      ' + "%f" % float(BMEout[0]) + ',\
                                                      ' + "%f" % float(BMEout[1]) + ',\
                                                      ' + "%f" % float(BMEout[2]) + ',\
                                                      ' + "%f" % pm25 + ',\
                                                      ' + "%f" % pm10 + ')')
    connection.commit()
                                                        

# 0xAA, 0xB4, 0x06, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x06, 0xAB
def sensor_wake():
    bytes = ['\xaa', #head
    '\xb4', #command 1
    '\x06', #data byte 1
    '\x01', #data byte 2 (set mode)
    '\x01', #data byte 3 (sleep)
    '\x00', #data byte 4
    '\x00', #data byte 5
    '\x00', #data byte 6
    '\x00', #data byte 7
    '\x00', #data byte 8
    '\x00', #data byte 9
    '\x00', #data byte 10
    '\x00', #data byte 11
    '\x00', #data byte 12
    '\x00', #data byte 13
    '\xff', #data byte 14 (device id byte 1)
    '\xff', #data byte 15 (device id byte 2)
    '\x05', #checksum
    '\xab'] #tail

    for b in bytes:
        ser.write(b)

# xAA, 0xB4, 0x06, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x05, 0xAB
def sensor_sleep():
    bytes = ['\xaa', #head
    '\xb4', #command 1
    '\x06', #data byte 1
    '\x01', #data byte 2 (set mode)
    '\x00', #data byte 3 (sleep)
    '\x00', #data byte 4
    '\x00', #data byte 5
    '\x00', #data byte 6
    '\x00', #data byte 7
    '\x00', #data byte 8
    '\x00', #data byte 9
    '\x00', #data byte 10
    '\x00', #data byte 11
    '\x00', #data byte 12
    '\x00', #data byte 13
    '\xff', #data byte 14 (device id byte 1)
    '\xff', #data byte 15 (device id byte 2)
    '\x05', #checksum
    '\xab'] #tail

    for b in bytes:
        ser.write(b)

sensor_sleep()
time.sleep(30)

while True:
    sensor_wake()
    time.sleep(40)
    
    while byte != "\xaa":
        byte = ser.read(size=1)
    d = ser.read(size=10)
    if d[0] == "\xc0":
        process_frame(byte + d)
    
    sensor_sleep()
    time.sleep(5*60)


