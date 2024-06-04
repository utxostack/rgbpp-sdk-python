from unittest import TestCase
from .rpc import rpc

class TestRpc(TestCase):
    def test_get_version(self):
        self.assertEqual(rpc.get_version(), "0.0.1")

