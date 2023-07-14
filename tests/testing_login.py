import unittest
from unittest.mock import patch, Mock, MagicMock
from application.login.login import UserLogin
import io

class TestUserLogin(unittest.TestCase):

    # Setting up the object for the tests
    def setUp(self):
        self.connection = Mock()
        self.user_login = UserLogin(self.connection)

    # Test to ensure that the initialise_user_auth function correctly handles invalid input,
    # prompts the user to input a valid choice again, and then correctly returns that valid input.
    # This decorator replaces the standard 'input' function with a mock function for the duration of the test.
    # The 'side_effect' parameter provides the sequence of responses ('3' and '1') the mock function will give when called.
    @patch('builtins.input', side_effect=['3', '1'])
    def test_initialise_user_auth_invalid_choice_then_valid(self, mock_input):
        # This context manager replaces 'sys.stdout', which is responsible for handling print statements,
        # with an instance of 'io.StringIO', which stores the printed text in a string buffer.
        # The buffer can later be accessed via 'fake_out.getvalue()'.
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            # Call the 'initialise_user_auth' function, which is now using the mock 'input' function.
            # Given the sequence of inputs ('3' and '1'), the function should return '1'.
            # This line verifies that the return value is indeed '1'.
            self.assertEqual(self.user_login.initialise_user_auth(), '1')
        # Check the stored output from the print statements in the 'initialise_user_auth' function.
        # Verify that the expected error message was printed when an invalid choice ('3') was entered.
        self.assertIn('Invalid choice. Please select 1 or 2.', fake_out.getvalue())

    # Test to check if get_user_id returns the correct user ID when the username is found in the database.
    def test_get_user_id_username_found(self):
        mock_cursor = MagicMock()
        self.connection.cursor.return_value = mock_cursor
        mock_cursor.__enter__.return_value.fetchone.return_value = (123,)
        user_id = self.user_login.get_user_id('test_user')
        self.assertEqual(user_id, 123)

    # Test to check if get_user_id returns None when the username is not found in the database.
    def test_get_user_id_username_not_found(self):
        mock_cursor = MagicMock()
        self.connection.cursor.return_value = mock_cursor
        mock_cursor.__enter__.return_value.fetchone.return_value = None
        user_id = self.user_login.get_user_id('nonexistent_user')
        self.assertIsNone(user_id)

    # Test to verify if call_main_menu correctly creates an instance of the HomePage class
    # and calls its run_main_menu method with the provided user ID.
    @patch('application.login.login.HomePage')
    def test_call_main_menu(self, mock_homepage):
        user_id = 123
        self.user_login.call_main_menu(user_id)
        mock_homepage.assert_called_once_with(self.user_login, self.connection)
        mock_homepage.return_value.run_main_menu.assert_called_once_with(user_id)

    # Test to check the behavior of user_auth when the user chooses the login option.
    @patch('application.login.login.UserLogin.initialise_user_auth', return_value='1')
    @patch('application.login.login.UserLogin.user_log_in', return_value=123)
    @patch('application.login.login.UserLogin.create_new_user', return_value=456)
    @patch('application.login.login.UserLogin.title_image')
    def test_user_auth_login_choice(self, mock_title_image, mock_create_new_user, mock_user_log_in, mock_initialise_user_auth):
        user_id = self.user_login.user_auth()
        self.assertEqual(user_id, [123])
        mock_title_image.assert_called_once()
        mock_user_log_in.assert_called_once()
        mock_create_new_user.assert_not_called()

    # Test to check the behavior of user_auth when the user chooses the create user option.
    @patch('application.login.login.UserLogin.initialise_user_auth', return_value='2')
    @patch('application.login.login.UserLogin.user_log_in', return_value=123)
    @patch('application.login.login.UserLogin.create_new_user', return_value=456)
    @patch('application.login.login.UserLogin.title_image')
    def test_user_auth_create_user_choice(self, mock_title_image, mock_create_new_user, mock_user_log_in, mock_initialise_user_auth):
        user_id = self.user_login.user_auth()
        self.assertEqual(user_id, [456])
        mock_title_image.assert_called_once()
        mock_user_log_in.assert_not_called()
        mock_create_new_user.assert_called_once()

if __name__ == "__main__":
    unittest.main()
