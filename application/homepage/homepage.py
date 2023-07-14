# Helper functions -----------------------------------------------------------------------------------------------------
import subprocess
from application.logbook.logbook import run_logbook


# Homepage -------------------------------------------------------------------------------------------------------------
def exit_app():
    print('\nSee you next time!')
    print('********** APP CLOSED **********')
    raise SystemExit

class HomePage:
    def __init__(self, user_id):
        self.user_id = user_id

    def main_menu_options(self):
        while True:
            print("\nWelcome back, please choose from the following options:")
            print("1. Search and Store")
            print("2. Weather")
            print("3. Quote of the Day")
            print("4. Plant Quiz")
            print("5. Exit")
            choice = input("\nEnter your choice (1-5): ")
            if choice in ('1', '2', '3', '4', '5'):
                return choice
            else:
                print('\nInvalid choice. Please select 1, 2, 3, 4, or 5.')
                continue

    def run_main_menu(self):
        while True:
            choice = self.main_menu_options()

            if choice == '1':
                run_logbook(self.user_id)

            elif choice == '2':
                self.view_weather()

            elif choice == '3':
                self.get_random_quote()

            elif choice == '4':
                self.do_plant_quiz()

            elif choice == '5':
                exit_app()

            else:
                print("\nInvalid choice. Please enter 1, 2, 3, 4, or 5.")

    def search_plant(self):
        from application.search.plantsearch import MainPlantSearch
        plant_search = MainPlantSearch()  # Instantiate the MainPlantSearch class
        plant_search.user_plant_search()  # Call the user_plant_search() method


    def view_weather(self):
        from application.weather.todays_weather import main_weather_program

        while True:
            main_weather_program()
            choice = input("\nEnter 'm' to return to the main menu or any other key to view weather again: ")
            if choice.lower() == 'm':
                break

    def get_random_quote(self):
        subprocess.run(["python", "application/quotations/randomquote.py"])

    def do_plant_quiz(self):
        subprocess.run(["python", "application/plantquiz/plantquizfunctions.py"])

