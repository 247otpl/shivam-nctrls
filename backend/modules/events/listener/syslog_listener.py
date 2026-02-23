# backend/modules/events/listener/syslog_listener.py

import socket
import threading
from datetime import datetime

from ..event_store import store_event
from ..device_resolver import resolve_device  # we create this next


BUFFER_SIZE = 4096


def start_syslog_listener(base_dir, host="0.0.0.0", port=1514):

    def listener():

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))

        print(f"[SYSLOG] Listening on UDP {port}")

        while True:
            try:
                data, addr = sock.recvfrom(BUFFER_SIZE)
                message = data.decode(errors="ignore")

                source_ip = addr[0]

                device_info = resolve_device(base_dir, source_ip)
                if not device_info:
                    continue

                org_id = device_info["org_id"]
                site_id = device_info["site_id"]
                device_id = device_info["device_id"]

                event = {
                    "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "device_id": device_id,
                    "source_ip": source_ip,
                    "message": message
                }

                store_event(base_dir, org_id, site_id, event)

            except Exception as e:
                print("[SYSLOG ERROR]", e)

    thread = threading.Thread(target=listener, daemon=True)
    thread.start()