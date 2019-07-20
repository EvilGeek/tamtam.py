import typing
import logging
import ipaddress

from aiohttp import web

from tamtam.types.updates import Update

logger = logging.getLogger("tamtam:server")

DEFAULT_TAMTAM_ROUTER_NAME = "tamtamsubs"
DEFAULT_TAMTAM_SUBS_WEBHOOK_PATH = "tamtamwebhooks/"

TAMTAM_NETWORKS = [
    ipaddress.IPv4Network("185.16.150.0/30"),
    ipaddress.IPv4Network("185.16.150.84/30"),
    ipaddress.IPv4Network("185.16.150.152/30"),
    ipaddress.IPv4Network("185.16.150.192/30"),
]

TAMTAM_ALLOWED_PORTS = (80, 8080, 443, 8443, *range(16384, 32383 + 1))
DEFAULT_TAMTAM_SUBS_PORT = 8484

allowed_ips: typing.Set[
    typing.Union[ipaddress.IPv4Network, ipaddress.IPv4Address]
] = set()


class TTSubsView(web.View):
    def validate_ip(self) -> typing.NoReturn:
        checker = self.request.app.get("_check_ip")
        if checker:
            ip, accepted = self.check_ip(checker)
            if not accepted:
                logger.warning(f"{ip} is not listed as allowed IP so denying access")
                return web.HTTPBadRequest()

    def check_ip(
        self, checker_callback: typing.Callable[[str], bool]
    ) -> typing.Tuple[typing.Optional[str], bool]:
        forwarded_for = self.request.headers.get("X-Forwarded-For")

        if forwarded_for:
            return forwarded_for, checker_callback(forwarded_for)

        peer_name = self.request.transport.get_extra_info("peername")

        if peer_name is not None:
            host, _ = peer_name
            return host, checker_callback(host)

        logger.info("Failed to get IP-address")
        return None, False

    async def post(self) -> web.Response:
        """
        Process POST request with validating, further deserialization and resolving BASE

        REQUIRES: BINDING DISPATCHER
        """

        self.validate_ip()

        await self.request.app["_dispatcher"].process_events(
            [await self.parse_update()]
        )
        return web.Response(text="ok")

    async def parse_update(self) -> Update:
        try:
            return Update(**(await (self.request.json())))
        except ValueError:
            logger.exception(
                f"Cannot deserialize server-request {await self.request.read()}"
            )


def _check_ip(ip: str) -> bool:
    address = ipaddress.IPv4Address(ip)
    return address in allowed_ips


def allow_ip(
    *ips_like: typing.Union[str, ipaddress.IPv4Network, ipaddress.IPv4Address]
):
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


def _setup(dispatcher, app: web.Application, path=None) -> typing.NoReturn:
    allow_ip(*TAMTAM_NETWORKS)

    app["_check_ip"] = _check_ip
    app["_dispatcher"] = dispatcher

    app.router.add_view(
        path or DEFAULT_TAMTAM_SUBS_WEBHOOK_PATH,
        TTSubsView,
        name=DEFAULT_TAMTAM_ROUTER_NAME,
    )


def run_app(
    dispatcher,
    app: web.Application = None,
    host: str = None,
    port: int = None,
    path: str = None,
) -> typing.NoReturn:

    if port is not None and port not in TAMTAM_ALLOWED_PORTS:
        raise RuntimeError(
            f"Port must be either in None to set default DEFAULT_TAMTAM_SUBS_PORT={DEFAULT_TAMTAM_SUBS_PORT}"
            f", either in {', '.join(map(str, TAMTAM_ALLOWED_PORTS))}"
        )

    if not isinstance(app, web.Application):
        app = web.Application()

    _setup(
        dispatcher=dispatcher, app=app, path=path or DEFAULT_TAMTAM_SUBS_WEBHOOK_PATH
    )

    web.run_app(
        app=app, host=host or "localhost", port=port or DEFAULT_TAMTAM_SUBS_PORT
    )
