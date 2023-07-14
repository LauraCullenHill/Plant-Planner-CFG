import requests
import json
from datetime import datetime
import calendar
import random
import time
from images.ascii_art import ascii_plant_quiz, ascii_flower_d

# Intro to Main Quiz
class IntroQuiz:
    def __init__(self):
        pass

    def start(self):
        ascii_plant_quiz()
        ascii_flower_d()
        time.sleep(1)
        print('                  🄿 🄻 🄰 🄽 🅃  🅀 🅄 🄸 🅉')
        time.sleep(1)
        print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        time.sleep(1.5)
        print("So you're all geared up and ready to garden but there's just one thing...how to decide what to plant:")
        time.sleep(1.5)
        print("Here's a handy quick quiz to get you started.")
        time.sleep(1.5)
        print("Know your requirements already? No problem!")
        time.sleep(1.5)
        print("Press 'q' at any point to head back to the main menu and check out the Plant Search page.")
        time.sleep(1.5)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        time.sleep(2.5)

intro_quiz = IntroQuiz()
intro_quiz.start()

# main class for all plant quiz functions
class all_plant_quiz_functions():
    JSON_URL = 'https://raw.githubusercontent.com/RubyBlues/Project/main/plantjsondata.json'
    def __init__(self):
        # Fetch JSON data from the URL
        response = requests.get(self.JSON_URL)
        self.plant_data = json.loads(response.text)

    # helper function for q1
    def is_choice_in_plant_info_json(self, choice, category):
        results = [(plant_id, plant_info) for plant_id, plant_info in self.plant_data.items() if choice in plant_info[category]]
        return results

    # helper function for q2-q4, q6
    def is_choice_in_plant_info(self, choice, results, category):
        results = [(plant_id, plant_info) for plant_id, plant_info in results if choice in plant_info[category]]
        return results

    # Plant Quiz Questions split into functions: q1 through q6
    def q1(self):
        while True:
            print("Question 1:")
            time.sleep(1)
            print("First things first, what type of plant are you looking for?")
            time.sleep(1)
            print("a) Fruit \nb) Flower \nc) Shrub \nd) Vegetable \ne) Don't mind")
            choice = input("Choose a, b, c, d or e \n")
            category = 'class_name'

            if choice.lower() == 'a':
                choice = 'Fruit'
                return self.is_choice_in_plant_info_json(choice, category)

            elif choice.lower() == 'b':
                choice = 'Flower'
                return self.is_choice_in_plant_info_json(choice, category)

            elif choice.lower() == 'c':
                choice = 'Shrub'
                return self.is_choice_in_plant_info_json(choice, category)

            elif choice.lower() == 'd':
                choice = 'Vegetable'
                return self.is_choice_in_plant_info_json(choice, category)

            elif choice.lower() == 'e':
                results = [(plant_id, plant_info) for plant_id, plant_info in self.plant_data.items()]
                return results

            elif choice.lower() == 'q':
                print("Thanks for playing, Happy Planting :)")
                return None
            else:
                print("Invalid choice, please select from one of the listed options")
                time.sleep(1)

    def q2(self, results):
        while True:
            print("Question 2:")
            time.sleep(1)
            print("So thinking a bit about the planting location now, how much light does it get?")
            time.sleep(1)
            print("a) Full sun \nb) Partial shade \nc) Shade \nd) Skip")
            choice = input("Choose a, b, c or d \n")
            category = 'light_conditions'

            if choice.lower() == 'a':
                choice = 'Full sun'
                return self.is_choice_in_plant_info(choice, results, category)

            elif choice.lower() == 'b':
                choice = 'Partial shade'
                return self.is_choice_in_plant_info(choice, results, category)

            elif choice.lower() == 'c':
                choice = 'Shade'
                return self.is_choice_in_plant_info(choice, results, category)

            elif choice.lower() == 'd':
                return results

            elif choice.lower() == 'q':
                print("Thanks for playing, Happy Planting :)")
                return None

            else:
                print("Invalid choice, please select from one of the listed options")
                time.sleep(1)

    def q3(self, results):
        while True:
            print("Question 3:")
            time.sleep(1)
            print("Thinking a bit more about that location, what's the soil like?")
            time.sleep(1)
            print("a) Well drained \nb) Loamy \nc) Acidic \nd) Moist \ne) Skip")
            choice = input("Choose a, b, c, d or e\n")
            category = 'soil_type'
            if choice.lower() == 'a':
                choice = 'Well drained'
                return self.is_choice_in_plant_info(choice, results, category)

            elif choice.lower() == 'b':
                choice = 'Loamy'
                return self.is_choice_in_plant_info(choice, results, category)

            elif choice.lower() == 'c':
                choice = 'Acidic'
                return self.is_choice_in_plant_info(choice, results, category)

            elif choice.lower() == 'd':
                choice = 'Moist'
                return self.is_choice_in_plant_info(choice, results, category)

            elif choice.lower() == 'e':
                return results

            elif choice.lower() == 'q':
                print("Thanks for playing, Happy Planting :)")
                return None

            else:
                print("Invalid choice, please select from one of the listed options")
                time.sleep(1)

    def q4(self, results):
        while True:
            print("Question 4:")
            time.sleep(1)
            print("Are you just looking for some inspiration or do you want to plant something this month?")
            time.sleep(1)
            print("a) This month! \nb) Just browsing")
            choice = input("Choose a or b\n")
            category = 'planting_season'

            if choice.lower() == 'a':
                month = calendar.month_name[datetime.now().month]
                choice = month
                return self.is_choice_in_plant_info(choice, results, category)

            elif choice.lower() == 'b':
                return results

            elif choice.lower() == 'q':
                print("Thanks for playing, Happy Planting :)")
                return None

            else:
                print("Invalid choice, please select from one of the listed options")
                time.sleep(1)

    def q5(self, results):
        while True:
            print("Question 5:")
            time.sleep(1)
            print("Got time on your hands? How often are you prepared to water your plant pal?")
            time.sleep(1)
            print("a) Every day \nb) Every few days \nc) Maximum of once a week \nd) Skip")
            choice = input("Choose a, b, c or d \n")

            if choice.lower() == 'a' or choice.lower() == 'd':
                return results

            elif choice.lower() == 'b':
                choice = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
                results = [(plant_id, plant_info) for plant_id, plant_info in results if plant_info['frequency_watering'] in choice]
                return results

            elif choice.lower() == 'c':
                choice = [7, 8, 9, 10, 11, 12, 13, 14]
                results = [(plant_id, plant_info) for plant_id, plant_info in results if plant_info['frequency_watering'] in choice]
                return results

            elif choice.lower() == 'q':
                print("Thanks for playing, Happy Planting :)")
                return None

            else:
                print("Invalid choice, please select from one of the listed options")
                time.sleep(1)

    def q6(self, results):
        while True:
            print("Question 6:")
            time.sleep(1)
            print("Nearly there... Any small creatures of the two or four leg variety? Not all plants are friendly to humans or dogs/cats.")
            time.sleep(1)
            print("Do you need a plant that is: \na) Non-toxic \nb) Just non-toxic to animals \nc) Just non-toxic to humans \nd) Doesn't matter")
            choice = input("Choose a, b, c or d \n")
            category = 'toxicity'

            if choice.lower() == 'a':
                choice = 'None'
                return self.is_choice_in_plant_info(choice, results, category)

            elif choice.lower() == 'b':
                choice = 'Humans'
                return self.is_choice_in_plant_info(choice, results, category)

            elif choice.lower() == 'c':
                choice = 'Animals'
                return self.is_choice_in_plant_info(choice, results, category)

            elif choice.lower() == 'd':
                return results

            elif choice.lower() == 'q':
                print("Thanks for playing, Happy Planting :)")
                return None

            else:
                print("Invalid choice, please select from one of the listed options")
                time.sleep(1)

    def quiz_result(self, results):
        perfect_plant = random.choice(results)
        print("\n R-E-S-U-L-T-S")
        time.sleep(1)
        print(".")
        time.sleep(0.25)
        print("..")
        time.sleep(0.25)
        print("...")
        time.sleep(0.25)
        print("....")
        time.sleep(0.25)
        print(".....")
        time.sleep(0.25)
        print("....")
        time.sleep(0.25)
        print("...")
        time.sleep(0.25)
        print("..")
        time.sleep(0.25)
        print(".")
        print("The results are in!")
        time.sleep(0.5)
        plant_name = perfect_plant[1]['plant_name']
        latin_name = perfect_plant[1]['latin_name']
        class_name = perfect_plant[1]['class_name']
        light_conditions = perfect_plant[1]['light_conditions']
        soil_type = perfect_plant[1]['soil_type']
        planting_season = perfect_plant[1]['planting_season']
        month1 = planting_season[0]
        month2 = planting_season[1]
        month3 = planting_season[2]
        frequency_watering = perfect_plant[1]['frequency_watering']
        print("Your perfect plant pal is:")
        time.sleep(1)
        print(f"{plant_name} ({latin_name}). It's a {class_name.lower()}, preferring {light_conditions.lower()} and {soil_type.lower()} soil.")
        print(f"The best months for planting are {month1}, {month2} and {month3}. It needs watering every {frequency_watering} days.")
        time.sleep(3)
        print("")
        print("Thanks for playing, hope this gave you some inspiration! Happy Planting :)")

    # Helper function for run_program to check if results is every empty and if so,
    # to inform the user and restart the quiz
    def check_results(self, results):
        if len(results) == 0:
            print("Uh-oh, looks like we don't have anything that ticks all your boxes. Please try again.")
            return False
        return True

    # Collation of above functions (and their helper functions) to run the program, also includes a check
    # (if results is None) which checks if 'q' has been entered by the user, and if so, quits
    def run_program(self):
        while True:
            results = self.q1()
            if results is None:
                return
            if not self.check_results(results):
                continue

            results = self.q2(results)
            if results is None:
                return
            if not self.check_results(results):
                continue

            results = self.q3(results)
            if results is None:
                return
            if not self.check_results(results):
                continue

            results = self.q4(results)
            if results is None:
                return
            if not self.check_results(results):
                continue

            results = self.q5(results)
            if results is None:
                return
            if not self.check_results(results):
                continue

            results = self.q6(results)
            if results is None:
                return
            if not self.check_results(results):
                continue

            self.quiz_result(results)
            return

plant_quiz = all_plant_quiz_functions()
plant_quiz.run_program()
