# TODO: Write tests!

import sys
import requests

from django.test import TestCase

class TestLoginAsTheOSF(TestCase):

    def test_login_as_the_osf(self):
        url = 'http://localhost:8000/accounts/login/'
        client = requests.session()

        # Retrieve the CSRF token first
        client.get(url)  # sets cookie
        csrftoken = client.cookies['csrftoken']

        USERNAME = 'osf'
        PASSWORD = 'a very secret password'

        login_data = dict(username=USERNAME, password=PASSWORD, csrfmiddlewaretoken=csrftoken)
        r = client.post(url, data=login_data, headers=dict(Referer=url))
        self.assertEqual(r.status_code, 200)