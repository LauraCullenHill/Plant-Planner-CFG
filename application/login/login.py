# Helper functions -----------------------------------------------------------------------------------------------------
from application.homepage.homepage import HomePage
from images.ascii_art import ascii_title


# Logging in and creating a new user -----------------------------------------------------------------------------------
class UserLogin:
    def __init__(self, connection):
        self.connection = connection

    def exit_app():
        print('\nSee you next time!')
        print('********** APP CLOSED **********')
        raise SystemExit

    def initialise_user_auth(self):
        while True:
            print("1. Log in")
            print("2. Create a new account")
            choice = input("Enter your choice (1 or 2): ")
            if choice == '1' or choice == '2':
                return choice
            else:
                print('\nInvalid choice. Please select 1 or 2.')

    def user_log_in(self):
        try:
            cursor = self.connection.cursor()
            while True:
                username = input("\nEnter your username: ")
                cursor.execute("USE plantsapp;")
                cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
                result = cursor.fetchone()
                if result is None:
                    while True:
                        print("\nUsername not found. \n1. Create an account\n2. Try again\n3. Exit")
                        log_in_choice = input('Enter 1, 2, or 3: ')
                        if log_in_choice == '1':
                            self.create_new_user()
                            print('\nThe app will close now so you can log back in.')
                            exit_app()
                            break
                        elif log_in_choice == '2':
                            break
                        elif log_in_choice == '3':
                            exit_app()
                            break
                        else:
                            print('\nInvalid choice. Enter 1, 2, or 3.')
                            continue
                else:
                    print(f"\nLogged in as {username}")
                    user_id = result[0]
                    return user_id
        except Exception as exc:
            print(f'Error in connecting to db: {exc}')

    def create_new_user(self):
        try:
            cursor = self.connection.cursor()
            while True:
                username = input("\nEnter a new username: ")
                cursor.execute("USE plantsapp;")
                cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
                result = cursor.fetchone()
                if result is None:
                    cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
                    self.connection.commit()
                    cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
                    result = cursor.fetchone()
                    print(f"\nAccount created. Logged in as {username}")
                    user_id = result[0]
                    return user_id
                else:
                    print('\nThat username already exists. Try another one.')
        except Exception as exc:
            print(f'Error in connecting to db: {exc}')
        finally:
            if self.connection:
                self.connection.close()

    def get_user_id(self, username):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("USE plantsapp")  # Select the 'plantsapp' database
                cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
                result = cursor.fetchone()
                if result:
                    return result[0]  # Return the user ID directly from the result tuple
                else:
                    print("Username not found.")
                    return None  # Return None when username is not found
        except Exception as e:
            print(f'Error: {e}')

    def call_main_menu(self, user_id):
        if user_id is not None:
            print(f"\nLogged in as user_id: {user_id}")
            home_page = HomePage(self, self.connection)  # Pass user_login and database connection
            home_page.run_main_menu(user_id)

    def title_image(self):
        ascii_title()

    def user_auth(self):
        choice = self.initialise_user_auth()
        if choice == '1':
            user_id = self.user_log_in()
            self.title_image()
            return [user_id]  # Return a list containing the user_id
        elif choice == '2':
            user_id = self.create_new_user()
            self.title_image()
            return [user_id]  # Return a list containing the user_id

        print("Authentication failed.")
        return [None]