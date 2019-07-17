import typing
import logging
import ipaddress

from aiohttp import web

from tamtam.types.updates import Update

logger = logging.getLogger("tamtam:server")

DEFAULT_TAMTAM_ROUTER_NAME = "tamtamsubs"
DEFAULT_TAMTAM_SUBS_WEBHOOK_PATH = "tamtamwebhooks/"
TAMTAM_ALLOWED_PORTS = (80, 8080, 443, 8443, *range(16384, 32383 + 1))
DEFAULT_TAMTAM_PORT = 8443

allowed_ips = set()


class TTSubsView(web.View):
    def validate_ip(self):
        # pulled from aioqiwi
        checker = self.request.app.get("_check_ip")
        if checker:
            ip, accepted = self.check_ip(checker)
            if not accepted:
                logger.warning(f"{ip} is not listed as allowed IP")
                raise web.HTTPUnauthorized()

    def check_ip(self, checker_callback: typing.Callable[[str], bool]):
        forwarded_for = self.request.headers.get("X-Forwarded-For")

        if forwarded_for:
            return forwarded_for, checker_callback(forwarded_for)

        peer_name = self.request.transport.get_extra_info("peername")

        if peer_name is not None:
            host, _ = peer_name
            return host, checker_callback(host)

        logger.info("Failed to get IP-address")
        return None, False

    async def post(self):
        """
        Process POST request with validating, further deserialization and resolving BASE

        REQUIRES: BINDING DISPATCHER
        """
        # todo IP-validation by simply calling validate ip

        await self.request.app["_dispatcher"].process_events(await self.parse_updates())
        return web.Response(text="ok")

    async def parse_updates(self) -> typing.List[Update]:
        try:
            updates = (await self.request.json()).get("updates")
            return [Update(**update) for update in updates]
        except ValueError:
            logger.exception(f"Cannot deserialize server-request {await self.request.read()}")


def _check_ip(ip: str) -> bool:
    address = ipaddress.IPv4Address(ip)
    return address in allowed_ips


def allow_ip(*ips_like: typing.Union[str, ipaddress.IPv4Network, ipaddress.IPv4Address]):
    for ip in ips_like:
        if isinstance(ip, ipaddress.IPv4Address):
            allowed_ips.add(ip)
        elif isinstance(ip, str):
            allowed_ips.add(ipaddress.IPv4Address(ip))
        elif isinstance(ip, ipaddress.IPv4Network):
            allowed_ips.update(ip.hosts())
        else:
            raise ValueError("Ensure you're passing right IP(address|network)")

        logger.info(f"Added new ip(hosts|host) {ip}")


allow_ip()


def _setup(dispatcher, app: web.Application, path=None):
    app["_check_ip"] = _check_ip
    app["_dispatcher"] = dispatcher

    app.router.add_view(
        path or DEFAULT_TAMTAM_SUBS_WEBHOOK_PATH,
        TTSubsView,
        name=DEFAULT_TAMTAM_ROUTER_NAME,
    )


def run_app(
    dispatcher,
    host:            str = None,
    port:            int = None,
    path:            str = None,
    app: web.Application = None
):

    app = app or web.Application()

    _setup(
        dispatcher=dispatcher,
        app=app or web.Application(),
        path=path or DEFAULT_TAMTAM_SUBS_WEBHOOK_PATH
    )

    web.run_app(
        app=app,
        host=host or "localhost",
        port=port or DEFAULT_TAMTAM_PORT
    )
