from configuration import APP_CONFIG

from tools import writer_manager, ws_receiver

import json
import time


def get_current_timestamp():
    """
    This function returns the current timestamp in milliseconds.
    :return:
    """
    return int(time.time() * 1000)


def dprint(str_to_print, priority_level=1, preprint="", hashtag_display=True, date_display=True, source=None):
    """
    This function is used to print debug messages
    :param str_to_print:
    :param priority_level:
    :param preprint:
    :param hashtag_display:
    :param date_display:
    :param source:
    :return:
    """
    if APP_CONFIG.PRIORITY_DEBUG_LEVEL >= priority_level:
        str_ident = "".join("-" for _ in range(priority_level))

        # Date display
        if date_display:
            date = f" [{time.strftime('%d/%m/%y, %H:%M:%S', time.localtime()) + '.{:03d}'.format(get_current_timestamp() % 1000)}] "
        else:
            date = ""

        output = f"{preprint}{date}"

        if source:
            output += f" [{source}] "
        if hashtag_display:
            output += f"#{str_ident} "

        output += str_to_print
        print(output)


"""
    Requests function to interact with the API
"""


async def authentication_request(socket) -> bool:
    """
    This function is used to authenticate current client to websocket
    with user gives in configuration.
    Don't use ws_receiver in this function ! Its coroutine is executed later, use directly websocket object.
    :param socket:
    :return:
    """
    dprint("Authenticating...", priority_level=1)
    request = {
        "type": "authenticate",
        "username": APP_CONFIG.USERNAME,
        "password": APP_CONFIG.PASSWORD,
        "infos": APP_CONFIG.INFO
    }
    dprint(f"Sending authentication request: {request}", priority_level=2)
    await socket.send(json.dumps(request))
    response = json.loads(await socket.recv())

    if response["status_code"] == 200:
        dprint(f"Authentication successful !", priority_level=2)
        dprint(f"privileges: {response.get('privileges', 'not found')}", priority_level=3)
        dprint(f"uuid: {response.get('uuid', 'not found')}", priority_level=3)
        return True
    else:
        dprint(f"Authentication failed.", priority_level=2)
        dprint(f"Response: {response}", priority_level=3)
        return False


async def subscribe_request(socket, topic):
    """
    This function is used to subscribe to a topic. It also got its last value
    and update states.json file according to the topic and value.
    Don't use ws_receiver in this function ! Its coroutine is executed later, use directly websocket object.
    :param socket:
    :param topic:
    :return:
    """
    dprint(f"Subscribe to [{topic}]", priority_level=2, preprint="\n")
    request = {
        "type": "subscribe",
        "topic": topic,
        "get_current_value": 1
    }
    dprint(f"Sending subscribing request: {request}", priority_level=3)

    raw_response = None
    try:
        await socket.send(json.dumps(request))
        raw_response = await socket.recv()
        response = json.loads(raw_response)

        # Differentiate between subscription response and subscription callback
        # - Subscription callback: (wait another response while we get subscription response)
        while response.get("type") == "subscription_callback":
            raw_response = await socket.recv()
            response = json.loads(raw_response)

        # - Subscription response:
        dprint(f"Subscribing successful !", priority_level=3)
        dprint(f"Current value: {response.get('current_value', 'not found')}", priority_level=4)
        writer_manager.update_state(topic, response.get('current_value', 'null'))
        return True

    except Exception as error:
        dprint(f"Subscribing failed (error).", priority_level=3)
        dprint(f"Error: {error}", priority_level=4)
        dprint(f"Response: {raw_response}", priority_level=4)
        return False


async def ping_ws_clients_request(socket):
    """
    This function get all the connected clients with their authentication info
    Return server response if success, False if failed
    :return: response or False
    """
    dprint(f"Get ping result of ws clients.", priority_level=1, preprint="\n\n", source="PING")
    request = {
        "type": "ping_ws_device"
    }
    dprint(f"Sending ping request: {request}", priority_level=2, source="PING")

    raw_response = None
    try:
        await socket.send(json.dumps(request))
        raw_response = await ws_receiver.devices_info_updates_queue.get()
        response = json.loads(raw_response)

        # Differentiate between ping_ws_device response and subscription callback
        # - Subscription callback: (wait another response while we get subscription response)
        while response.get("type") == "subscription_callback":
            raw_response = await ws_receiver.devices_info_updates_queue.get()
            response = json.loads(raw_response)

        # - Subscription response:
        dprint(f"Ping request success successful !", priority_level=2, source="PING")
        dprint(f"Connected devices count: {response.get('devices_count', 'not found')}", priority_level=3,
               source="PING")
        return response

    except Exception as error:
        dprint(f"Ping failed (error).", priority_level=2, source="PING")
        dprint(f"Error: {error}", priority_level=3, source="PING")
        dprint(f"Response: {raw_response}", priority_level=3, source="PING")
        return False
