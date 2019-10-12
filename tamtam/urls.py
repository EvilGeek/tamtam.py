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
    send_action: typing.Callable[["Urls", int], URL] = lambda self, chat_id: URL(
        self.get_chat(chat_id) + "actions"
    )
    membership: typing.Callable[["Urls", int], URL] = lambda self, chat_id, who: URL(
        self.get_chat(chat_id) + "members" + ("/" + str(who) if who else None)
    )

    messages: URL = base.with_path("messages")
    """base_endpoint/messages"""

    send_message: URL = messages
    """base_endpoint/messages"""

    answers: URL = base.with_path("answers")
    """base_endpoint/answers"""

    updates: URL = base.with_path("updates")
    """base_endpoint/updates"""

    get_upload_url: URL = base.with_path("uploads")
    """base_endpoint/uploads"""

    subscriptions: URL = base.with_path("subscriptions")
    """base_endpoint/subscriptions"""
