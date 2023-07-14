import unittest
from unittest.mock import MagicMock, patch, call
from logbook import PlantLogbook, UserLogbook, Plant, PlantRequirements

class UserLogbookTests(unittest.TestCase):
    def setUp(self):
        self.user_id = 1
        self.logbook = UserLogbook(self.user_id, load_from_db=False)

    def test_load_logbook_from_db(self):
        self.logbook.db = MagicMock()
        self.logbook.db.connect.return_value = True
        self.logbook.db.connection.cursor.return_value.__enter__.return_value.fetchall.return_value = [
            (1, 'Plant 1', 'Latin Name 1', 'Class Name 1', 'Light Conditions 1', 'Watering 1', 'Soil Type 1',
             'Growing Time 1', 'Toxicity 1', '2022-01-01'),
            (2, 'Plant 2', 'Latin Name 2', 'Class Name 2', 'Light Conditions 2', 'Watering 2', 'Soil Type 2',
             'Growing Time 2', 'Toxicity 2', '2022-01-02')
        ]

        self.logbook.load_logbook_from_db()

        self.assertEqual(len(self.logbook.logbook), 2)
        self.assertIsInstance(self.logbook.logbook[0][0], Plant)
        self.assertIsInstance(self.logbook.logbook[0][1], PlantRequirements)
        self.assertEqual(self.logbook.logbook[0][0].plant_id, 1)
        self.assertEqual(self.logbook.logbook[0][1].light_conditions, 'Light Conditions 1')

    def test_add_plant(self):
        plant = Plant(1, 'Plant 1', 'Latin Name 1', 'Class Name 1', '2022-01-01')
        requirements = PlantRequirements('Light Conditions', 'Watering', 'Soil Type', 'Growing Time', 'Toxicity')

        self.logbook.add_plant(plant, requirements)

        self.assertEqual(len(self.logbook.logbook), 1)
        self.assertEqual(self.logbook.logbook[0][0], plant)
        self.assertEqual(self.logbook.logbook[0][1], requirements)

    def test_remove_plant(self):
        plant1 = Plant(1, 'Plant 1', 'Latin Name 1', 'Class Name 1', '2022-01-01')
        plant2 = Plant(2, 'Plant 2', 'Latin Name 2', 'Class Name 2', '2022-01-02')
        requirements1 = PlantRequirements('Light Conditions 1', 'Watering 1', 'Soil Type 1', 'Growing Time 1', 'Toxicity 1')
        requirements2 = PlantRequirements('Light Conditions 2', 'Watering 2', 'Soil Type 2', 'Growing Time 2', 'Toxicity 2')

        self.logbook.logbook = [(plant1, requirements1), (plant2, requirements2)]

        self.logbook.remove_plant(1)

        self.assertEqual(len(self.logbook.logbook), 1)
        self.assertEqual(self.logbook.logbook[0][0], plant2)
        self.assertEqual(self.logbook.logbook[0][1], requirements2)

class PlantLogbookTests(unittest.TestCase):
    def setUp(self):
        self.user_id = 1
        self.logbook = PlantLogbook(self.user_id)

    def test_populate_logbook_entries(self):
        user_logbook_mock = MagicMock()
        user_logbook_mock.logbook = [(Plant(1, 'Plant 1', 'Latin Name 1', 'Class Name 1', '2022-01-01'),
                                      PlantRequirements('Light Conditions 1', 'Watering 1', 'Soil Type 1',
                                                        'Growing Time 1', 'Toxicity 1'))]

        user_logbook_constructor_mock = MagicMock(return_value=user_logbook_mock)
        user_logbook_mock.load_logbook_from_db = MagicMock()

        self.logbook.user_logbooks = {}
        self.logbook.db = MagicMock()
        self.logbook.db.connect.return_value = True
        self.logbook.db.connection.cursor.return_value.__enter__.return_value.fetchall.return_value = []

        with patch('logbook.UserLogbook', user_logbook_constructor_mock):
            self.logbook.populate_logbook_entries(self.user_id)

        self.assertEqual(len(self.logbook.user_logbooks), 1)

    def test_display_logbook_existing_logbook(self):
        user_logbook_mock = MagicMock()
        user_logbook_mock.logbook = [(Plant(1, 'Plant 1', 'Latin Name 1', 'Class Name 1', '2022-01-01'),
                                      PlantRequirements('Light Conditions 1', 'Watering 1', 'Soil Type 1',
                                                        'Growing Time 1', 'Toxicity 1')),
                                     (Plant(2, 'Plant 2', 'Latin Name 2', 'Class Name 2', '2022-01-02'),
                                      PlantRequirements('Light Conditions 2', 'Watering 2', 'Soil Type 2',
                                                        'Growing Time 2', 'Toxicity 2'))]

        self.logbook.user_logbooks = {self.user_id: user_logbook_mock}

        with patch('builtins.print') as mock_print:
            self.logbook.display_logbook(self.user_id)

            expected_output = [
                call("\nYour Logbook:"),
                call("Plant ID: 1"),
                call("Plant Name: Plant 1"),
                call("Latin Name: Latin Name 1"),
                call("Class Name: Class Name 1"),
                call("Light Conditions: Light Conditions 1"),
                call("Frequency of Watering: Watering 1"),
                call("Soil Type: Soil Type 1"),
                call("Growing Time: Growing Time 1"),
                call("Toxicity: Toxicity 1"),
                call("Date planted: 2022-01-01"),
                call("---------------------"),
                call("Plant ID: 2"),
                call("Plant Name: Plant 2"),
                call("Latin Name: Latin Name 2"),
                call("Class Name: Class Name 2"),
                call("Light Conditions: Light Conditions 2"),
                call("Frequency of Watering: Watering 2"),
                call("Soil Type: Soil Type 2"),
                call("Growing Time: Growing Time 2"),
                call("Toxicity: Toxicity 2"),
                call("Date planted: 2022-01-02"),
                call("---------------------")
            ]
            mock_print.assert_has_calls(expected_output)

    def test_display_logbook_empty_logbook(self):
        user_logbook_mock = MagicMock()
        user_logbook_mock.logbook = []

        self.logbook.user_logbooks = {self.user_id: user_logbook_mock}

        with patch('builtins.print') as mock_print:
            self.logbook.display_logbook(self.user_id)

            mock_print.assert_called_with("Your logbook is empty.")

    def test_display_logbook_no_logbook(self):
        self.logbook.user_logbooks = {}

        with patch('builtins.print') as mock_print:
            self.logbook.display_logbook(self.user_id)

            mock_print.assert_called_with("No logbook found for the user.")

    def test_remove_plant_from_logbook(self):
        user_logbook_mock = MagicMock()
        user_logbook_mock.remove_plant = MagicMock()
        self.logbook.user_logbooks = {self.user_id: user_logbook_mock}

        self.logbook.delete_logbook_entry = MagicMock()

        self.logbook.remove_plant_from_logbook(self.user_id, 1)

        user_logbook_mock.remove_plant.assert_called_with(1)
        self.logbook.delete_logbook_entry.assert_called_with(self.user_id, 1)
        print("Plant removed from your logbook.")

    def test_search_plants(self):
        query = "Plant"

        self.logbook.db = MagicMock()
        self.logbook.db.connect.return_value = True
        self.logbook.db.connection.cursor.return_value.__enter__.return_value.fetchall.return_value = [
            (1, 'Plant 1', 'Latin Name 1', 'Class Name 1'),
            (2, 'Plant 2', 'Latin Name 2', 'Class Name 2')
        ]

        plants = self.logbook.search_plants(query)

        self.assertEqual(len(plants), 2)
        self.assertIsInstance(plants[0], Plant)
        self.assertEqual(plants[0].plant_id, 1)
        self.assertEqual(plants[0].plant_name, 'Plant 1')

    def test_get_plant_by_id(self):
        plant_id = 1

        self.logbook.db = MagicMock()
        self.logbook.db.connect.return_value = True
        self.logbook.db.connection.cursor.return_value.__enter__.return_value.fetchone.return_value = (
            1, 'Plant 1', 'Latin Name 1', 'Class Name 1'
        )

        plant = self.logbook.get_plant_by_id(plant_id)

        self.assertIsInstance(plant, Plant)
        self.assertEqual(plant.plant_id, 1)
        self.assertEqual(plant.plant_name, 'Plant 1')

    def test_insert_logbook_entry(self):
        user_id = 1
        plant_id = 1
        date_planted = '2022-01-01'

        self.logbook.db = MagicMock()
        self.logbook.db.connect.return_value = True
        self.logbook.db.connection.cursor.return_value.__enter__.return_value.execute.return_value = None
        self.logbook.db.connection.commit.return_value = None

        self.logbook.insert_logbook_entry(user_id, plant_id, date_planted)

        self.logbook.db.connection.cursor.return_value.__enter__.return_value.execute.assert_called_with(
            "INSERT INTO logbook (user_id, plant_id, date_planted) VALUES (%s, %s, %s)",
            (user_id, plant_id, date_planted)
        )
        self.logbook.db.connection.commit.assert_called()

    def test_delete_logbook_entry(self):
        plant_id = 1
        user_id = 1
        self.logbook.db = MagicMock()
        self.logbook.db.connection.cursor.return_value.__enter__.return_value.fetchone.return_value = (1,)

        with unittest.mock.patch('builtins.print') as mock_print:
            self.logbook.delete_logbook_entry(user_id, plant_id)

        self.logbook.db.connection.cursor.return_value.__enter__.return_value.execute.assert_called_with(
            'DELETE FROM logbook WHERE user_id = %s AND plant_id = %s;', (user_id, plant_id))
        mock_print.assert_called_once_with("Plant removed from your logbook.")

if __name__ == '__main__':
    unittest.main()