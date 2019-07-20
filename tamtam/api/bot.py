import typing
import datetime

import aiohttp

from .requests import Requester, UrlType

from ..urls import Urls
from ..types import user, updates, chat, messages, subscription
from ..helpers import ctx


TTPFType = typing.Tuple[bytes, str]  # (file, file_type)


class Bot(ctx.ContextInstanceMixin):
    def __init__(
        self, token: str, timeout: int = 60, _session: aiohttp.ClientSession = None
    ):
        """

        :param token:
        :param timeout:
        :param _session:
        """
        timeout = aiohttp.ClientTimeout(total=timeout + 1) if timeout else None
        self.request = Requester(
            aiohttp.client.ClientSession(timeout=timeout),
            default_params={"access_token": token},
        )

        self.set_current(self)
        self.urls = Urls()

        self.__polling = False

    # me zone
    async def get_me(self) -> user.User:
        """

        :return:
        """
        return await self.request.get(self.urls.get_me, model=user.User)

    async def set_me(self, info: user.BotInfoSetter):
        """

        :param info:
        :return:
        """
        return await self.request(
            "patch",
            self.urls.set_me,
            model=user.User,
            json=info.json(skip_defaults=True),
        )

    # chats
    async def get_chats(self, lim: int = 50, marker: int = None) -> chat.Chats:
        """

        :param lim:
        :param marker:
        :return:
        """
        return await self.request.get(
            self.urls.get_chats,
            model=chat.Chats,
            params={"count": lim, "marker": marker},
        )

    async def get_chat(self, chat_id: int) -> chat.Chat:
        """

        :param chat_id:
        :return:
        """
        return await self.request.get(self.urls.get_chat(chat_id), model=chat.Chat)

    # messages
    async def get_messages(
        self,
        chat_id: int = None,
        messages_ids: typing.Optional[typing.List[int]] = None,
        from_date: typing.Optional[datetime.datetime] = None,
        to_date: typing.Optional[datetime.datetime] = None,
        lim: int = None,
    ) -> typing.List[updates.Message]:
        """

        :param chat_id:
        :param messages_ids:
        :param from_date:
        :param to_date:
        :param lim:
        :return:
        """
        return await self.request.get(
            self.urls.get_messages,
            params={
                "chat_id": chat_id,
                "messages_ids": messages_ids,
                "from": from_date.timestamp().__int__()
                if isinstance(from_date, datetime.datetime)
                else None,
                "to": to_date.timestamp().__int__()
                if isinstance(to_date, datetime.datetime)
                else None,
                "count": lim,
            },
            models_in_list=True,
            model_from_key="messages",
        )

    async def send_message(
        self, body: messages.NewMessage, *, chat_id: int = None, user_id: int = None
    ) -> updates.Message:
        """

        :param body:
        :param chat_id:
        :param user_id:
        :return:
        """
        return await self.request.post(
            self.urls.send_message,
            params={"chat_id": chat_id, "user_id": user_id},
            json=body.json(),
            model=updates.Message,
            model_from_key="message",
        )

    async def get_updates(
        self,
        lim: int,
        timeout: int,
        marker: int,
        update_types: typing.Optional[str],
        ignore_old_updates: bool,
    ) -> typing.Tuple[typing.List[updates.Update], int]:
        """
        Get Updates
        :param lim: get updates limit
        :param timeout: timeout
        :param marker: last update marker
        :param update_types: comma separated update types from UpdatesEnum
        :param ignore_old_updates: ignore pending updates
        :return:
        """
        return await self.request.get(
            self.urls.updates,
            params={
                "limit": lim,
                "timeout": timeout,
                "marker": marker if not ignore_old_updates else -1,
                "types": ",".join(update_types or []),
            },
            model_from_key="updates",
            models_in_list=True,
            model=updates.Update,
            extra_key="marker",
        )

    async def subscriptions(self) -> typing.List[subscription.Subscription]:
        tt_url = self.urls.subscriptions
        return await self.request.get(
            tt_url,
            model_from_key="subscriptions",
            models_in_list=True,
            model=subscription.Subscription,
        )

    async def subscribe(self, config: subscription.NewSubscriptionConfig) -> dict:
        tt_url = self.urls.subscriptions
        return await self.request.post(tt_url, json=config.json())

    async def unsubscribe(self, url: UrlType) -> dict:
        tt_url = self.urls.subscriptions
        return await self.request("DELETE", url=tt_url, params={"url": str(url)})

    async def make_attachments(
        self, files: typing.Union[typing.List[TTPFType], TTPFType, UrlType]
    ) -> typing.List[int]:
        # todo make user-friendly files uploading [!will behave very slow!]
        files = files if isinstance(files, list) else [files]

        attachments = []
        url_attachments = list(filter(lambda nt: isinstance(nt, str), files))
        file_like_objects = filter(lambda nt: isinstance(nt, tuple), files)

        for file, file_type in file_like_objects:
            attachments.append(
                await self.request.make_file_token(
                    self.urls.get_upload_url, file, file_type
                )
            )

        attachments.extend(url_attachments)
        return attachments

    async def __aenter__(self) -> "Bot":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.request.close()
