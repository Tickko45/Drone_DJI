import sys
import socket
import logging
import time

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

class DroneManager(object):
    """docstring for DroneManager."""
    def __init__(self, host_ip="192.168.10.2", host_port=8889,
                 drone_ip="192.168.10.1", drone_port=8889):
        self.host_ip = host_ip
        self.host_port = host_port
        self.drone_ip = drone_ip
        self.drone_port = drone_port
        self.drone_address = (drone_ip, drone_port)
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host_ip, host_port))
        self.socket.sendto(b"command", self.drone_address)
        self.socket.sendto(b"streamon", self.drone_address)
        
    def __dell__(self):
        self.stop()
        
    def stop(self):
        self.socket.close()
        
    def send_command(self, command):
        logger.info({'action' : 'send_command', 'command' : 'command'})
        self.socket.sendto(command.encode("utf8"), self.drone_address)
        
    def takeoff(self):
        self.send_command("takeoff")
        
    def land(self):
        self.send_command("land")
        
if __name__ == '__main__':
    dronemanage = DroneManager()
    dronemanage.takeoff()
    time.sleep(1)
    dronemanage.land()
        #super(DroneManager, self).__init__()
    #arg

    