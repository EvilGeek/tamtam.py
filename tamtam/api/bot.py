import asyncio
import typing
import datetime

import aiohttp
import ujson

from .requests import Requester, UrlType

from ..urls import Urls
from ..types import (
    user,
    updates,
    chat,
    messages,
    subscription,
    chat_enums,
    uploads_enums,
)
from ..helpers import ctx


loop = asyncio.get_event_loop()


async def _open_file(
    file: str,
    mode,
    event_loop: asyncio.BaseEventLoop = None,
):
    return await (event_loop or loop).run_in_executor(None, open, file, mode)


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
        self.force_non_model_return = False
        self.open_file = _open_file

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

    async def edit_chat(self, chat_id: int, edit_chat: chat.EditChatInfo) -> chat.Chat:
        return await self.request(
            "PATCH",
            url=self.urls.get_chat(chat_id),
            json=edit_chat.json(),
            model=chat.Chat,
        )

    async def action(self, chat_id: int, action: chat_enums.ChatAction) -> typing.NoReturn:
        if chat_enums.ChatAction.has(action):
            action = action.value

        json = ujson.dumps({"action": action})

        await self.request.post(
            self.urls.send_action(chat_id),
            json=json,
        )

    async def get_membership(self, chat_id: int) -> chat.Membership:
        return await self.request.get(
            self.urls.membership(chat_id, "me"),
            model=chat.Membership,
        )

    async def leave_chat(self, chat_id: int) -> typing.NoReturn:
        await self.request.post(
            self.urls.membership(chat_id, "me"),
            model=chat.Membership,
        )

    async def get_admins(self, chat_id: int) -> chat.Admins:
        return await self.request.get(
            self.urls.membership(chat_id, "admins"),
            model=chat.Admins,
        )

    async def get_members(
        self,
        chat_id: int,
        users_ids: typing.List[int] = None,
        count: int = 20,
        marker: int = None
    ) -> chat.Members:
        return await self.request.get(
            self.urls.membership(chat_id, None),
            model=chat.Members,
            params={"users_ids": ",".join(map(str, users_ids) or ()), "marker": marker, "count": count}
        )

    async def add_members(self, chat_id: int, users_ids: typing.List[int]) -> typing.NoReturn:
        await self.request.post(
            self.urls.membership(chat_id, "me"),
            params={"users_ids": ",".join(map(str, users_ids) or ())}
        )

    async def remove_member(self, chat_id: int, user_id: int):
        await self.request(
            "DELETE",
            self.urls.membership(chat_id, None),
            params={"user_id": user_id},
        )

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
            self.urls.messages,
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

    async def edit_message(self, cfg: messages.EditMessageConfig) -> typing.List[updates.Message]:
        return await self.request(
            "PUT",
            self.urls.messages,
            params={
                "chat_id": cfg.chat_id,
                "message_ids": ",".join(map(str, cfg.message_ids) or ()),
                "from": cfg.from_,
                "to": cfg.to,
                "count": cfg.count,
            },
            models_in_list=True,
            model_from_key="messages",
            model=updates.Message,
        )

    async def delete_message(self, message_id: str):
        await self.request(
            "DELETE",
            self.urls.messages,
            params={"message_id": message_id}
        )

    async def answer_callback_query(
        self,
        callback_id: str,
        *,
        edit_message: messages.NewMessage = None,
        notification: str = None
    ) -> typing.NoReturn:

        json = {}
        if edit_message is not None:
            json["message"] = edit_message.json()
        if notification is not None:
            json["notification"] = notification

        json = ujson.dumps(json)

        await self.request.post(
            self.urls.answers,
            params={"callback_id": callback_id},
            json=json,
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

    async def subscribe(self, onfig: subscription.NewSubscriptionConfig) -> dict:
        tt_url = self.urls.subscriptions
        return await self.request.post(tt_url, json=config.json())

    async def unsubscribe(self, url: UrlType) -> dict:
        tt_url = self.urls.subscriptions
        return await self.request("DELETE", url=tt_url, params={"url": str(url)})

    async def make_attachments(
        self, *files: typing.Tuple[str, typing.Tuple[str, typing.Union[bytes, str]]]
    ) -> typing.List[int]:
        raise NotImplemented()

    async def get_upload_url(self, type_: uploads_enums.UploadTypes) -> str:
        return ((await self.request.post(
            self.urls.get_upload_url,
            params={"type": type_}
        )) or {}).get("url")

    async def upload(self, url: UrlType):
        # todo :D aiohttp.FormData
        ...

    async def __aenter__(self) -> "Bot":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.request.close()
