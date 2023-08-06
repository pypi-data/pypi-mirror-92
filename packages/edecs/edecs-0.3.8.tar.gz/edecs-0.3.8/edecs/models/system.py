from time import time
from asyncio import iscoroutinefunction, sleep
from .event import Event
from .exceptions import (SystemNotCreated, SystemAlreadyExists)


class System():
    '''Base system class'''

    __slots__ = ['_type', '_entity_manager', '_component_manager',
                 '_system_manager', '_event_manager', 'alive']

    default_system_type = None


    @property
    def type(self):
        return self._type

    @property
    def initialized(self):
        return self._entity_manager and self._component_manager and \
               self._system_manager and self._event_manager

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


    def __init__(self, system_type=None):
        self._type = system_type or self.default_system_type or type(self).__name__

        self.alive = False

        self._entity_manager = None
        self._component_manager = None
        self._system_manager = None
        self._event_manager = None

        self._subscribed_functions = []


    def create_entity(self, entity):
        if not self.initialized:
            raise SystemNotCreated(self)

        entity.create(self._entity_manager, self._component_manager)

    def destroy_entity(self, entity):
        if not self.initialized:
            raise SystemNotCreated(self)

        entity.destroy()

    def generate_event(self, event_type, data={}):
        if not self.initialized:
            raise SystemNotCreated(self)

        event = Event(self.type, event_type, data)
        self._event_manager.add_event(event)

    def send_event(self, event):
        if not self.initialized:
            raise SystemNotCreated(self)

        self._event_manager.add_event(event)

    def generate_engine_event(self, event_type, data={}):
        if not self.initialized:
            raise SystemNotCreated(self)

        event = Event(self.type, event_type, data)
        self._event_manager.add_engine_event(event)

    def send_engine_event(self, event):
        if not self.initialized:
            raise SystemNotCreated(self)

        self._event_manager.add_engine_event(event)

    def subscribe(self, fn, event_type):
        # TO DO: decorator
        if not self.initialized:
            raise SystemNotCreated(self)

        self._subscribed_functions.append((fn, event_type))
        self._event_manager.subscribe(fn, event_type)

    def unsubscribe(self, fn, event_type):
        if not self.initialized:
            raise SystemNotCreated(self)

        self._subscribed_functions.remove((fn, event_type))
        self._event_manager.unsubscribe(fn, event_type)

    def create(self, entity_manager, component_manager,
                                                system_manager, event_manager):
        if self.initialized:
            raise SystemAlreadyExists(self)

        self._entity_manager = entity_manager
        self._component_manager = component_manager
        self._system_manager = system_manager
        self._event_manager = event_manager

        self._system_manager.create_system(self)

        self.alive = True
        self.init()

    def destroy(self):
        self.alive = False
        self.final()

        if not self.initialized:
            raise SystemNotCreated(self)

        for subscriber in self._subscribed_functions:
            self._event_manager.unsubscribe(subscriber[0], subscriber[1])
        self._system_manager.destroy_system(self)

        self._entity_manager = None
        self._component_manager = None
        self._system_manager = None
        self._event_manager = None

    async def a_update(self, upd_time=0):
        if getattr(self, 'update', None) is not None:
            last_update = time()
            if iscoroutinefunction(self.update):
                while self.alive:
                    new_update = time()
                    await self.update(new_update-last_update)
                    last_update = new_update
                    await sleep(upd_time)

            else:
                while self.alive:
                    new_update = time()
                    self.update(new_update-last_update)
                    last_update = new_update
                    await sleep(upd_time)


    def init(self):
        pass

    #def update(self, dt):
        #pass

    def final(self):
        pass
