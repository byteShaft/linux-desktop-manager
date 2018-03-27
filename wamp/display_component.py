import os

from autobahn.asyncio.component import Component, run
from autobahn.wamp.types import RegisterOptions

from ldm import manager

CONFIG_TRANSPORT = {
    "type": "websocket",
    "url": u"ws://localhost:8080/ws"
}
with open('/etc/machine-id') as f:
    MACHINE_ID = f.read().strip()
OPTIONS = RegisterOptions(match='exact', invoke='roundrobin')


component = Component(transports=[CONFIG_TRANSPORT], realm=u"realm1")
display = manager.Display(os.environ.get('XDG_CURRENT_DESKTOP', 'KDE').lower())


@component.register('com.om26er.ldm.machine-{}.is_screen_locked'.format(MACHINE_ID), OPTIONS)
def is_locked():
    return display.is_locked()


@component.register('com.om26er.ldm.machine-{}.lock_screen'.format(MACHINE_ID), OPTIONS)
def lock():
    return display.lock()


def main():
    run(component)


if __name__ == '__main__':
    main()
