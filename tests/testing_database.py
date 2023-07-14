import unittest
from unittest.mock import patch
from databases.database import DatabaseCreation, DatabaseManagement, PlantDataManager


class TestDatabaseManagement(unittest.TestCase):

    def setUp(self):
        self.db_management = DatabaseManagement('localhost', 'user', 'password', 'plantsapp')

    def test_connect(self):
        with patch('database.pymysql') as mock_pymysql:
            self.db_management.connect()
            mock_pymysql.connect.assert_called_with(
                host='localhost',
                user='user',
                password='password',
                database='plantsapp'
            )
            self.assertIsNotNone(self.db_management.connection)
            self.assertIsNotNone(self.db_management.cursor)

    def test_exit(self):
        self.db_management.cursor = 'mock_cursor'
        self.db_management.connection = 'mock_connection'
        self.db_management.__exit__(None, None, None)
        self.assertIsNone(self.db_management.cursor)
        self.assertIsNone(self.db_management.connection)


class TestDatabaseCreation(unittest.TestCase):

    def setUp(self):
        self.db_creation = DatabaseCreation('localhost', 'user', 'password', 'plantsapp')

    def test_create_database(self):
        with patch('database.pymysql') as mock_pymysql:
            mock_cursor = mock_pymysql.connect.return_value.cursor.return_value
            self.db_creation.create_database()
            mock_cursor.execute.assert_any_call("CREATE DATABASE IF NOT EXISTS plantsapp;")
            mock_cursor.execute.assert_any_call("USE plantsapp;")

    def test_create_tables(self):
        with patch('database.pymysql') as mock_pymysql:
            mock_cursor = mock_pymysql.connect.return_value.cursor.return_value
            self.db_creation.create_tables()
            mock_cursor.execute.assert_any_call("USE plantsapp;")
            mock_cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) NOT NULL UNIQUE);")
            mock_cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS plant_id (id VARCHAR(10) PRIMARY KEY, plant_name VARCHAR(255) NOT NULL, latin_name VARCHAR(255) NOT NULL, class_name VARCHAR(255) NOT NULL);")
            mock_cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS plant_requirements (id VARCHAR(10), light_conditions VARCHAR(255) NOT NULL, frequency_watering INT NOT NULL, soil_type VARCHAR(255) NOT NULL, growing_time INT NOT NULL, toxicity VARCHAR(255) NOT NULL, FOREIGN KEY (id) REFERENCES plant_id(id));")
            mock_cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS logbook (logbook_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, plant_id VARCHAR(10) NOT NULL, date_planted DATE, FOREIGN KEY (user_id) REFERENCES users(user_id), FOREIGN KEY (plant_id) REFERENCES plant_id(id));")
            mock_pymysql.connect.return_value.commit.assert_called_once()

    def test_populate_plant_id_and_requirements_tables(self):
        plant_data = {
            '1': {
                'plant_name': 'Plant 1',
                'latin_name': 'Latin 1',
                'class_name': 'Class 1',
                'light_conditions': 'Full Sun',
                'frequency_watering': 1,
                'soil_type': 'Well-drained',
                'growing_time': 10,
                'toxicity': 'Non-toxic'
            }
        }
        with patch('database.pymysql') as mock_pymysql:
            mock_cursor = mock_pymysql.connect.return_value.cursor.return_value
            mock_cursor.fetchone.return_value = None
            self.db_creation.populate_plant_id_and_requirements_tables(plant_data)
            mock_cursor.execute.assert_called_with("USE plantsapp;")
            mock_cursor.execute.assert_called_with(
                "INSERT INTO plant_id (id, plant_name, latin_name, class_name) VALUES (%s, %s, %s, %s);",
                ('1', 'Plant 1', 'latin 1', 'Class 1')
            )
            mock_cursor.execute.assert_called_with(
                "INSERT INTO plant_requirements (id, light_conditions, frequency_watering, soil_type, growing_time, toxicity) VALUES (%s, %s, %s, %s, %s, %s);",
                ('1', 'Full Sun', 1, 'Well-drained', 10, 'Non-toxic')
            )
            mock_pymysql.connect.return_value.commit.assert_called_once()


class TestPlantDataManager(unittest.TestCase):

    def setUp(self):
        self.plant_data_manager = PlantDataManager()

    @patch('database.requests.get')
    def test_fetch_plant_data(self, mock_get):
        # Prepare mock response
        mock_response = {'plant': 'data'}
        mock_get.return_value.json.return_value = mock_response

        # Call the function
        plant_data = self.plant_data_manager.fetch_plant_data()

        # Assertions
        mock_get.assert_called_with('https://raw.githubusercontent.com/RubyBlues/Project/main/plantjsondata.json')
        self.assertEqual(plant_data, mock_response)


if __name__ == '__main__':
    unittest.main()