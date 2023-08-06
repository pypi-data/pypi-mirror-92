from abc import ABC
from typing import Optional


class Headers:
    def __init__(self, role=None, user_id=None, key=None, **kwargs):
        headers = {"x-gapo-role": role or "service"}

        if key:
            headers.update({"x-gapo-api-key": key})

        if user_id:
            headers.update({"x-gapo-user-id": user_id})

        if kwargs:
            headers.update(kwargs)

        self._h = headers

    def dict(self):
        return self._h


class AbstractRequest(ABC):
    service: str
    endpoint: str = ""
    key: str
    response: Optional
    Response: Optional
    Params: Optional

    def __init__(self, client_cfg: dict, client_session):
        self.url = client_cfg[self.service] + "/" + self.endpoint

        api_key = client_cfg.get(
            getattr(self, "key", None) or (self.service + "___KEY")
        )

        self.headers = Headers(
            role=getattr(self, "role", None),
            key=api_key,
            user_id=getattr(self, "user_id", None),
        )

        self._cl = client_session
