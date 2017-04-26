import re
class serialData(object):

    def __init__(self):
        self.data = []
        self.buffer_data = []
        self.index = 0
        self.buffer = ''

    @staticmethod
    def receive(serial_connection, serial_data, stop_event):
        while (not stop_event.is_set()):
            if serial_connection.isOpen():
                try:
                    serial_data.handle_bytes(serial_connection.read())
                except Exception as e:
                    raise e

    def handle_bytes(self, byte):
        try:
            data = byte.decode()
            if re.match('\d|\.|\,|-', data):
                self.buffer += data
            elif re.match('\n|\r', data):
                if len(self.buffer):
                    current_data = self.buffer.split(",")
                    self.buffer_data = current_data
                    self.data.append(current_data)
                    self.index += 1
                    self.buffer = ''
            else:
                self.buffer = ''
        except Exception as e:
            print(byte)
            self.buffer = ''
