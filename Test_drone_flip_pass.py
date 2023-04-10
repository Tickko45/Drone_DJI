import logging
import socket
import sys
import time
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
DEFAULT_DISTANCE = 2.30

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
    def takeoff(self):
        self.send_command('takeoff')
    def land(self):
        self.send_command('land')
        
    def move(self, direction, distance):
        distance = float(distance)
        if self.is_imperial:
            distance = int(round(distance * 30.48))
        else:
            distance = int(round(distance * 100))
        return self.send_command(f'{direction} {distance}')

    def up(self, distance=DEFAULT_DISTANCE):
        return self.move('up', distance)

    def down(self, distance=DEFAULT_DISTANCE):
        return self.move('down', distance)
    
    def flip_left(self):
        self.send_command('flip l')
    def flip_right(self):
        self.send_command('flip r')
    def flip_forward(self):
        self.send_command('flip f')
    def flip_backward(self):
        self.send_command('flip b')
                
if __name__ == '__main__':
    drone_manager = DroneManager()
    
    drone_manager.takeoff()
    time.sleep(1)

    drone_manager.up()
    time.sleep(5)
#    drone_manager.down()
#    time.sleep(5)
    
    drone_manager.flip_left()
    time.sleep(5)
    drone_manager.flip_right()
    time.sleep(5)
    drone_manager.flip_forward()
    time.sleep(5)
    drone_manager.flip_backward()
    time.sleep(5)
    drone_manager.land()