import logging

import scenarios # noqa

from dialogic.dialog_connector import DialogConnector
from dialogic.server.flask_server import FlaskServer

from dialog_manager import make_dm

logging.basicConfig(level=logging.DEBUG)

dm = make_dm()
connector = DialogConnector(
    dialog_manager=dm,
    alice_native_state='session',
)
server = FlaskServer(connector=connector)

handler = connector.serverless_alice_handler

if __name__ == '__main__':
    server.parse_args_and_run()
