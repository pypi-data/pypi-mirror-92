import socket
import ssl

import select
from urllib.parse import urlparse


# Для ws и wss в URL дописывается charger id
# protocol: ocpp1.5, ocpp1.6
def test_websocket_conn(cs_uri: str, protocol: str) -> None:
    print(f'Test connection to {cs_uri}...')

    url_items = urlparse(cs_uri)
    host = url_items.hostname
    is_ssl = url_items.scheme == 'wss'
    port = url_items.port or (443 if is_ssl else 80)
    path = url_items.path

    print(f'1. Open raw connection to {host}:{port}')
    
    try:
        with socket.create_connection((host, port), timeout=5.0) as s:
            if is_ssl:
                context = ssl.create_default_context()
                with context.wrap_socket(s, server_hostname=host) as ss:
                    _send_rcv(ss, host, port, path, protocol)
            else:
                _send_rcv(s, host, port, path, protocol)
    
    except Exception as ex:
        print(ex)

def _send_rcv(s, host, port, path, protocol):
    print(f'2. Send request')
    req_lines = [
        f'GET {path} HTTP/1.1',
        f'User-Agent: python',
        f'Host: {host}:{port}',
        f'Upgrade: WebSocket',
        f'Connection: Upgrade',
        f'Pragma: no-cache',
        f'Cache-Control: no-cache',
        f'Sec-WebSocket-Key: omf+YISYGBBTwPNsGSiWtg==',
        f'Sec-WebSocket-Protocol: {protocol}',
        f'Sec-WebSocket-Version: 13',
        f'\r\n',
    ]
    req = '\r\n'.join(req_lines)
    print('REQUEST:')
    print(req)
    s.sendall(req.encode('utf-8'))

    rcv_buf = bytearray()

    no_data_loops = 0
    while no_data_loops < 25:
        fd_read, fd_write, fd_err = select.select([s], [], [], 0.1)
        if s in fd_read:
            no_data_loops = 0
            data = s.recv(1024)
            if data:
                rcv_buf += data
            else:
                break
        else:
            no_data_loops += 1
    
    print(f'RESPONSE {len(rcv_buf)} bytes:')
    try:
        for ln in rcv_buf.split(b'\r\n'):
            rcv_str = ln.decode('utf-8')
            print(rcv_str)
    except Exception as ex2:
        print(ex2)
        print(rcv_buf)
