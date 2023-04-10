import logging
import socket
import sys
import time

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


class DroneManager(object):
    def __init__(self, host_ip='192.168.10.2', host_port=8889,
                 drone_ip='192.168.10.1', drone_port=8889):
        self.host_ip = host_ip
        self.host_port = host_port
        self.drone_ip = drone_ip
        self.drone_port = drone_port
        self.drone_address = (drone_ip, drone_port)
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


    def flipleft(self):
        """
        Flips.

        :param direction: Direction to flip, 'l', 'r', 'f', 'b'.
        :return: Response from Tello, 'OK' or 'FALSE'.
        """
        return self.send_command(f'flip l')

if __name__ == '__main__':
    dronemanage = DroneManager()
    dronemanage.takeoff()
    time.sleep(5)
    dronemanage.flipleft()
    dronemanage.land()
        # super(DroneManager, self).init()
    # arg