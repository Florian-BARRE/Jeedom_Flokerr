import asyncio
import websockets

from configuration import APP_CONFIG
from tools import ws_receiver
from tools.functions import authentication_request, dprint

from tasks.topics_subscriber import subscribe_to_topics
from tasks.states_updates_manager import states_updates_routine
from tasks.devices_info_updates_manager import devices_info_updates_routine


async def main():
    async with websockets.connect(APP_CONFIG.WS_URI) as websocket:
        # Authenticate
        if not await authentication_request(websocket):
            return

        # Subscribe to topics
        dprint("Subscribe to all topics.", priority_level=1, preprint="\n\n")
        await subscribe_to_topics(websocket)

        # Create all coroutines (message_receiver_supervisor / states_updater / devices_info_updater)
        msg_receiver = asyncio.create_task(ws_receiver.ws_receiver_routine(websocket))
        states_updater = asyncio.create_task(states_updates_routine())
        devices_info_updater = asyncio.create_task(devices_info_updates_routine(websocket))

        # Start coroutines
        await asyncio.gather(msg_receiver, states_updater, devices_info_updater)


if __name__ == "__main__":
    asyncio.run(main())
