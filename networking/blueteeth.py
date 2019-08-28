import bluetooth


class BluetoothClient:
    """
    Usage::

        speaker_1 = 'skrrrrr'
        client = BluetoothClient()
        speaker_1_addr = client.find_and_save_mac(speaker_1)
        client.connect('C0:28:8D:45:50:77')
        while True:
            a = input('? ')
            if a == 'q':
                break
            elif a == 'a':
                file_data = Converter.file_to_binary('audio/song1.mp3')
                client.socket.send(file_data)
    """

    def __init__(self):
        self.port = 0x0003
        self.socket = bluetooth.BluetoothSocket(bluetooth.L2CAP)

    @staticmethod
    def find_and_save_mac(device_name: str) -> str:
        devices = bluetooth.discover_devices()
        target_address = None
        for bdaddr in devices:
            if bluetooth.lookup_name(bdaddr) == device_name:
                target_address = bdaddr
        if target_address:
            with open(f'devices/{device_name}', 'w') as file:
                file.write(target_address)
        return target_address

    def connect(self, device_addr: str) -> None:
        self.socket.connect((device_addr, self.port))

    def close(self) -> None:
        self.socket.close()
