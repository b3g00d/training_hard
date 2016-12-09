#!/usr/bin/env python3
import mock
import unittest
from mock_ import rm


class RmTestCase(unittest.TestCase):

    @mock.patch('mock_.os.path')
    @mock.patch('mock_.os')
    def test_rm(self, mock_os, mock_path):
        mock_path.isfile.return_value = False

        rm("/home/begood/Downloads/CTF/irc.py")
        self.assertFalse(mock_os.remove.called, "Failed to not remove the"
                         "file if not prsent.")
        mock_path.isfile.return_value = True

        rm("any asdpath")

        mock_os.remove.assert_called_with("any asdpath")

if __name__ == '__main__':
    unittest.main()
