import datetime
from angle_convert import AngleConvert
import time

class NatNetController(object):
    frequency = 1000000 * 0.1

    def __init__(self):
        self.positions_buffer = {}
        self.rotations_buffer = {}
        self.command_buffer = []
        self.data = {}

        self.last_send_data_time = datetime.datetime.now()

        self.begin_time = datetime.datetime.now()

        self.last_update_buffer_id = 1

    @staticmethod
    def store_data(controller, store_data_stop):
        while not store_data_stop.is_set():
            if controller.send:
                print("store data")
                for id in controller.positions_buffer.keys():
                    if id in controller.data.keys():
                        controller.data[id].append([*controller.positions_buffer[id], *controller.rotations_buffer[id]]) 
                    else:
                        controller.data[id] = []
                time.sleep(0.01)

    @staticmethod
    def receiveNewFrame( frameNumber, markerSetCount, unlabeledMarkersCount, rigidBodyCount, skeletonCount,
                        labeledMarkerCount, latency, timecode, timecodeSub, timestamp, isRecording, trackedModelsChanged ):
        #  print( "Received frame", frameNumber )
        pass

    @staticmethod
    def receiveRigidBodyFrame( controller, id, position, rotation ):
        print( "Received frame for rigid body", id )
        #print( "position: ", position )
        #print( "rotation: ", rotation )
        current_position = position
        current_rotation = AngleConvert.quaternion_to_euler(rotation)
        controller.positions_buffer[id] = current_position
        controller.rotations_buffer[id] = current_rotation
        controller.last_update_buffer_id = id
