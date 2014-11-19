import os
import random
import string
import tempfile
import unittest

from app import app, db
from app.models import Bark, Friendship, User
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)


TEST_USERS = User.query.all()


def random_string(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))


class BaseTestCase(unittest.TestCase):
    """
    Abstract base test class for this app.
    """
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])


class BaseLoginTestCase(BaseTestCase):
    """
    Abstract test case for login testing.
    """
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
        
    def register(self, firstName, lastName, email, password, password2):
        """ Register user. """
        return self.app.post('/registration', data={'firstName': firstName,
        									'lastName': lastName,
        									'email': email,
        									'password': password},
                             follow_redirects=True)

    def tearDown(self):
        # logout after running all tests
        self.logout()
        super(BaseLoginTestCase, self).tearDown()


class BaseAuthenticatedTestCase(BaseLoginTestCase):
    """
    Base test case for testing authenticated views.
    """
    def setUp(self):
        super(BaseAuthenticatedTestCase, self).setUp()
        pw_hash = bcrypt.generate_password_hash('noarms')
        self.login('vader@deathstar.com', pw_hash)

    def tearDown(self):
        # Delete all barks
        Bark.query.delete()
        # Delete all friendships
        Friendship.query.delete()

        db.session.commit()

        super(BaseAuthenticatedTestCase, self).setUp()


class UnauthenticatedViewTestCase(BaseTestCase):
    """
    Tests related to checking that unauthenticated users cannot access
    protected resources without logging in first.
    """
    def test_stream_view(self):
        """ Test accessing the stream view without being logged in. """
        response = self.app.get('/index', follow_redirects=True)
        assert 'Home - dogpound' in response.data


class LoginTestCase(BaseLoginTestCase):
    """
    Tests related to logging in and logging out.
    """
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
#         pw_hash = bcrypt.generate_password_hash('')
        response = self.login('vader@deathstar.com', '')
        assert 'This field is required' in response.data

    def test_valid_login(self):
        """ Test a valid email and a valid password. """
        response = self.login('vader@deathstar.com', 'noarms')
        assert 'Home - dogpound' in response.data

class RegistrationTestCase(BaseLoginTestCase):
    """
    Tests related to Registration.
    """

    def test_blank_firstName(self):
        """ Test a blank first name with all others valid. """
        response = self.register('', 'TestLast', 'test@email.com', 'test', 'test')
        assert 'This field is required' in response.data
        
    def test_blank_lastName(self):
        """ Test a blank last name with all others valid. """
        response = self.register('TestFirst', '', 'test@email.com', 'test', 'test')
        assert 'This field is required' in response.data
    
	def test_blank_email(self):
		""" Test a blank email with all others valid. """
        response = self.register('TestFirst', 'TestLast', '', 'test', 'test')
        assert 'This field is required' in response.data
     
    def test_blank_password1(self):
        """ Test a blank password1 with all others valid. """
        response = self.register('TestFirst', 'TestLast', 'test@email.com', '', 'test')
        assert 'This field is required' in response.data
        
    def test_blank_password2(self):
        """ Test a blank retyped password with all others valid. """
        response = self.register('TestFirst', 'TestLast', 'test@email.com', 'test', '')
        assert 'This field is required' in response.data   
        
#     def test_unmatched_passwords(self):
#         """ Test unmatched passwords with all others valid. """
#         response = self.register('TestFirst', 'TestLast', 'test@email.com', 'test1', 'test')
#         assert 'Passwords must match' in response.data
    

class BaseBarkTestCase(BaseAuthenticatedTestCase):
    """
    Tests related to the stream view.
    """
    def create_bark(self, body):
        """ Create a new bark given a content body. """
        return self.app.post('/index', data={'barkBody': body},
                             follow_redirects=True)


class CreateBarkTestCase(BaseBarkTestCase):
    def test_create_single_bark(self):
        """ Test creation of a new bark. """
        body = random_string(15)
        self.create_bark(body)

        response = self.app.get('/index', follow_redirects=True)
        assert body in response.data

    def test_create_multiple_barks(self):
        """ Test creation of multiple barks. """
        amount = 10

        contents = [random_string(15) for x in range(amount)]
        for content in contents:
            self.create_bark(content)

        response = self.app.get('/index', follow_redirects=True)
        for content in contents:
            assert content in response.data


class ViewBarkTestCase(BaseBarkTestCase):
    def test_view_only_friends_barks(self):
        """ Test that the stream contains only friend's barks. """
        user1, user1_content = TEST_USERS[0], "hello world"
        user2, user2_content = TEST_USERS[1], "world hello"
        user3, user3_content = TEST_USERS[2], "whats up?"

        # Add user2 to user1's friends
        friendship = Friendship()
        friendship.user_id = user1.id
        friendship.friend_id = user2.id
        db.session.add(friendship)
        db.session.commit()

        # Create barks from all 3 users
        self.logout()
        self.login(user1.email, user1.password)
        self.create_bark(user1_content)
        self.logout()
        self.login(user2.email, user2.password)
        self.create_bark(user2_content)
        self.logout()
        self.login(user3.email, user3.password)
        self.create_bark(user3_content)
        self.logout()

        # View stream as user 1
        self.login(user1.email, user1.password)
        response = self.app.get('/index', follow_redirects=True)

        assert user1_content in response.data
        assert user2_content in response.data
        assert user3_content not in response.data


if __name__ == '__main__':
    unittest.main()
