from typing import Union

TEncoded = Union[bytes, memoryview]
TDecoded = Union[str, int, float]
TEncodable = Union[TEncoded, TDecoded]
