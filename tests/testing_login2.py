from application.login.login import UserLogin
from databases.mysql_connect import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD
import pymysql
import unittest

class TestUserLogin:
    def setup_method(self):
        self.connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        self.login = UserLogin(self.connection)

    def teardown_method(self):
        self.connection.close()

    # Test valid login
    def test_valid_login(self):
        # Mocking the user input for testing purposes
        self.login.user_log_in = lambda: "valid_username"
        user_id = self.login.user_auth()[0]
        assert user_id is not None

    # Test invalid login
    def test_invalid_login(self):
        # Mocking the user input for testing purposes
        self.login.user_log_in = lambda: "invalid_username"
        user_id = self.login.user_auth()[0]
        assert user_id is None

    # Test corner case: creating a new user with an existing username
    def test_create_existing_user(self):
        # Mocking the user input for testing purposes
        self.login.create_new_user = lambda: "existing_username"
        user_id = self.login.user_auth()[0]
        assert user_id is None

if __name__ == "__main__":
    unittest.main()