import asyncio
from typing import Any, cast, Dict, Set, Tuple
import urllib

import aioredis
from terminado import NamedTermManager, TermSocket
import tornado.web

from anyscale.webterminal.utils import write_zshrc


class AnyscaleTermManager(NamedTermManager):  # type: ignore
    def __init__(self, **kwargs: Any) -> None:
        super(AnyscaleTermManager, self).__init__(**kwargs)
        # For each terminal, record if it is a debug terminal
        # (keyed by terminal name).
        self.is_debugger: Dict[str, bool] = {}

    def get_terminal(self, term_name: str, is_debugger: bool = False) -> Any:
        terminal = super(AnyscaleTermManager, self).get_terminal(term_name)
        self.is_debugger[term_name] = is_debugger
        return terminal

    def new_named_terminal(self, **kwargs: Any) -> Tuple[str, Any]:
        name, term = super(AnyscaleTermManager, self).new_named_terminal(**kwargs)
        self.is_debugger[name] = False
        return name, term


class AnyscaleTermSocket(TermSocket):  # type: ignore
    def check_origin(self, origin: Any) -> bool:
        parsed_origin = urllib.parse.urlparse(origin)
        if self.application.settings["deploy_environment"] == "development":
            return True
        elif self.application.settings["deploy_environment"] == "staging":
            return cast(bool, parsed_origin.netloc.endswith("anyscale.dev"))
        else:
            return cast(bool, parsed_origin.netloc.endswith("beta.anyscale.com"))


class TerminalPageHandler(tornado.web.RequestHandler):
    """Render the /ttyX pages"""

    def delete(self, term_name: str) -> None:
        term_manager = self.application.settings["term_manager"]

        term_manager.kill(term_name)
        del term_manager.terminals[term_name]


class TerminalListHandler(tornado.web.RequestHandler):
    """List active terminals."""

    def get(self) -> None:
        term_manager = self.application.settings["term_manager"]

        data = {
            "terminals": [
                {"id": term_name, "debugger": term_manager.is_debugger[term_name]}
                for term_name in term_manager.terminals.keys()
            ]
        }

        self.write(data)


class NewTerminalHandler(tornado.web.RequestHandler):
    """Create new unused terminal"""

    def get(self) -> None:
        self.application.settings["term_manager"].new_named_terminal()


def make_application(deploy_environment: str, cwd: str) -> tornado.web.Application:
    term_manager = AnyscaleTermManager(
        shell_command=["bash"], max_terminals=100, term_settings={"cwd": cwd}
    )
    handlers: Any = [
        (
            r"/webterminal/_websocket/(\w+)",
            AnyscaleTermSocket,
            {"term_manager": term_manager},
        ),
        (r"/webterminal/new/?", NewTerminalHandler),
        (r"/webterminal/list", TerminalListHandler),
        (r"/webterminal/(\w+)/?", TerminalPageHandler),
    ]
    return tornado.web.Application(
        handlers, term_manager=term_manager, deploy_environment=deploy_environment,
    )


async def initialize_debugger(application: Any) -> None:
    redis_client = await aioredis.create_redis_pool(
        ("localhost", 6379), password="5241590000000000", encoding="utf-8"
    )

    ray_version = await redis_client.execute("get", b"VERSION_INFO")
    print("Starting debugger backend, Ray version is {}".format(ray_version))

    registered_breakpoints: Set[str] = set()

    while True:
        keys = await redis_client.keys(b"RAY_PDB_*")

        new_breakpoints = set(keys) - registered_breakpoints

        if len(new_breakpoints) > 0:
            print("new breakpoints", new_breakpoints)

        for new_breakpoint in new_breakpoints:
            term_manager = application.settings["term_manager"]
            debugger = term_manager.get_terminal(new_breakpoint, is_debugger=True)
            debugger.ptyproc.write("ray debug\n")

        registered_breakpoints = registered_breakpoints.union(new_breakpoints)

        await asyncio.sleep(1.0)


def main(
    deploy_environment: str,
    use_debugger: bool,
    cli_token: str,
    host: str,
    working_dir: str,
) -> None:
    # Write the .zshrc file before starting the server.
    write_zshrc()
    application = make_application(deploy_environment, working_dir)
    port = 8700
    application.listen(port, "localhost")
    print("Listening on localhost:{}".format(port))
    loop = tornado.ioloop.IOLoop.instance()

    if use_debugger:
        loop.run_sync(lambda: initialize_debugger(application))

    try:
        loop.start()
    except KeyboardInterrupt:
        print(" Shutting down on SIGINT")
    finally:
        application.settings["term_manager"].shutdown()
        loop.close()
