from typing import Optional
from abc import ABC
from urllib import parse
from asyncio import iscoroutinefunction
from pydantic import BaseModel, ValidationError

try:
    from logzero import logger
except ImportError:
    import logging as logger


class Headers:
    def __init__(
        self,
        role=None,
        user_id=None,
        key=None,
        **kwargs,
    ):
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

    async def get(self, **params):
        try:
            if hasattr(self, "Params"):
                params = self.Params(**params).dict()
                params = parse.urlencode(params)

            headers = self.headers.dict()
            request_cfg = {"params": params, "headers": headers}

            async with self._cl.get(self.url, **request_cfg) as resp:
                if resp.status != 200:
                    msg = "Url=%s, API call unsuccesful => %s"
                    text = await resp.text()
                    logger.error(msg, self.url, text)
                    return self.on_failure(resp)

                json = await resp.json()

                if iscoroutinefunction(self.on_success):
                    return await self.on_success(json)

                return self.on_success(json)

        except ValidationError as err:
            logger.error("Url=%s, Invalid query-param: %s", self.url, err)
            return self.on_error(err)

        except Exception as err:
            logger.error("Url=%s, API call error: %s", self.url, err)
            return self.on_error(err)

    def on_failure(self, response):
        pass

    def on_error(self, error):
        pass

    def on_success(self, json_data):
        if hasattr(self, "Response"):
            return self.Response(**json_data)

        if hasattr(self, "response"):
            return self.response(**json_data)

        return json_data
