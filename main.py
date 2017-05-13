from NatNetClient import NatNetClient
from nat_net_controller import NatNetController
import serial
from serial_data import serialData
from uwb_client import UwbClient
from threading import Thread, Event
import time
import datetime
import platform
import json
import os
import sys

if platform.system() == 'Darwin':
    serial_connection = serial.Serial('/dev/cu.SLAB_USBtoUART', '38400', timeout = 0.1, writeTimeout = 0)
elif platform.system() == 'Linux':
    serial_connection = serial.Serial('/dev/ttyAMA0', '115200', timeout = 0.1, writeTimeout = 0)
else:
    print("无法识别系统!")

data_array = []

serial_connection.flushInput()

#  serial_client = serialData()
serial_client = UwbClient()

nat_net_controller = NatNetController()
nat_net_streaming_client = NatNetClient(nat_net_controller)
nat_net_streaming_client.newFrameListener = NatNetController.receiveNewFrame
nat_net_streaming_client.rigidBodyListener = NatNetController.receiveRigidBodyFrame

json_path = os.path.join(os.getcwd(), datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S.json"))

def record_data(record_stop):
    while not record_stop.is_set():
        try:
            with open(json_path, "w+") as f:
                f.write(json.dumps({'data': data_array}))
            print("记录存档")
            time.sleep(1)
        except Exception as e:
            raise e

record_stop = Event()
record_dataThread = Thread( target = record_data, args = (record_stop,))

receive_stop = Event()
#  receive_dataThread = Thread( target = serialData.receive, args = (serial_connection, serial_client, receive_stop))
receive_dataThread = Thread( target = UwbClient.receive, args = (serial_connection, serial_client, receive_stop))

record_dataThread.start()
nat_net_streaming_client.run()
receive_dataThread.start()

def handle_data(handle_data_stop):
    i = 0
    print("开始")
    while not handle_data_stop.is_set():
        try:
            current_data = [serial_client.buffer_data, nat_net_controller.positions_buffer, nat_net_controller.rotations_buffer, datetime.datetime.now().strftime("%H:%M:%S.%f")]
            data_array.append(current_data)
            if i > 10000:
                print(current_data)
                i = 0
            i += 1
            time.sleep(0.1)
        except Exception as e:
            raise e

handle_data_stop = Event()
handle_dataThread = Thread( target = handle_data, args = (handle_data_stop,))
handle_dataThread.start()

def stop():
    record_stop.set()
    handle_data_stop.set()
    receive_stop.set()
    nat_net_streaming_client.stop()
    print("close all threads")

#  sys.exit(stop())
