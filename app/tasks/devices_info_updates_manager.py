from configuration import APP_CONFIG
from tools import writer_manager

import asyncio
from tools.functions import ping_ws_clients_request, dprint


def get_devices_name():
    devices_to_track = []
    with open(APP_CONFIG.DEVICES_PATH, 'r') as file:
        for device in file:
            devices_to_track.append(device.strip())

    return devices_to_track


def extract_device_info(response_info, device_name):
    """
    Extract device info from the request response
    Device info are: version, type, ip, ping, last_action_date, uuid, is_connected
    If the device is not found, return is_connected (value to 0) and '?' for the other fields
    :param request_response:
    :param device_name:
    :return: device_info
    """
    for device in response_info:
        if device.get("name") == device_name:
            return {
                "version": device.get("version", "?"),
                "type": device.get("type", "?"),
                "ip": device.get("ip", "?"),
                "ping": device.get("ping", "?"),
                "last_action_date": device.get("last_action_date", "?"),
                "uuid": device.get("uuid", "?"),
                "is_connected": 1
            }

    return {
        "version": "?",
        "type": "?",
        "ip": "?",
        "ping": "?",
        "last_action_date": "?",
        "uuid": "?",
        "is_connected": 0
    }


def extract_extra_info(request_response, tracked_devices):
    """
    Extract extra info from the request response
    Extra info are: devices_count and all devices.txt which are not tracked (laptop / jeedom_ws / ...)
    :param request_response:
    :param tracked_devices:
    :return: extra_info
    """
    extra_info = {
        "devices_count": request_response.get("devices_count", "not found"),
        "not_tracked_devices": []
    }

    for ws_client in request_response.get("infos", []):
        if ws_client.get("name") not in tracked_devices:
            extra_info["not_tracked_devices"].append(ws_client)

    return extra_info


async def devices_info_updates_routine(websocket):
    devices_to_track = get_devices_name()

    while True:
        # Get the devices.txt info
        response = await ping_ws_clients_request(websocket)

        # If response is False (failed), try again 5s later
        if response is False:
            await asyncio.sleep(5)
            continue

        # If response is not False, update the states
        for device in devices_to_track:
            device_info = extract_device_info(response.get("infos"), device)

            dprint(f"Device [{device}]", priority_level=4, source="PING")
            dprint(f"Infos: {device_info}", priority_level=5, source="PING")

            for key, value in device_info.items():
                if device[-1] != "/":
                    device += "/"
                states_topic = f"devices/{device}{key}"
                writer_manager.update_state(states_topic, value)

        # If ENABLE_EXTRA_PING_INFO is True add, extra info from request response
        if APP_CONFIG.ENABLE_EXTRA_PING_INFO:
            extra_info = extract_extra_info(response, devices_to_track)
            writer_manager.update_state("devices/extra_infos", extra_info)

        writer_manager.save_states()
        await asyncio.sleep(APP_CONFIG.PING_WS_CLIENTS_INTERVAL)
