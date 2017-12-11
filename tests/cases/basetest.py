import unittest
import hexdi


class BaseHexDITest(unittest.TestCase):
    def setUp(self):
        self.container = hexdi.get_root_container()

    def tearDown(self):
        self.container.destroy()
        del self.container
