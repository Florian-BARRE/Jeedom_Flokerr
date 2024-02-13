from configuration import APP_CONFIG

from tools import writer_manager
from tools import ws_receiver

from tools.functions import dprint

import json


async def states_updates_routine():
    # Listen to callback messages
    while True:
        message = json.loads(await ws_receiver.states_updates_queue.get())

        if message.get("type") == "subscription_callback":
            dprint(f"Topic update: {message}", priority_level=2, source="STATES")
            topic = message["topic"]
            state = message["state"]
            writer_manager.write_state(topic, state)
