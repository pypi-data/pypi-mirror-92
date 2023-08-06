import sys
import argparse
import logging
import traceback 

from urllib.parse import urlparse

import requests


import asyncio
import websockets
import ssl

from aiohttp import web

from .mylog import configure_arg_parser_for_log, configure_logger
from .test_conn import test_websocket_conn


SAMPLE_CLOUD = 'ws://cloud.v4d.ru:8180/steve/websocket/CentralSystemService'


async def ws_handler(env):
    uri = env.cloud + '/' + env.id
    if env.is_ssl:
        ssl_context = ssl.create_default_context()
        async with websockets.connect(uri, subprotocols=[env.ocpp], ssl=ssl_context) as ws:
            #await websocket.send(name)
            #print(f"> {name}")
            print('ok')
            #greeting = await websocket.recv()
    else:
        async with websockets.connect(uri, subprotocols=[env.ocpp]) as ws:
            #await websocket.send(name)
            #print(f"> {name}")
            print('ok')
            #greeting = await websocket.recv()


async def hello(request):
    return web.Response(text="Hello, world")
    
    
async def web_server(env):
    server = web.Server(hello)
    runner = web.ServerRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

    #app.add_routes([web.static('/www', './www')])

    #routes.static('/prefix', path_to_static_folder)
    #print("======= Serving on http://127.0.0.1:8080/ ======")

    while True:
        await asyncio.sleep(1000)

def main():
    parser = argparse.ArgumentParser()
    configure_arg_parser_for_log(parser)
    parser.add_argument('--cloud', help='Cloud')
    parser.add_argument('--id', help='Override charger id')
    parser.add_argument('--ocpp', help='OCPP version', default='ocpp1.5')
    parser.add_argument('--debug', '-d', help='Debug mode', action='store_true')
    parser.add_argument('--test', help='Just open connection', action='store_true')
    #parser.add_argument('--web', help='Just open connection', action='store_true')
    env = parser.parse_args()

    # Logging
    configure_logger(env)
    log = logging.getLogger()

    try:
        if not env.id:
            raise UserWarning(f'Specify ChargerId: --id. E.g. --id abcd1234')

        if not env.cloud:
            raise UserWarning(f'Specify CentralSystem location: --cloud. E.g. --cloud {SAMPLE_CLOUD}')
            
        url_items = urlparse(env.cloud)
        if url_items.scheme not in ('http', 'https', 'ws', 'wss'):
            raise UserWarning(f'Invalid cloud scheme: {url_items.scheme}. Should be http, https, ws, wss')
        
        env.is_websocket = url_items.scheme in ('ws', 'wss')
        env.is_ssl = url_items.scheme in ('https', 'wss')
            
        if env.test:
            if env.is_websocket:
                test_websocket_conn(env.cloud + '/' + env.id, env.ocpp)
            else:
                raise UserWarning('URL detected as SOAP, but no soap connection tester detected')
        else:
            loop = asyncio.get_event_loop()
            loop.create_task(ws_handler(env))
            #loop.create_task(web_server(env))
            try:
                loop.run_forever()
            except KeyboardInterrupt:
                print('Goodbye')
            loop.close()
            
    except UserWarning as ex:
        log.error(ex)
        return 1

    except Exception as ex:
        if env.debug:
            traceback.print_exc()
        else:
            log.error(ex)
        return 1
        
    return 0

#==========================================

sys.exit(main())
