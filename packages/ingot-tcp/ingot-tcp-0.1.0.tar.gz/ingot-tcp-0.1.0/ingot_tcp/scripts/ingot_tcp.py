import typing as t
from logging import getLogger
from logging import INFO

from ingots.scripts.base import BaseDispatcher
from ingots.utils.logging import configure_startup_logging

if t.TYPE_CHECKING:
    from ingots.bootstrap.builders import BaseBuilder  # noqa


__all__ = (
    "IngotTcpDispatcher",
    "main",
)


configure_startup_logging(
    default_level=INFO,
    format="%(levelname)s: %(message)s",
)
logger = getLogger(__name__)


class IngotTcpDispatcher(BaseDispatcher):

    prog = "ingot_tcp"
    description = "The Ingot Tcp skeletons generation management CLI."
    skeletons_builders_classes: t.List[t.Type["BaseBuilder"]] = []


def main():
    dispatcher = IngotTcpDispatcher.build()
    dispatcher.run()


if __name__ == "__main__":
    main()
