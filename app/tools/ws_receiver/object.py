import asyncio


class WSreceiver:
    def __init__(self):
        self.states_updates_queue = asyncio.Queue()
        self.devices_info_updates_queue = asyncio.Queue()

    async def ws_receiver_routine(self, websocket):
        """
        Coroutine to read received messages and add them in queues (one for each task).
        """
        while True:
            msg = await websocket.recv()
            await self.states_updates_queue.put(msg)
            await self.devices_info_updates_queue.put(msg)
