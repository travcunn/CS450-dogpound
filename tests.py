import os
import unittest
import tempfile

from app import app, db


class BaseTestCase(unittest.TestCase):
    """ Abstract base test class for this app. """
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])


class BaseLoginTestCase(BaseTestCase):
    """ Abstract test case for login testing. """

    def __init__(self, *args, **kwargs):
        super(BaseLoginTestCase, self).__init__(*args, **kwargs)

    def login(self, email, password):
        """ Login to the app. """
        return self.app.post('/login', data={'email': email,
                                             'password': password},
                             follow_redirects=True)

    def logout(self):
        """ Logout from the app. """
        return self.app.get('/logout', follow_redirects=True)

    def tearDown(self):
        self.logout()
        super(BaseLoginTestCase, self).tearDown()


class LoginTestCase(BaseLoginTestCase):
    """ Tests related to logging in and logging out. """

    def test_invalid_email(self):
        """ Test an invalid email address. """
        response = self.login('invaliduser', 'notfound')
        assert 'Invalid Login' in response.data

    def test_blank_email(self):
        """ Test a blank email address. """
        response = self.login('', 'notfound')
        assert 'This field is required' in response.data

    def test_invalid_password(self):
        """ Test an invalid password with a valid email. """
        response = self.login('vader@deathstar.com', 'default')
        assert 'Invalid Login' in response.data

    def test_blank_password(self):
        """ Test a blank password with a valid email. """
        response = self.login('vader@deathstar.com', '')
        assert 'This field is required' in response.data

    def test_valid_login(self):
        """ Test a valid email and a valid password. """
        response = self.login('vader@deathstar.com', 'noarms')
        assert 'Home - dogpound' in response.data


class UnauthenticatedViewTestCase(BaseTestCase):
    """
    Tests related to checking that unauthenticated users cannot access
    protected resources without logging in first.
    """
    def test_stream_view(self):
        """ Test accessing the stream view without being logged in. """
        response = self.app.get('/index', follow_redirects=True)
        assert 'Welcome to dogpound' in response.data


if __name__ == '__main__':
    unittest.main()
