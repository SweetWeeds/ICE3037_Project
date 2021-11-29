from bluetooth import *

class BluetoothScanner:
    def __init__(self):
        self.charge_rate = 0

    def connect(self, addr: str="F0:08:D1:F2:AC:42") -> bool:
        #MAC address of ESP32
        self.addr = addr
        service_matches = find_service( address = self.addr )

        self.buf_size = 1

        if len(service_matches) == 0:
            print(f"couldn't find the SampleServer service (addr:{addr}")
            return False

        for s in range(len(service_matches)):
            print("\nservice_matches: [" + str(s) + "]:")
            print(service_matches[s])
            
        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

        port=1
        print("connecting to \"%s\" on %s, port %s" % (name, host, port))

        # Create the client socket
        self.sock = BluetoothSocket(RFCOMM)
        self.sock.connect((host, port))

        print("connected")
        return True
    
    def close(self):
        self.sock.close()

    def input_and_send(self):
        print("\nType something\n")
        while True:
            data = input()
            if len(data) == 0: break
            self.sock.send(data)
            self.sock.send("\n")
            
    def run(self):
        buf = ""
        while self.running:
            data = self.sock.recv(self.buf_size)
            if data:
                if (data == b'\n'):
                    self.charge_rate = int(buf)
                    print(self.charge_rate)
                    buf = ""
                else:
                    buf += data.decode('utf-8')
    
    def recv(self) -> str:
        buf = ""
        while True:
            #self.send()
            data = self.sock.recv(self.buf_size)
            if data:
                if (data == b'\0'):
                    break
                else:
                    buf += data.decode('utf-8')
        self.send(b'\0')
        return buf
    
    def send(self, data=b'\0'):
        self.sock.send(data)

if __name__ == "__main__":
    bs = BluetoothScanner()
