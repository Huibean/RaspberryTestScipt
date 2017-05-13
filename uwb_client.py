import codecs
def take_opposite(binary):
    new_binary = ''
    for b in binary:
        if b == '1':
            new_binary += '0'
        else:
            new_binary += '1'
    return new_binary

def handle_hex(hex_str):
    original_int = int(hex_str, base=16)
    binary = bin(original_int - 1).zfill(16)
    if binary[2:][0] == '1':
        return (int(take_opposite(binary[2:]), 2) * -1) / 100
    else:
        return original_int / 100
    

class UwbClient(object):

    def __init__(self):
        self.data = []
        self.buffer_data = []
        self.index = 0
        self.buffer = []

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
            data = codecs.encode(byte, 'hex_codec').decode()
            if data == '59':
                self.buffer.append(data)
            elif len(self.buffer) > 0:
                self.buffer.append(data)
                if data == '47':
                    if len(self.buffer) == int(self.buffer[2] + self.buffer[1], base=16):
                        current_data = self.buffer[-11:-5]
                        self.buffer_data = [handle_hex(current_data[1] + current_data[0]),
                                            handle_hex(current_data[3] + current_data[2]),
                                            handle_hex(current_data[5] + current_data[4])] 
                        self.index += 1
                    self.buffer = []
            else:
                self.buffer = []
        except Exception as e:
            self.buffer = []
            raise e
