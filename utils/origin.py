from typing import Optional

def set_origin_header(origin: Optional[str], headers: Optional[dict] = None) -> dict:
    new_headers = {}
    if headers is not None:
        new_headers.update(headers)
    if origin is None:
        return new_headers
    new_headers["Origin"] = origin
    new_headers["Referer"] = origin
    return new_headers