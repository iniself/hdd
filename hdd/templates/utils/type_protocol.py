from typing import Protocol, overload, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from hdd.service.config import ConfigManager
    from hdd.service.pipeline import Pipeline


class CoreProtocol(Protocol):
    @overload
    def make(self, key: Literal["config"]) -> "ConfigManager": ...
    @overload
    def make(self, key: Literal["pipeline"]) -> "Pipeline": ...

    @overload
    def __call__(self, key: Literal["config"]) -> "ConfigManager": ...
    @overload
    def __call__(self, key: Literal["pipeline"]) -> "Pipeline": ...
