import asyncio


class Relay(object):
    def __init__(self, actor):
        self.actor = actor
        self.duration = actor.settings.get_int("processing-duration", 0)

    async def process(self, apc):
        envelope = await apc.read_envelope_complete("default", 1)
        if self.duration != 0:
            asyncio.sleep(self.duration)
        await apc.forward("default", input_name="default")
