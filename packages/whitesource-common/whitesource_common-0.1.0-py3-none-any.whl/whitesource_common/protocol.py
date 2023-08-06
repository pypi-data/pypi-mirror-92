import dataclasses
import enum
import typing


@dataclasses.dataclass(frozen=True)
class WhiteSourceApiExtensionWebsocketWSConfig:
    apiKey: str
    extraWsConfig: typing.Dict
    productToken: str
    projectName: str
    requesterEmail: str
    userKey: str
    wssUrl: str


@dataclasses.dataclass(frozen=True)
class WhiteSourceApiExtensionWebsocketMetadata:
    chunkSize: int
    length: int


@dataclasses.dataclass(frozen=True)
class WhiteSourceApiExtensionWebsocketContract:
    metadata: WhiteSourceApiExtensionWebsocketMetadata
    wsConfig: WhiteSourceApiExtensionWebsocketWSConfig


class WhiteSourceApiExtensionStatusCodeReasons(enum.IntEnum):
    CONTRACT_VIOLATION = 4000
    CHUNK_SIZE_TOO_BIG = 4001
    BINARY_CORRUPTED = 4002
