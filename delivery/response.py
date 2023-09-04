from typing import Iterator, Tuple
from sanic.response import HTTPResponse


class DeliveryHTTPResponse(HTTPResponse):
    # We override this method to prevent Sanic automatically setting or removing HTTP headers
    # e.g. original Sanic adds a Content-Type header to responses
    @property
    def processed_headers(self) -> Iterator[Tuple[bytes, bytes]]:
        return (
            (name.encode("ascii"), f"{value}".encode(errors="surrogateescape"))
            for name, value in self.headers.items()
        )
