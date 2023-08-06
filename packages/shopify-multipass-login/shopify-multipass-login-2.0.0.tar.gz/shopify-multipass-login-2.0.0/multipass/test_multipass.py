from multipass import Multipass

import unittest
from  urllib.parse import urlparse

class MultipassTestCase(unittest.TestCase):

    base_url = 'https://store.example.com'

    def test_multipass(self):
        user = {
            'email': 'test@example.com',
            'first_name': 'first',
            'last_name': 'last',
            'identifier': '12345'
        }

        multipass = Multipass('secret')
        url = multipass.generateURL(user, self.base_url)
        self.assertTrue(url.startswith(self.base_url))
        token = urlparse(url).path.split('/')[-1]
        self.assertTrue(len(token) > 50)
