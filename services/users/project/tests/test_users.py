import json
import unittest

from base import BaseTestCase
from project.api.models import User

from project import db


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUsersService(BaseTestCase):
    # Tests for the users service

    def test_users(self):
        # Ensure the /ping route behaves correctly.
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'test',
                    'email': 'test@gmail.com'
                }),
                content_type='application/json',
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('test@gmail.com was added', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'soyese@gmail'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'yo',
                    'email': 'soyese@gmail.com'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'yo',
                    'email': 'soyese@gmail.com'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry, email is already taken', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_single_user(self):
        user = add_user('yo', 'soyese@gmail.com')

        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('yo', data['data']['username'])
            self.assertIn('soyese@gmail.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_user_no_id(self):
        with self.client:
            response = self.client.get('/users/any_id')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid user id provided', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_wrong_id(self):
        with self.client:
            response = self.client.get('/users/0000')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        add_user('Yo', 'soyese@gmail.com')
        add_user('Tu', 'nosoyese@gmail.com')

        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('Yo', data['data']['users'][0]['username'])
            self.assertIn('soyese@gmail.com', data['data']['users'][0]['email'])
            self.assertIn('Tu', data['data']['users'][1]['username'])
            self.assertIn('nosoyese@gmail.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)
        self.assertIn(b'<p>No users</p>', response.data)

    def test_main_with_users(self):
        add_user('leo', 'leo@gmail.com')
        add_user('oel', 'oel@gmail.com')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users</p>', response.data)
            self.assertIn(b'leo', response.data)
            self.assertIn(b'oel', response.data)

    def test_main_add_user(self):
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='leo', email='leo@gmail.com'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertNotIn(b'<p>No users</p>', response.data)
            self.assertIn(b'leo', response.data)


if __name__ == '__main__':
    unittest.main()
