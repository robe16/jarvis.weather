from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from time import sleep

from log.log import log_internal
from parameters import broadcast_frequency
from resources.lang.enGB.logs import *
from resources.global_resources.broadcast import *
from resources.global_resources.variables import serviceType
from resources.global_resources.log_vars import logException


def broadcast_service(service_id, self_port):
    try:
        #
        msg = jarvis_broadcast_msg.format(service_id=service_id,
                                          service_type=serviceType,
                                          port=str(self_port))
        #
        while True:
            broadcast_msg(msg)
            sleep(broadcast_frequency)
        #
    except Exception as e:
        log_internal(logException, logDesc_services_Broadcast, exception=e)


def broadcast_msg(msg):
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('0.0.0.0', 0))
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        #
        s.sendto(msg.encode(), ('<broadcast>', jarvis_broadcastPort))
        #
        return True
        #
    except Exception as e:
        #
        log_internal(logException, logDesc_Broadcast, exception=e)
        return False
