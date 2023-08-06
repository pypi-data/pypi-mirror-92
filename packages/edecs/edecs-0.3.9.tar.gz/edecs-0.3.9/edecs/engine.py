from time import time
import asyncio
from .models import Event
from .managers import (EntityManager, ComponentManager,
                       SystemManager, EventManager)

try:
    import uvloop
except ImportError:
    pass
else:
    uvloop.install()

class Engine():

    @property
    def entity_manager(self):
        return self._entity_manager

    @property
    def component_manager(self):
        return self._component_manager

    @property
    def system_manager(self):
        return self._system_manager

    @property
    def event_manager(self):
        return self._event_manager

    def __init__(self):
        self._entity_manager = EntityManager()
        self._component_manager = ComponentManager()
        self._system_manager = SystemManager()
        self._event_manager = EventManager()

        self.last_update = time()

    def create_system(self, system):
        system.create(self._entity_manager, self._component_manager,
                      self._system_manager, self._event_manager)

    def destroy_system(self, system):
        system.destroy()

    def generate_input(self, event_type='InputEvent', data={}):
        event = Event(sysname='ENGINE', event_type=event_type, data=data)

        self._event_manager.add_event(event)

    def send_input(self, event):
        self._event_manager.add_event(event)

    def get_output(self):
        return self._event_manager._engine_events

    def update(self):
        systems = self.system_manager.system_types

        for system in systems.values():
            if getattr(system, 'update', None) is not None:
                system.update(time()-self.last_update)

        self.last_update = time()

        while not self.event_manager.empty:
            self.event_manager.update_events()

    async def a_update_events(self):
        ev_manager = self.event_manager
        loop = self.loop
        while True:
            async for fn, event in ev_manager.a_get_events():
                if asyncio.iscoroutinefunction(fn):
                    loop.create_task(fn(event))
                else:
                    fn(event)

            await asyncio.sleep(0)

    async def a_shutdown_checker(self):
        while True:
            engine_events = self.get_output()

            while len(engine_events) > 0:
                event = engine_events.pop(0)

                if event.type == 'StopEngineEvent':
                    self.shutdown()
                    self.loop.stop()

            await asyncio.sleep(0)


    def a_run(self, upd_time=0):
        systems = self.system_manager.system_types
        self.loop = asyncio.get_event_loop()

        self.loop.create_task(self.a_update_events())
        self.loop.create_task(self.a_shutdown_checker())

        for system in systems.values():
            self.loop.create_task(system.a_update(upd_time))

        self.loop.run_forever()

    def shutdown(self):
        systems = self.system_manager.system_types

        for system in systems.values():
            self.destroy_system(system)
