from NatNetClient import NatNetClient
from nat_net_controller import NatNetController
import serial
from serial_data import serialData
from threading import Thread, Event
import time
import datetime
import platform
import json
import os

if platform.system() == 'Darwin':
    serial_connection = serial.Serial('/dev/cu.SLAB_USBtoUART', '38400', timeout = 0.02, writeTimeout = 0)
elif platform.system() == 'Linux':
    serial_connection = serial.Serial('/dev/ttyAMA0', '38400', timeout = 0.02, writeTimeout = 0)
else:
    print("无法识别系统!")

data_array = []

serial_connection.flushInput()

serial_client = serialData()

nat_net_controller = NatNetController()
nat_net_streaming_client = NatNetClient(nat_net_controller)
nat_net_streaming_client.newFrameListener = NatNetController.receiveNewFrame
nat_net_streaming_client.rigidBodyListener = NatNetController.receiveRigidBodyFrame


receive_stop = Event()
receive_dataThread = Thread( target = serialData.receive, args = (serial_connection, serial_client, receive_stop))

nat_net_streaming_client.run()
receive_dataThread.start()

json_path = os.path.join(os.getcwd(), datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S.json"))

while True:
    try:
        with open(json_path, "w+") as f:
            current_data = [serial_client.buffer_data, nat_net_controller.positions_buffer, nat_net_controller.rotations_buffer, datetime.datetime.now().strftime("%H:%M:%S.%f")]
            print(current_data)
            data_array.append(current_data)
            f.write(json.dumps({'data': data_array}))
            f.close()

    except Exception as e:
        raise e

    time.sleep(0.01)

print("close all threads")
nat_net_streaming_client.stop()
