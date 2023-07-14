from unittest import TestCase, mock, main
from application.homepage.homepage import HomePage, exit_app


class TestHomePage(TestCase):

    def setUp(self):
        self.homepage = HomePage(user_id='12345')

    def test_main_menu_options_valid_choice(self):
        with mock.patch('builtins.input', return_value='1'):
            choice = self.homepage.main_menu_options()
            self.assertEqual(choice, '1')

    def test_main_menu_options_invalid_choice(self):
        with mock.patch('builtins.input', return_value='6'):
            with mock.patch('builtins.print') as mock_print:
                choice = self.homepage.main_menu_options()
                expected_output = "\nInvalid choice. Please select 1, 2, 3, 4, or 5."
                mock_print.assert_called_with(expected_output)
                self.assertIsNone(choice)

    def test_run_main_menu_choice_1(self):
        with mock.patch('builtins.input', return_value='1'):
            with mock.patch('homepage.run_logbook') as mock_run_logbook:
                self.homepage.run_main_menu()
                mock_run_logbook.assert_called_with('12345')

    def test_run_main_menu_choice_2(self):
        with mock.patch('builtins.input', return_value='2'):
            with mock.patch.object(self.homepage, 'view_weather') as mock_view_weather:
                self.homepage.run_main_menu()
                mock_view_weather.assert_called()

    def test_run_main_menu_choice_3(self):
        with mock.patch('builtins.input', return_value='3'):
            with mock.patch.object(self.homepage, 'get_random_quote') as mock_get_random_quote:
                self.homepage.run_main_menu()
                mock_get_random_quote.assert_called()

    def test_run_main_menu_choice_4(self):
        with mock.patch('builtins.input', return_value='4'):
            with mock.patch.object(self.homepage, 'do_plant_quiz') as mock_do_plant_quiz:
                self.homepage.run_main_menu()
                mock_do_plant_quiz.assert_called()

    def test_run_main_menu_choice_5(self):
        with mock.patch('builtins.input', return_value='5'):
            with self.assertRaises(SystemExit):
                self.homepage.run_main_menu()

    def test_run_main_menu_invalid_choice(self):
        with mock.patch('builtins.input', return_value='invalid'):
            with mock.patch('builtins.print') as mock_print:
                self.homepage.run_main_menu()
                expected_output = "\nInvalid choice. Please enter 1, 2, 3, 4, or 5."
                mock_print.assert_called_with(expected_output)

    def test_search_plant(self):
        with mock.patch('homepage.MainPlantSearch') as mock_MainPlantSearch:
            plant_search_instance = mock_MainPlantSearch.return_value
            self.homepage.search_plant()
            plant_search_instance.user_plant_search.assert_called()

    def test_search_invalid_input(self):
        with patch('builtins.input', side_effect=['invalid plant']):
            with patch('homepage.print') as mock_print:
                self.homepage.do_search()
                mock_print.assert_called_with("Invalid input. Please enter a valid plant name.")

    def test_view_weather(self):
        with mock.patch('builtins.input') as mock_input:
            with mock.patch('homepage.main_weather_program') as mock_main_weather_program:
                mock_input.side_effect = ['m', 'other', 'm']
                self.homepage.view_weather()
                mock_main_weather_program.assert_called()
                self.assertEqual(mock_input.call_count, 3)

    def test_get_random_quote(self):
        with mock.patch('subprocess.run') as mock_subprocess_run:
            self.homepage.get_random_quote()
            mock_subprocess_run.assert_called_with(["python", "application/quotations/randomquote.py"])

    def test_do_plant_quiz(self):
        with mock.patch('subprocess.run') as mock_subprocess_run:
            self.homepage.do_plant_quiz()
            mock_subprocess_run.assert_called_with(["python", "application/plant_quiz/plant_quiz.py"])

    def test_exit_app(self):
        with self.assertRaises(SystemExit):
            exit_app()


if __name__ == '__main__':
    main()