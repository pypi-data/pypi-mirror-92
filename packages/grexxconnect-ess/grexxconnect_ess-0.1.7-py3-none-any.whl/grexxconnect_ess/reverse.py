import asyncio

from .ess_connect import EssConnect
from .log import init_logger

hasReversed = False
logger = init_logger(__name__, testing_mode=False)


async def handle_message(message):
    global logger
    global hasReversed

    logger.info(f"Got message {message}")
    reversedValue = message["parsed"]["content"][0]["value"][::-1]
    logger.info(f"Sending result: {reversedValue}")
    await message["resolve"]([{
        "reference": 'result',
        "values":    [{"value": reversedValue}]
    }])
    logger.info("Done doing the reeeeeeverse!")
    hasReversed = True


def handle_auth(queue):
    logger.info(f'Authorized! {queue}')


def handle_disconnect(a, b):
    logger.warn(f"Disconnected! {a}, {b} ")


def handle_error(error):
    logger.error("Error:", error)


def monitor_repsonse():
    global hasReversed
    status = 'warning' if hasReversed else 'ok'
    message = 'O... My... God.... I just reversed a value!' if hasReversed else 'Feeling good...'
    hasReversed = False
    return {
        "status":          status,  # // 'warning',
        "message":         message,  # // 'Something is wrong.... check me!',
    }


GrexxConnectEss = EssConnect({
    "applicationName": "Jeffrey's ESS v1.2",
    "debug":           True,
    "server":          "wss://ess-test.grexxconnect.com",
    "username":        "jeffrey.reverse",
    "password":        "^;bB]-^V?xvexR=Q`d*GF.Wc6G#_&h?@"  # //== prd-cluster
}, monitor_repsonse)

GrexxConnectEss.register_callback('message', handle_message)
GrexxConnectEss.register_callback('disconnected', handle_disconnect)
GrexxConnectEss.register_callback('error', handle_error)
GrexxConnectEss.register_callback('authorized', handle_auth)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(GrexxConnectEss.start_client())
