from typing import Optional, Any, Dict

from aioredis import Redis

from coresvc.base.base_service import BaseService
import aioredis

from coresvc.serializer import serializer


class RedisStore(BaseService):
    def __init__(self, url, **kwargs):
        self.url = url
        self._redis: Optional[Redis] = None
        super().__init__(**kwargs)

    async def on_start(self) -> None:
        self._redis = await aioredis.create_redis_pool(self.url)

    async def on_started(self) -> None:
        self.log.info(self.label + ' started')

    async def on_stop(self) -> None:
        if self._redis:
            self._redis.close()
            await self._redis.wait_closed()

    async def set(self, key: str, data: Dict[str, Any]) -> None:
        if not self.started:
            raise RuntimeError(self.label + ' not started')

        value = serializer.dumps(data)
        await self._redis.set(key, value)

    async def get(self, key: str) -> Dict:
        if not self.started:
            raise RuntimeError(self.label + ' not started')

        value = await self._redis.get(key)
        return serializer.loads(value) if value else {}
