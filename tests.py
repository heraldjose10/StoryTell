import unittest
from blogApp import create_app, db
from blogApp.models import Tags, Authors, Blogs
from config import Config


class TestConfig(Config):
    """Class with configurations for testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class DataBaseTest(unittest.TestCase):

    def setUp(self):
        """function to create database and app context for testing"""
        self.app = create_app(config_class=TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()  # push app context to current context
        db.create_all()

    def tearDown(self):
        """deletes testing database and app context"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def testRegisterUser(self):
        """Create two users and test adding them to database"""
        user1 = Authors(name='UserOne', email='user1@mail.com')
        user1.set_password('user1')
        user2 = Authors(name='UserTwo', email='user2@mail.com')
        user2.set_password('user2')

        db.session.add(user1)
        db.session.add(user2)

        self.assertEqual(user1.name, 'UserOne')
        self.assertEqual(user2.email, 'user2@mail.com')

    def testPassword(self):
        """Test hashing of password"""
        user1 = Authors(name='UserOne', email='user1@mail.com')
        user1.set_password('user1')

        self.assertNotEqual(user1.password, 'user1')
        self.assertFalse(user1.check_password('1234'))
        self.assertTrue(user1.check_password('user1'))

    def testBlogWriting(self):
        """Test adding blog to database and adding tags to blog"""
        user1 = Authors(name='UserOne', email='user1@mail.com')
        user1.set_password('user1')

        b = Blogs(title='Blog One',
                  content='ahga ajfaf ahfaiuhf aiufhauf aufhau', author=user1)

        t1 = Tags(name='tag1')
        t2 = Tags(name='tag2')
        t1.blogs.append(b)
        t2.blogs.append(b)

        self.assertEqual(len(b.tags), 2)
        self.assertEqual(b.author.name, 'UserOne')


if __name__ == '__main__':
    unittest.main(verbosity=2)
