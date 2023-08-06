from __future__ import annotations

from typing import Iterable

from mode import Service


class BaseService(Service):
    """
    Service life cycle.

    When starting (await Service.start())
    - The on_first_start callback is called.
    - Service logs: "[Service] Starting...".
    - on_start callback is called.
    - All @Service.task background tasks are started (in definition order).
    - All child services added by add_dependency(), or on_init_dependencies()) are started.
    - Service logs: "[Service] Started".
    - The on_started callback is called.

    When stopping (await Service.stop())
    - Service logs; "[Service] Stopping...".
    - The on_stop() callback is called.
    - All child services are stopped, in reverse order.
    - All asyncio futures added by add_future() are cancelled in reverse order.
    - Service logs: "[Service] Stopped".
    - If Service.wait_for_shutdown = True, it will wait for the Service.set_shutdown() signal to be called.
    - All futures started by add_future() will be gathered (awaited).
    - The on_shutdown() callback is called.
    - The service logs: "[Service] Shutdown complete!".

    When restarting (await Service.restart())
    - The service is stopped (await service.stop()).
    - The __post_init__() callback is called again.
    - The service is started (await service.start()).
    """

    def __post_init__(self) -> None:
        """Additional user initialization."""
        ...

    async def on_first_start(self) -> None:
        """Service started for the first time in this process."""
        self.log.info(self.label + ' first starting')

    async def on_start(self) -> None:
        """Service is starting."""
        self.log.info(self.label + ' starting')

    def on_init_dependencies(self) -> Iterable[BaseService]:
        """Return list of service dependencies for this service."""
        return []

    async def on_started(self) -> None:
        """Service has started."""
        self.log.info(self.label + ' started')

    async def on_stop(self) -> None:
        """Service is being stopped/restarted."""
        self.log.info(self.label + ' stopping')

    async def on_shutdown(self) -> None:
        """Service is stopped and shutdown."""
        self.log.info(self.label + ' shutdown')

    async def on_restart(self) -> None:
        """Service is being restarted."""
        self.log.info(self.label + ' restarting')
