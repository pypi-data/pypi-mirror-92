from functools import cached_property
from typing import Callable, Dict, Any

import faust
from faust import TopicT


class KafkaClient(faust.App):
    def __init__(self, app_id, broker='kafka://', store='rocksdb://', topic_to_model: dict = None):
        self.topic_to_model = topic_to_model or {}
        super().__init__(app_id, broker=broker, store=store)

    async def on_first_start(self) -> None:
        self.log.info(f'registered_topics {self.registered_topics}')

    @cached_property
    def registered_topics(self) -> Dict[str, TopicT]:
        topics = {}
        for key, val in self.topic_to_model.items():
            topics[key] = self.topic(key, value_type=val)
        return topics

    async def publish(self, topic_name: str, value: Any):
        if topic := self.registered_topics.get(topic_name, None):
            return await topic.send(value=value)
        raise KeyError('topic not registered')

    def subscribe(self, topic_name: str, callback: Callable):
        async def process(stream: faust.Stream):
            async for value in stream:
                await callback(value)

        if topic := self.registered_topics.get(topic_name, None):
            return self.agent(topic)(process)
        raise KeyError('topic not registered')
