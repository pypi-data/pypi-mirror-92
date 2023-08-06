import base64
from datetime import datetime
from typing import Callable, List, Dict

from .client import WebSocketClient
from .log import init_logger


class EssConnect:
    ws: WebSocketClient
    callbacks: Dict[str, Callable]

    def __init__(self, settings, status_function):
        self.setMonitoringResponse(status_function)
        creds = settings["username"] + ":" + settings["password"]
        creds = base64.b64encode(creds.encode("utf-8")).decode("utf-8")
        version = "1.0.8"
        app_name = settings["applicationName"]
        options = {
            "headers": {
                "User-Agent": f"ESS-Python-Agent v{version} - {app_name}",
                "Authorization": "Basic " + creds
            },
            "debug": settings["debug"]
        }
        self.callbacks = {}
        self.logger = init_logger(__name__, testing_mode=False)

        self.ws = WebSocketClient(settings["server"], options)

        self.ws.register_callback('close', self.on_close)
        self.ws.register_callback('message', self.on_message)
        self.ws.register_callback('error', self.on_error)
        self.ws.register_callback('timeout', self.on_timeout)

    async def start_client(self):
        await self.ws.start()

    async def on_message(self, _message):
        message_type = _message['type']
        self.logger.debug(_message)
        if message_type == "ping":
            self.logger.debug('responding to connection-ping')
            await self.send('pong', {})
        elif message_type == "authorized":
            self.logger.info(
                ('connected and authorized for', _message["namespace"]))
            self.callbacks['authorized'](_message["namespace"])
        elif message_type == "system":
            await self.handle_system_message(_message)
        elif message_type == "message":
            self.current_message = _message
            await self.callbacks['message']({
                "content": _message["content"],
                "parsed":  self.parse_message(_message["content"]["data"]),
                "resolve": self.handle_output
            })
        else:
            self.logger.warning(f"Unknown MessageType {message_type}")

    def on_close(self, error):
        self.logger.info("close has been called")
        self.callbacks['disconnected'](error)

    def on_error(self, error):
        self.logger.error(error)
        self.callbacks['error'](error)

    def on_timeout(self, error):
        self.logger.error('ESS-Timeout', error)

    async def handle_output(self, output_data):
        await self.send('response', {
            "toMessage":  self.current_message,
            "outputData": output_data
        })

    async def send(self, message_type, content):
        try:
            await self.ws.send({
                "type":      message_type,
                "content":   content,
                "timestamp": str(datetime.now())
            })
        except Exception as e:
            self.logger.error(("Error", e))

    async def handle_system_message(self, message):
        if message["content"]["action"] == "ping":
            self.logger.debug("responding to system-ping")
            try:
                await self.send('system', {
                    "action":      'pong',
                    "client_data": self._start_function() if callable(self._start_function) else {"status": 'ok'},
                    "server_data": message["content"]["id"]
                })
            except Exception as e:
                self.logger.error(("Error", e))

    def setMonitoringResponse(self, start_function):
        self._start_function = start_function

    def parse_message(self, message: List[str]):
        return {part['reference']: part['values'] for part in message}

    def register_callback(self, event, callback: Callable) -> None:
        if event in self.callbacks:
            self.logger.debug(f"Replacing callback function for {event} event")
        else:
            self.logger.debug(f"Setting callback function for {event} event")
        self.callbacks[event] = callback
