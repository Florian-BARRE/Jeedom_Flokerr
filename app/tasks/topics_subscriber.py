from configuration import APP_CONFIG

from tools import writer_manager
from tools.functions import subscribe_request

import asyncio


async def subscribe_to_topics(websocket):
    """
    This function is used to subscribe to topics which are in topics.txt file
    :param websocket:
    :return:
    """
    # Subscribe to topics
    with open(APP_CONFIG.TOPICS_PATH, 'r') as file:
        for topic in file:
            # Skip line if starts by # -> it is a comment not a topic
            if topic[0] != "#":
                await subscribe_request(websocket, topic.strip())
                await asyncio.sleep(0.1)  # Avoid to be kicked by the server

    # Update states
    writer_manager.save_states()
