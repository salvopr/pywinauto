"""Module containing tests for linux clipboard module"""
import sys
import os
import unittest
import subprocess
import time

sys.path.append(".")
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
import mouse

send_keys_dir = os.path.join(parent_dir, r"linux")
sys.path.insert(0, send_keys_dir)
from pywinauto.keyboard import SendKeys, KeySequenceError, KeyAction
import clipboard

def _test_app():
    test_folder = os.path.join(os.path.dirname
                               (os.path.dirname
                                (os.path.dirname
                                 (os.path.abspath(__file__)))),
                               r"apps/SendKeysTester")
    return os.path.join(test_folder, r"send_keys_test_app")


class SendKeysTests(unittest.TestCase):
    """Unit tests for the linux clipboard module"""

    def setUp(self):
        """Start the application set some data and ensure the application is in the state we want it."""
        self.app = subprocess.Popen("exec " + _test_app(), shell=True)
        time.sleep(0.1)
        mouse.click(coords=(300, 300))
        time.sleep(0.1)

    def tearDown(self):
        """Close the application after tests"""
        self.app.kill()

    def receive_text(self):
        """Receive data from text field"""
        time.sleep(0.2)
        SendKeys('^a')
        time.sleep(0.2)
        SendKeys('^c')
        SendKeys('{RIGHT}')
        received = clipboard.get_data()
        return received

    def test_get_data(self):
        """Make sure that get text from clipboard works"""
        SendKeys('abc')
        received = self.receive_text()
        self.assertEquals('abc', received)

    def test_set_data(self):
        """Make sure that set text to clipboard works"""
        clipboard.set_data('abc1')
        received = clipboard.get_data()
        self.assertEquals('abc1', received)


if __name__ == "__main__":
    if sys.platform != 'win32':
        unittest.main()
