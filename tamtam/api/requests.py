import typing
import logging

import aiohttp
import pydantic
from yarl import URL

from .exceptions import JsonParsingError, BaseWrapperError
from ..helpers.ctx import ContextInstanceMixin

logger = logging.getLogger(__name__)

UrlType = typing.Union[str, URL]


def params_filter(dictionary: dict):
    """
    Pop NoneType values and convert everything to str, designed?for=params
    :param dictionary: source dict
    :return: filtered dict
    """
    return (
        {k: str(v) for k, v in dictionary.items() if v is not None}
        if dictionary
        else {}
    )


class Requester(ContextInstanceMixin):
    def __init__(self, session: aiohttp.ClientSession, default_params: dict = None):
        self._session = session
        self.params = params_filter(default_params or {})

    async def __call__(
        self,
        http_method: str,
        url: UrlType,
        *,
        params: dict = None,
        json: str = None,
        model=None,
        models_in_list: bool = None,
        model_from_key: str = None,
        extra_key: str = None,
    ):
        async with self._session.request(
            http_method,
            url.__str__(),
            params={**self.params, **params_filter(params)},
            data=json,
        ) as response:

            try:
                response_json = await response.json()
                logger.info(
                    f"Sent [{http_method}] to {url!s} [model: {model!r}|data: {json!s}]\t"
                    f"Got  {response_json}"
                )

            except ValueError as exc:
                logger.error(exc, exc_info=True)
                raise JsonParsingError()

            if all(k in response_json for k in ("code", "message")):
                logger.error(response_json)
                raise BaseWrapperError(response_json)

            if model:
                try:
                    if model_from_key:
                        if models_in_list:
                            ret = [
                                model(**rjs)
                                for rjs in response_json.get(model_from_key)
                            ]
                        else:
                            ret = model(**(response_json.get(model_from_key)))
                    elif models_in_list:
                        ret = [model(**rjs) for rjs in response_json]
                    else:
                        ret = model(**response_json)

                except pydantic.ValidationError as exc:
                    logger.error(exc, exc_info=True)
                    raise JsonParsingError()

                if extra_key:
                    return ret, response_json.get(extra_key)
                return ret

            return response_json

    async def get(self, url: UrlType, params: dict = None, **kwargs):
        return await self("GET", url, params=params, **kwargs)

    async def post(self, url: UrlType, params: dict = None, json: str = None, **kwargs):
        return await self("POST", url, params=params, json=json, **kwargs)

    async def close(self):
        await self._session.close()
