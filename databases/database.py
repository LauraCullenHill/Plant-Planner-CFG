# Helper functions -----------------------------------------------------------------------------------------------------
import pymysql
import requests
from databases.mysql_connect import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD


# Database management --------------------------------------------------------------------------------------------------
class DatabaseManagement:
    def __init__(self, host, user, password, database=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f'Error in connecting to db: {e}')

    def __enter__(self):
        try:
            self.connect()
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f'Error in connecting to db: {e}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()


# Database creation --------------------------------------------
class DatabaseCreation(DatabaseManagement):
    def __init__(self, host, user, password, database=None):
        super().__init__(host, user, password, database)

    def create_database(self):
        try:
            self.connect()  # Connect without specifying a database
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database};")
            self.cursor.execute(f"USE {self.database};")
            print("Successfully created database.")
            self.connect(self.database)  # Reconnect with the new database
        except Exception as exc:
            print(f'Error in creating database: {exc}')

    def create_tables(self):
        try:
            self.cursor.execute("USE plantsapp;")
            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) NOT NULL UNIQUE
                    );
                    """)

            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS plant_id (
                        id VARCHAR(10) PRIMARY KEY,
                        plant_name VARCHAR(255) NOT NULL,
                        latin_name VARCHAR(255) NOT NULL,
                        class_name VARCHAR(255) NOT NULL
                    );
                    """)

            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS plant_requirements (
                        id VARCHAR(10),
                        light_conditions VARCHAR(255) NOT NULL,
                        frequency_watering INT NOT NULL,
                        soil_type VARCHAR(255) NOT NULL,
                        growing_time INT NOT NULL,
                        toxicity VARCHAR(255) NOT NULL,
                        FOREIGN KEY (id) REFERENCES plant_id(id)
                    );
                    """)

            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS logbook (
                        logbook_id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        plant_id VARCHAR(10) NOT NULL,
                        date_planted DATE,
                        FOREIGN KEY (user_id) REFERENCES users(user_id),
                        FOREIGN KEY (plant_id) REFERENCES plant_id(id)
                    );
                    """)

            self.connection.commit()
        except Exception as exc:
            print(f'Error in creating tables: {exc}')

    def disconnect(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def populate_plant_id_and_requirements_tables(self, plant_data):
        plant_id_exists_query = "SELECT 1 FROM plant_id WHERE id = %s"
        insert_query_plant_requirements = """
            INSERT INTO plant_requirements (id, light_conditions, frequency_watering, soil_type, growing_time, toxicity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        insert_query_plant_id = """
            INSERT INTO plant_id (id, plant_name, latin_name, class_name)
            VALUES (%s, %s, %s, %s)
        """
        try:
            for plant_id, plant_info in plant_data.items():
                self.cursor.execute("USE plantsapp;")
                self.cursor.execute(plant_id_exists_query, (plant_id,))
                if self.cursor.fetchone() is None:
                    self.cursor.execute(insert_query_plant_id, (
                        plant_id, plant_info['plant_name'], plant_info['latin_name'].lower(),
                        plant_info['class_name'].title()))
                    self.cursor.execute(insert_query_plant_requirements, (
                        plant_id, plant_info['light_conditions'], plant_info['frequency_watering'],
                        plant_info['soil_type'], plant_info['growing_time'], plant_info['toxicity']))
            self.connection.commit()
        except Exception as exc:
            print(f'Error in populating tables: {exc}')


# Plant data manager class
class PlantDataManager:
    @staticmethod
    def connect_to_plantapp():
        try:
            connection = pymysql.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database='plantsapp'
            )
            return connection
        except Exception as exc:
            print(f'Error in connecting to db: {exc}')

    def fetch_plant_data(self):
        json_url = 'https://raw.githubusercontent.com/RubyBlues/Project/main/plantjsondata.json'
        response = requests.get(json_url)
        return response.json()


def main():
    # Create an instance of the DatabaseCreation class
    db_creation = DatabaseCreation(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, 'plantsapp')
    from application.homepage.homepage import HomePage

    # Initialize the database
    with db_creation as db:
        # Create the tables and populate them with data
        db.create_tables()

        # Fetch JSON data and populate plant_data
        data_manager = PlantDataManager()
        plant_data = data_manager.fetch_plant_data()
        db.populate_plant_id_and_requirements_tables(plant_data)

        # Create an instance of the UserLogin class and pass the database connection
        from application.login.login import UserLogin
        user_login = UserLogin(db_creation.connection)

        # Authenticate the user and get the user ID
        user_id = user_login.user_auth()[0]

        # Check if authentication was successful
        if user_id is not None:
            # Create an instance of the HomePage class and pass the user ID
            home_page = HomePage(user_id)
            home_page.run_main_menu()
        else:
            print("Authentication failed.")


if __name__ == '__main__':
    main()