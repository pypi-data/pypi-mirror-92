from abc import ABC, abstractmethod
from typing import Any


class MediaRepository(ABC):
    @abstractmethod
    def retrieve(self, media_id: str, width: int = None) -> Any:
        raise NotImplementedError
