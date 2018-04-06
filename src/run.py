from multiprocessing import Process

from resources.lang.enGB.logs import *
from resources.global_resources.log_vars import logPass, logException
from config.config import get_cfg_serviceid, get_cfg_port_listener, get_cfg_port_broadcast
from discovery.broadcast import broadcast_service
from log.log import log_internal
from portlistener import start_bottle

port_threads = []

try:

    ################################

    log_internal(logPass, logDescStartingService, description='started')

    ################################
    # Initiate service broadcast

    process_broadcast = Process(target=broadcast_service, args=(get_cfg_serviceid(), get_cfg_port_broadcast(), ))
    process_broadcast.start()

    ################################
    # Port_listener

    log_internal(logPass, logDescPortListener.format(port=get_cfg_port_listener()), description='starting')

    start_bottle(port_threads)

    process_broadcast.terminate()

    log_internal(logPass, logDescPortListener.format(port=get_cfg_port_listener()), description='stopped')

except Exception as e:
    log_internal(logException, logDescStartingService, description='fail', exception=e)
    for t in port_threads:
        t._stop()
