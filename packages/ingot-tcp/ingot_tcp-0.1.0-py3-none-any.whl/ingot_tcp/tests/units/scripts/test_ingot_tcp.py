import typing as t
from unittest import TestCase

from ingots.tests.units.scripts.test_base import BaseDispatcherTestsMixin

from ingot_tcp.scripts.ingot_tcp import IngotTcpDispatcher

__all__ = ("IngotTcpDispatcherTestsMixin",)


class IngotTcpDispatcherTestsMixin(BaseDispatcherTestsMixin):
    """Contains tests for the IngotTcpDispatcher class and checks it."""

    tst_cls: t.Type = IngotTcpDispatcher
    tst_builder_name = "test"


class IngotTcpDispatcherTestCase(IngotTcpDispatcherTestsMixin, TestCase):
    """Checks the IngotTcp class."""
