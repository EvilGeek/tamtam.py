import typing

from yarl import URL

BASE = "https://botapi.tamtam.chat"


class Urls:
    base: URL = URL(BASE)
    """base_endpoint"""

    get_me: URL = base.with_path("me")
    """base_endpoint/me"""
    set_me: URL = get_me
    """base_endpoint/me"""

    get_chats: URL = base.with_path("chats")
    """base_endpoint/chats"""
    get_chat: typing.Callable[["Urls", int], URL] = lambda self, chat_id: URL(
        str(self.get_chats) + str(chat_id) + "/"
    )
    """base_endpoint/chats/chat_id/"""

    get_messages: URL = base.with_path("messages")
    """base_endpoint/messages"""

    send_message: URL = get_messages
    """base_endpoint/messages"""

    updates: URL = base.with_path("updates")
    """base_endpoint/updates"""
