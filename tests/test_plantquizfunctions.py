from unittest import TestCase, mock
from unittest.mock import patch
from application.plantquiz.plantquizfunctions import all_plant_quiz_functions
import requests
import json
from datetime import datetime
import calendar
from io import StringIO

# -------------------------------------------------------------------------
# Tests q1()
class TestQuizFunctions(TestCase):
    @mock.patch('builtins.input', side_effect=["a"])
    def test_q1a(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # calling the q1 method on the instance
        choice = 'Fruit'
        category = 'class_name'
        does_choice_work = plantquiz.is_choice_in_plant_info_json(choice, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)

    @mock.patch('builtins.input', side_effect=["b"])
    def test_q1b(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()  # calling the q1 method on the instance
        choice = 'Flower'
        category = 'class_name'
        does_choice_work = plantquiz.is_choice_in_plant_info_json(choice, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)

    @mock.patch('builtins.input', side_effect=["c"])
    def test_q1c(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()  # calling the q1 method on the instance
        choice = 'Shrub'
        category = 'class_name'
        does_choice_work = plantquiz.is_choice_in_plant_info_json(choice, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)

    @mock.patch('builtins.input', side_effect=["d"])
    def test_q1d(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()  # calling the q1 method on the instance
        choice = 'Vegetable'
        category = 'class_name'
        does_choice_work = plantquiz.is_choice_in_plant_info_json(choice, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)

    @mock.patch('builtins.input', side_effect=["e"])
    def test_q1e(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()  # calling the q1 method on the instance
        self.assertTrue(len(results) > 0)
        response = requests.get('https://raw.githubusercontent.com/RubyBlues/Project/main/plantjsondata.json')
        self.plant_data = json.loads(response.text)
        self.assertCountEqual(self.plant_data.items(), results)

    @mock.patch('builtins.input', side_effect=["q"])
    def test_q1q(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()  # calling the q1 method on the instance
        self.assertIsNone(results)

    @mock.patch('builtins.input', side_effect=["x", "a"]) # Mocking invalid input followed by a valid choice
    def test_q1_invalid_choice(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class

        results = plantquiz.q1()

        # Assert that the method returns a valid result after the second iteration (so it doesn't loop indefinitely)
        # Just needs to be not none as choice 'a' is already tested above
        self.assertIsNotNone(results)



# -------------------------------------------------------------------------
# Tests q2()
    @mock.patch('builtins.input', side_effect=["e", "a"])
    def test_q2a(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # get the results from the previous function to use in this one
        results = plantquiz.q2(results) # calling the q2 method on the instance
        choice = 'Full sun'
        category = 'light_conditions'
        does_choice_work = plantquiz.is_choice_in_plant_info(choice, results, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)

    @mock.patch('builtins.input', side_effect=["e", "b"])
    def test_q2b(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # get the results from the previous function to use in this one
        results = plantquiz.q2(results) # calling the q2 method on the instance
        choice = 'Partial shade'
        category = 'light_conditions'
        does_choice_work = plantquiz.is_choice_in_plant_info(choice, results, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)

    @mock.patch('builtins.input', side_effect=["e", "c"])
    def test_q2c(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # get the results from the previous function to use in this one
        results = plantquiz.q2(results) # calling the q2 method on the instance
        choice = 'Shade'
        category = 'light_conditions'
        does_choice_work = plantquiz.is_choice_in_plant_info(choice, results, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)

    @mock.patch('builtins.input', side_effect=["e", "d"])
    def test_q2d(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # get the results from the previous function to use in this one
        results = plantquiz.q2(results) # calling the q2 method on the instance
        self.assertTrue(len(results) > 0)
        choice_a = 'Full sun'
        choice_b = 'Partial shade'
        choice_c = 'Shade'
        category = 'light_conditions'
        # to test this function, it needs to have not filtered anything in this question, so check for the
        # presence of all three 'filters' in order to pass the test
        does_choice_a_work = plantquiz.is_choice_in_plant_info(choice_a, results, category)
        does_choice_b_work = plantquiz.is_choice_in_plant_info(choice_b, results, category)
        does_choice_c_work = plantquiz.is_choice_in_plant_info(choice_c, results, category)
        all_choices_found = does_choice_a_work and does_choice_b_work and does_choice_c_work
        self.assertTrue(all_choices_found)

    @mock.patch('builtins.input', side_effect=["e", "q"])
    def test_q2q(self, mock_input):
            plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
            results = plantquiz.q1()  # get the results from the previous function to use in this one
            results = plantquiz.q2(results)  # calling the q2 method on the instance
            self.assertIsNone(results)

    @mock.patch('builtins.input', side_effect=["e", "x", "a"])  # Mocking invalid input followed by a valid choice
    def test_q2_invalid_choice(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()
        results = plantquiz.q2(results)

        # Assert that the method returns a valid result after the second iteration (so it doesn't loop indefinitely)
        # Just needs to be not none as choice 'a' is already tested above
        self.assertIsNotNone(results)

# -------------------------------------------------------------------------
# Tests q3()

    @mock.patch('builtins.input', side_effect=["e", "d", "a"])
    def test_q3a(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # get the results from the previous functions to use in this one
        results = plantquiz.q2(results) # get the results from the previous functions to use in this one
        results = plantquiz.q3(results) # calling the q3 method on the instance
        choice = 'Well drained'
        category = 'soil_type'
        does_choice_work = plantquiz.is_choice_in_plant_info(choice, results, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)

    @mock.patch('builtins.input', side_effect=["e", "d", "b"])
    def test_q3b(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # get the results from the previous functions to use in this one
        results = plantquiz.q2(results) # get the results from the previous functions to use in this one
        results = plantquiz.q3(results) # calling the q3 method on the instance
        choice = 'Loamy'
        category = 'soil_type'
        does_choice_work = plantquiz.is_choice_in_plant_info(choice, results, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)


    @mock.patch('builtins.input', side_effect=["e", "d", "c"])
    def test_q3c(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()  # get the results from the previous functions to use in this one
        results = plantquiz.q2(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q3(results)  # calling the q3 method on the instance
        choice = 'Acidic'
        category = 'soil_type'
        does_choice_work = plantquiz.is_choice_in_plant_info(choice, results, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)


    @mock.patch('builtins.input', side_effect=["e", "d", "d"])
    def test_q3d(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()  # get the results from the previous functions to use in this one
        results = plantquiz.q2(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q3(results)  # calling the q3 method on the instance
        choice = 'Moist'
        category = 'soil_type'
        does_choice_work = plantquiz.is_choice_in_plant_info(choice, results, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)


    @mock.patch('builtins.input', side_effect=["e", "d", "e"])
    def test_q3e(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()  # get the results from the previous functions to use in this one
        results = plantquiz.q2(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q3(results)  # calling the q3 method on the instance
        self.assertTrue(len(results) > 0)
        choice_a = 'Well drained'
        choice_b = 'Loamy'
        choice_c = 'Acidic'
        choice_d = 'Moist'
        category = 'soil_type'
        does_choice_a_work = plantquiz.is_choice_in_plant_info(choice_a, results, category)
        does_choice_b_work = plantquiz.is_choice_in_plant_info(choice_b, results, category)
        does_choice_c_work = plantquiz.is_choice_in_plant_info(choice_c, results, category)
        does_choice_d_work = plantquiz.is_choice_in_plant_info(choice_d, results, category)
        all_choices_found = does_choice_a_work and does_choice_b_work and does_choice_c_work and does_choice_d_work
        self.assertTrue(all_choices_found)

    @mock.patch('builtins.input', side_effect=["e", "d", "q"])
    def test_q3q(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()  # get the results from the previous functions to use in this one
        results = plantquiz.q2(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q3(results)  # calling the q3 method on the instance
        self.assertIsNone(results)

    @mock.patch('builtins.input', side_effect=["e", "d", "x", "a"])  # Mocking invalid input followed by a valid choice
    def test_q3_invalid_choice(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()
        results = plantquiz.q2(results)
        results = plantquiz.q3(results)

        # Assert that the method returns a valid result after the second iteration (so it doesn't loop indefinitely)
        # Just needs to be not none as choice 'a' is already tested above
        self.assertIsNotNone(results)

# -------------------------------------------------------------------------
# Tests q4()

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "a"])
    def test_q4a(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # get the results from the previous functions to use in this one
        results = plantquiz.q2(results) # get the results from the previous functions to use in this one
        results = plantquiz.q3(results) # get the results from the previous functions to use in this one
        results = plantquiz.q4(results) # calling the q4 method on the instance
        month = calendar.month_name[datetime.now().month]
        choice = month
        category = 'planting_season'
        does_choice_work = plantquiz.is_choice_in_plant_info(choice, results, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "b"])
    def test_q4b(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # get the results from the previous functions to use in this one
        results = plantquiz.q2(results) # get the results from the previous functions to use in this one
        results = plantquiz.q3(results) # get the results from the previous functions to use in this one
        results = plantquiz.q4(results) # calling the q4 method on the instance
        self.assertTrue(len(results) > 0)
        choice_a = 'June' # plant seasons are split into 3 months, choose 1 month from each season to check all
        choice_b = 'September' # results from previous function have been carried over
        choice_c = 'December'
        choice_d = 'March'
        category = 'planting_season'
        does_choice_a_work = plantquiz.is_choice_in_plant_info(choice_a, results, category)
        does_choice_b_work = plantquiz.is_choice_in_plant_info(choice_b, results, category)
        does_choice_c_work = plantquiz.is_choice_in_plant_info(choice_c, results, category)
        does_choice_d_work = plantquiz.is_choice_in_plant_info(choice_d, results, category)
        all_choices_found = does_choice_a_work and does_choice_b_work and does_choice_c_work and does_choice_d_work
        self.assertTrue(all_choices_found)

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "q"])
    def test_q4q(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()  # get the results from the previous functions to use in this one
        results = plantquiz.q2(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q3(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q4(results)  # calling the q4 method on the instance
        self.assertIsNone(results)

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "x", "a"])  # Mocking invalid input followed by a valid choice
    def test_q4_invalid_choice(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()
        results = plantquiz.q2(results)
        results = plantquiz.q3(results)
        results = plantquiz.q4(results)

        # Assert that the method returns a valid result after the second iteration (so it doesn't loop indefinitely)
        # Just needs to be not none as choice 'a' is already tested above
        self.assertIsNotNone(results)

# -------------------------------------------------------------------------
# Tests q5()

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "b", "a"])
    def test_q5a(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # get the results from the previous functions to use in this one
        results = plantquiz.q2(results) # get the results from the previous functions to use in this one
        results = plantquiz.q3(results) # get the results from the previous functions to use in this one
        results_q4 = plantquiz.q4(results) # save results from the previous functions to check same as this one
        results = plantquiz.q5(results) # calling the q5 method on the instance
        self.assertTrue(len(results) > 0)
        self.assertListEqual(results_q4, results)

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "b", "b"])
    def test_q5b(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()  # get the results from the previous functions to use in this one
        results = plantquiz.q2(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q3(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q4(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q5(results)  # calling the q5 method on the instance
        choice = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        category = 'frequency_watering'
        are_results_in_choice = all(result[1][category] in choice for result in results)
        self.assertTrue(are_results_in_choice)

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "b", "c"])
    def test_q5c(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()  # get the results from the previous functions to use in this one
        results = plantquiz.q2(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q3(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q4(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q5(results)  # calling the q5 method on the instance
        choice = [7, 8, 9, 10, 11, 12, 13, 14]
        category = 'frequency_watering'
        are_results_in_choice = all(result[1][category] in choice for result in results)
        self.assertTrue(are_results_in_choice)

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "b", "d"])
    def test_q5d(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # get the results from the previous functions to use in this one
        results = plantquiz.q2(results) # get the results from the previous functions to use in this one
        results = plantquiz.q3(results) # get the results from the previous functions to use in this one
        results_q4 = plantquiz.q4(results) # save results from the previous functions to check same as this one
        results = plantquiz.q5(results) # calling the q5 method on the instance
        self.assertTrue(len(results) > 0)
        self.assertListEqual(results_q4, results)

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "b", "q"])
    def test_q5q(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()  # get the results from the previous functions to use in this one
        results = plantquiz.q2(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q3(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q4(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q5(results)  # calling the q5 method on the instance
        self.assertIsNone(results)

    @mock.patch('builtins.input',
                side_effect=["e", "d", "e", "b", "x", "a"])  # Mocking invalid input followed by a valid choice
    def test_q5_invalid_choice(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()
        results = plantquiz.q2(results)
        results = plantquiz.q3(results)
        results = plantquiz.q4(results)
        results = plantquiz.q5(results)

        # Assert that the method returns a valid result after the second iteration (so it doesn't loop indefinitely)
        # Just needs to be not none as choice 'a' is already tested above
        self.assertIsNotNone(results)

# -------------------------------------------------------------------------
# Tests q6()

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "a", "d", "a"])
    def test_q6a(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # get the results from the previous functions to use in this one
        results = plantquiz.q2(results) # get the results from the previous functions to use in this one
        results = plantquiz.q3(results) # get the results from the previous functions to use in this one
        results = plantquiz.q4(results) # get the results from the previous functions to use in this one
        results = plantquiz.q5(results) # get the results from the previous functions to use in this one
        results = plantquiz.q6(results) # calling the q6 method on the instance
        choice = 'None'
        category = 'toxicity'
        does_choice_work = plantquiz.is_choice_in_plant_info(choice, results, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "a", "d", "b"])
    def test_q6b(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # get the results from the previous functions to use in this one
        results = plantquiz.q2(results) # get the results from the previous functions to use in this one
        results = plantquiz.q3(results) # get the results from the previous functions to use in this one
        results = plantquiz.q4(results) # get the results from the previous functions to use in this one
        results = plantquiz.q5(results) # get the results from the previous functions to use in this one
        results = plantquiz.q6(results) # calling the q6 method on the instance
        choice = 'Humans'
        category = 'toxicity'
        does_choice_work = plantquiz.is_choice_in_plant_info(choice, results, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "a", "d", "c"])
    def test_q6c(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # get the results from the previous functions to use in this one
        results = plantquiz.q2(results) # get the results from the previous functions to use in this one
        results = plantquiz.q3(results) # get the results from the previous functions to use in this one
        results = plantquiz.q4(results) # get the results from the previous functions to use in this one
        results = plantquiz.q5(results) # get the results from the previous functions to use in this one
        results = plantquiz.q6(results) # calling the q6 method on the instance
        choice = 'Animals'
        category = 'toxicity'
        does_choice_work = plantquiz.is_choice_in_plant_info(choice, results, category)
        self.assertTrue(does_choice_work)
        self.assertTrue(len(results) > 0)

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "a", "d", "d"])
    def test_q6d(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1() # get the results from the previous functions to use in this one
        results = plantquiz.q2(results) # get the results from the previous functions to use in this one
        results = plantquiz.q3(results) # get the results from the previous functions to use in this one
        results = plantquiz.q4(results) # get the results from the previous functions to use in this one
        results = plantquiz.q5(results) # get the results from the previous functions to use in this one
        results = plantquiz.q6(results) # calling the q6 method on the instance
        self.assertTrue(len(results) > 0)
        choice_a = 'None'
        choice_b = 'Humans'
        choice_c = 'Animals'
        category = 'toxicity'
        does_choice_a_work = plantquiz.is_choice_in_plant_info(choice_a, results, category)
        does_choice_b_work = plantquiz.is_choice_in_plant_info(choice_b, results, category)
        does_choice_c_work = plantquiz.is_choice_in_plant_info(choice_c, results, category)
        all_choices_found = does_choice_a_work and does_choice_b_work and does_choice_c_work
        self.assertTrue(all_choices_found)

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "a", "d", "q"])
    def test_q6q(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()  # get the results from the previous functions to use in this one
        results = plantquiz.q2(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q3(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q4(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q5(results)  # get the results from the previous functions to use in this one
        results = plantquiz.q6(results)  # calling the q6 method on the instance
        self.assertIsNone(results)

    @mock.patch('builtins.input',
                side_effect=["e", "d", "e", "b", "d", "x", "a"])  # Mocking invalid input followed by a valid choice
    def test_q6_invalid_choice(self, mock_input):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = plantquiz.q1()
        results = plantquiz.q2(results)
        results = plantquiz.q3(results)
        results = plantquiz.q4(results)
        results = plantquiz.q5(results)
        results = plantquiz.q6(results)

        # Assert that the method returns a valid result after the second iteration (so it doesn't loop indefinitely)
        # Just needs to be not none as choice 'a' is already tested above
        self.assertIsNotNone(results)

# -------------------------------------------------------------------------
# Tests check_results()

    def test_check_results(self):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        results = [] # simulating empty results
        self.assertFalse(plantquiz.check_results(results))


# -------------------------------------------------------------------------
# Tests quiz_results()
    @patch('random.choice')
    def test_quiz_result(self, mock_choice):
        plantquiz = all_plant_quiz_functions()  # Creating an instance of the all_plant_quiz_functions class
        results = [
            ('result1', {
                'plant_name': 'Plant1',
                'latin_name': 'Latin1',
                'class_name': 'Class1',
                'light_conditions': 'Light1',
                'soil_type': 'Soil1',
                'planting_season': ['Month1', 'Month2,', 'Month3'],
                'frequency_watering': 7
            })
        ]
        perfect_plant = results[0]

        # Mock the random.choice function to return the test data
        mock_choice.return_value = perfect_plant

        # Redirect the standard output to capture the printed output
        stdout = StringIO()
        with patch('sys.stdout', stdout):
            plantquiz.quiz_result(results)


            expected_output = """\n R-E-S-U-L-T-S
.
..
...
....
.....
....
...
..
.
The results are in!
Your perfect plant pal is:
Plant1 (Latin1). It's a class1, preferring light1 and soil1 soil.
The best months for planting are Month1, Month2, and Month3. It needs watering every 7 days.

Thanks for playing, hope this gave you some inspiration! Happy Planting :)
    """


            self.assertEqual(stdout.getvalue().strip(), expected_output.strip())

# -------------------------------------------------------------------------
# Tests run_program()

    @mock.patch('builtins.input', side_effect=["e", "d", "e", "b", "d", "d"])
    def test_run_program(self, mock_input):
        plantquiz = all_plant_quiz_functions() # Creating an instance of the all_plant_quiz_functions class
        #create StringIO object to stout output to then, later, check if expected output is within actual output
        output = StringIO()
        # continuation of above, mock.patch redirects sys.stdout to the 'output' object so output can be captured
        with mock.patch("sys.stdout", new=output):
            plantquiz.run_program()
        # this is the last line of the program if run successfully
        expected_output_snippet = "Thanks for playing, hope this gave you some inspiration! Happy Planting :)"
        # checking if the above line is in the captured output
        self.assertIn(expected_output_snippet, output.getvalue())

# -------------------------------------------------------------------------

if __name__ == '__main__':
    if __name__ == '__main__':
        unittest.main()


