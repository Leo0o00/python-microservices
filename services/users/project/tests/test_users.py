import json
import unittest

from base import BaseTestCase


class TestUsersService(BaseTestCase):
    # Tests for the users service

    def test_users(self):
        # Ensure the /ping route behaves correctly.
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])


if __name__ == '__main__':
    unittest.main()
