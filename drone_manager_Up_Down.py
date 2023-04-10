import logging
import socket
import sys
import time
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

DEFAULT_DISTANCE = 0.30

class DroneManager(object):
    def __init__(self, host_ip='192.168.10.2', host_port=8889,
                 drone_ip='192.168.10.1', drone_port=8889,
                 is_imperial=False):
        
        self.host_ip = host_ip
        self.host_port = host_port
        self.drone_ip = drone_ip
        self.drone_port = drone_port
        self.drone_address = (drone_ip, drone_port)
        self.is_imperial = is_imperial
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host_ip, self.host_port))
        self.socket.sendto(b'command', self.drone_address)
        self.socket.sendto(b'streamon', self.drone_address)
        
    def __dell__(self):
        self.stop()
        
    def stop(self):
        self.socket.close()
        
    def send_command(self, command):
        logger.info({'action': 'send_command', 'command': command})
        self.socket.sendto(command.encode('utf-8'), self.drone_address)
        
        #คำสั่งขึ้น
    def takeoff(self):
        self.send_command('takeoff')
        
        #คำสั่งลง
    def land(self):
        self.send_command('land')
        
        #คำสั่งกำหนดการเคลื่อนที่
    def move(self, direction, distance): 
        distance = float(distance)
        if self.is_imperial:
            distance = int(round(distance * 30.48))
        else:
            distance = int(round(distance * 100))
        return self.send_command(f'{direction} {distance}')

        #คำสั่งไปขึ้นข้างบน
    def up(self, distance=DEFAULT_DISTANCE):
        return self.move('up', distance)

        #คำสั่งไปลงขข้างล่าง
    def down(self, distance=DEFAULT_DISTANCE):
        return self.move('down', distance)
    
        #คำสั่งไปซ้าย
    def left(self, distance=DEFAULT_DISTANCE):
        return self.move('left', distance)
    
        #คำสั่งไปขวา
    def right(self, distance=DEFAULT_DISTANCE):
        return self.move('right', distance)
    
        #คำสั่งไปข้างหน้า
    def forward(self, distance=DEFAULT_DISTANCE):
        return self.move('forward', distance)
    
        #คำสั่งไปข้างหลัง
    def back(self, distance=DEFAULT_DISTANCE):
        return self.move('back', distance)
    
        #ตีลังกาไปทางซ้าย
    def flip_left(self):
        self.send_command('flip l')
        
        #ตีลังกาไปขวา
    def flip_right(self):
        self.send_command('flip r')
        
        #ตีลังกาไปข้างหน้า
    def flip_forward(self):
        self.send_command('flip f')
        
        #ตีลังกาไปข้างหลัง
    def flip_backward(self):
        self.send_command('flip b')
                
if __name__ == '__main__':
    drone_manager = DroneManager()
    
    drone_manager.takeoff()
    time.sleep(10)
    
    drone_manager.right() #ขวา
    time.sleep(5)
    drone_manager.back() #หลัง
    time.sleep(5)
    drone_manager.left() #ซ้าย
    time.sleep(5)
    drone_manager.forward() #ข้างหน้า
    time.sleep(5)
    drone_manager.up() #ขึ้น
    time.sleep(5)
    drone_manager.down() #ลง
    time.sleep(5)

    drone_manager.land()