# Helper functions -----------------------------------------------------------------------------------------------------
from application.homepage.homepage import exit_app
from databases.database import PlantDataManager, DatabaseManagement
from images.ascii_art import ascii_search_store


# General search ----------------------------------------------
class Search:
    def search_plants(self, plant_data, query):
        results = []
        for plant_id, plant_info in plant_data.items():
            if query.lower() in plant_info['plant_name'].lower():
                results.append((plant_id, plant_info['plant_name']))
        return results


# Name search ----------------------------------------------
class NameSearch(Search):
    def search_plants_by_name(self):
        plant_name = self.get_plant_name_for_search()
        connection = None
        try:
            connection = DatabaseManagement.connect
            cursor = connection.cursor()
            cursor.execute("USE plantsapp;")
            cursor.execute(f"SELECT id.id, id.plant_name FROM plant_id id WHERE id.plant_name LIKE '%{plant_name}%';")
            result = cursor.fetchall()
            return [result for result in result]
        except Exception as exc:
            print(f'Error in connecting to db: {exc}')
        finally:
            if connection:
                connection.close()

    def get_plant_name_for_search(self):
        return input('\nEnter the plant name you want to search for: ')


# Type search ----------------------------------------------
class TypeSearch(Search):
    @staticmethod
    def type_of_plant_search():
        try:
            while True:
                ascii_search_store()
                print("\nSelect the type of plant search: ")
                print("1. Search by common name")
                print("2. Search by planting conditions")
                print("3. Exit app")
                choice = input("\nEnter your choice (1, 2, or 3): ")
                if choice.strip() in ['1', '2']:
                    return choice
                elif choice.strip() == '3':
                    exit_app()
                else:
                    print('\nInvalid choice. Please select 1, 2 or 3.')
                    continue
        except Exception as exc:
            print(f'Problem with main menu: {exc}')  # once we debug we can make custom exception for this if needed


# Requirement search ---------------------------
class RequirementSearch(Search):
    def search_by_requirement(self):
        req = self.what_requirement()
        user_conditions = self.get_data_for_search_query(req)
        connection = None
        try:
            connection = PlantDataManager.connect_to_plantapp()
            cursor = connection.cursor()
            cursor.execute("USE plantsapp;")
            cursor.execute(
                f"SELECT id.id, id.plant_name FROM plant_id id INNER JOIN plant_requirements req ON id.id = req.id WHERE req.{req} = {user_conditions};"
            )
            result = cursor.fetchall()
            return [result for result in result]
        except Exception as exc:
            print(f'Error in connecting to db: {exc}')
        finally:
            if connection:
                connection.close()

    @staticmethod
    def what_requirement():
        while True:
            print('Select the requirement you want to search by: ')
            print('1. Light conditions')
            print('2. Watering frequency (days)')
            print('3. Soil type')
            print('4. Growing time (days)')
            print('5. Toxicity')
            req = input('\nEnter your choice (1, 2, 3, 4, or 5): ').strip()
            if req == '1':
                req = 'light_conditions'
                return req
            elif req == '2':
                req = 'frequency_watering'
                return req
            elif req == '3':
                req = 'soil_type'
                return req
            elif req == '4':
                req = 'growing_time'
                return req
            elif req == '5':
                req = 'toxicity'
                return req
            else:
                print('\nInvalid choice. Please enter 1, 2, 3, 4, or 5.\n')

    def get_data_for_search_query(self, req):
        if req == 'frequency_watering':
            user_conditions = int(
                input('\nPlease enter how frequently you want to water your plants in days: ').strip())
            return user_conditions
        elif req == 'growing_time':
            user_conditions = int(input('\nPlease enter the amount of days you want for growing time: ').strip())
            return user_conditions
        else:
            user_conditions = input('\nPlease enter the growing conditions: ')
            user_conditions = f'\'{user_conditions}\''
            return user_conditions

    def search_string_req_data(self, req, user_conditions):
        connection = None
        try:
            connection = PlantDataManager.connect_to_plantapp()
            cursor = connection.cursor()
            cursor.execute("USE plantsapp;")
            cursor.execute("""SELECT id. id, id.plant_name FROM plant_id id
        INNER JOIN 
        plant_requirements req
        ON 
        id.id = req.id
        WHERE req.{}
        LIKE '%{}%';""".format(req, user_conditions))
            result = cursor.fetchall()
            return [result for result in result]
        except Exception as exc:
            print(f'Error in connecting to db: {exc}')
        finally:
            if connection:
                connection.close()

    def search_int_req_data(self, req, user_conditions):
        connection = None
        try:
            connection = PlantDataManager.connect_to_plantapp()
            cursor = connection.cursor()
            cursor.execute("USE plantsapp;")
            cursor.execute("""SELECT id. id, id.plant_name FROM plant_id id
        INNER JOIN 
        plant_requirements req
        ON 
        id.id = req.id
        WHERE req.{} = {};""".format(req, user_conditions))
            result = cursor.fetchall()
            return [result for result in result]
        except Exception as exc:
            print(f'Error in connecting to db: {exc}')
        finally:
            if connection:
                connection.close()


# Menu ---------------------------
class MainPlantSearch(Search):
    def user_plant_search(self):
        choice = TypeSearch.type_of_plant_search()
        counter = 1
        plant_ids = []
        if choice == '1':
            plants_to_grow = NameSearch().search_plants_by_name()
            if plants_to_grow is None:
                print('\nSorry, there are no results for your query.')
            else:
                print('\nThese plants match your search: ')
                for plants in plants_to_grow:
                    print(f'{counter}. {plants[1]}')
                    plant_ids.append(plants[0])
                    counter += 1
                choice = input(f'\nWhich plant would you like to add to your logbook? Enter 1 - {counter - 1}: ')
                if int(choice) in range(1, counter):
                    choice = plant_ids[int(choice) - 1]
                    return choice
                else:
                    print('Error in finding plant_ID in user_plant_search()')
                    exit_app()
        if choice == '2':
            plants_to_grow = RequirementSearch().search_by_requirement()
            if plants_to_grow is None:
                print('\nSorry, there are no results for your query.')
            else:
                print('\nYou can grow these plants: ')
                for plants in plants_to_grow:
                    print(f'{counter}. {plants[1]}')
                    plant_ids.append(plants[0])
                    counter += 1
                choice = input(f'\nWhich plant would you like to add to your logbook? Enter 1 - {counter - 1}: ')
                if int(choice) in range(1, counter):
                    choice = plant_ids[int(choice) - 1]
                    return choice
                else:
                    print('Error in finding plant_ID in user_plant_search()')
                    exit_app()


    def plant_search_results(self, plant_options):
        # Plant search results if loop
        counter = 1
        plant_ids = []
        if plant_options is None:
            print('\nSorry there are no results for your query.')
        else:
            print('\nThese plants match your search: ')
            for plants in plant_options:
                print(f'{counter}. {plants[1]}')
                plant_ids.append(plants[0])
                counter += 1
            choice = input(f'\nWhich plant would you like to add to your logbook? Enter 1 - {counter - 1}: ')
            if int(choice) in range(1, counter):
                choice = plant_ids[int(choice) - 1]
                return choice
            else:
                print('Error in finding plant_ID in user_plant_search()')
                exit_app()
