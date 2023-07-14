# Helper functions -----------------------------------------------------------------------------------------------------
from datetime import datetime
import requests
from databases.mysql_connect import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD
from databases.database import DatabaseManagement

# Used to define data from columns in plant_id table -------------------------------------------------------------------
class Plant:
    def __init__(self, plant_id, plant_name, latin_name, class_name, date_planted):
        self.plant_id = plant_id
        self.plant_name = plant_name
        self.latin_name = latin_name
        self.class_name = class_name
        self.date_planted = date_planted

# Used to define data from columns in plant_requirements table ---------------------------------------------------------
class PlantRequirements:
    def __init__(self, light_conditions, frequency_watering, soil_type, growing_time, toxicity):
        self.light_conditions = light_conditions
        self.frequency_watering = frequency_watering
        self.soil_type = soil_type
        self.growing_time = growing_time
        self.toxicity = toxicity

# Pulls all existing logbook data in main logbook table in plantsapp DB ------------------------------------------------
class UserLogbook:
    def __init__(self, user_id, load_from_db=True):
        self.user_id = user_id
        self.logbook = []

        if load_from_db:
            self.db = DatabaseManagement(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, 'plantsapp')
            self.load_logbook_from_db()
    # loads existing entries for specific user ID in logbook table in plantsapp DB -------------------------------------
    def load_logbook_from_db(self):
        select_query = """
            SELECT plant_id.id, plant_id.plant_name, plant_id.latin_name, plant_id.class_name,
                   plant_requirements.light_conditions, plant_requirements.frequency_watering,
                   plant_requirements.soil_type, plant_requirements.growing_time, plant_requirements.toxicity, 
                   logbook.date_planted
            FROM logbook
            JOIN plant_id ON logbook.plant_id = plant_id.id
            JOIN plant_requirements ON plant_id.id = plant_requirements.id
            WHERE logbook.user_id = %s
        """
        try:
            self.db.connect()  # Establish database connection
            with self.db.connection.cursor() as cursor:
                cursor.execute(select_query, (self.user_id,))
                results = cursor.fetchall()

            for result in results:
                plant_id = result[0]
                plant_name = result[1]
                latin_name = result[2]
                class_name = result[3]
                light_conditions = result[4]
                frequency_watering = result[5]
                soil_type = result[6]
                growing_time = result[7]
                toxicity = result[8]
                date_planted = result[9]
                plant = Plant(plant_id, plant_name, latin_name, class_name, date_planted)
                requirements = PlantRequirements(light_conditions, frequency_watering, soil_type, growing_time, toxicity)
                self.add_plant(plant, requirements)
        except Exception as e:
            print(f"An error occurred while loading the logbook from the database: {e}")

    # Used to add existing entries to self.logbook list ----------------------------------------------------------------
    def add_plant(self, plant, requirements):
        self.logbook.append((plant, requirements))

    # Used in PlantLogbook to remove entry from local logbook dict -----------------------------------------------------
    def remove_plant(self, plant_id):
        for entry in self.logbook:
            if entry[0].plant_id == plant_id:  # Compare plant_id with entry[0].plant_id
                self.logbook.remove(entry)
                break



# Creates instance of user logbook and performs search functions -------------------------------------------------------
class PlantLogbook:
    # Connects to DB, sets up local dict of user's logbook for them to view and access whilst on app--------------------
    def __init__(self, user_id):
        self.user_id = user_id
        self.db = DatabaseManagement(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, 'plantsapp')
        # stores each instance of a logbook made after a search has been completed
        self.user_logbooks = {}

    # pulls all existing logbook data into self.user_logbooks so user can view existing entries without searching ------
    def populate_logbook_entries(self, user_id):
        if user_id not in self.user_logbooks:
            logbook = UserLogbook(user_id)
            self.user_logbooks[user_id] = logbook

    # displays existing logbook to user if exists. displays all info from plant_id and plant_req -----------------------
    def display_logbook(self, user_id):
        if user_id in self.user_logbooks:
            logbook = self.user_logbooks[user_id]
            if logbook.logbook:
                print("\nYour Logbook:")
                for entry in logbook.logbook:
                    plant = entry[0]
                    requirements = entry[1]
                    print(f"Plant ID: {plant.plant_id}")
                    print(f"Plant Name: {plant.plant_name}")
                    print(f"Latin Name: {plant.latin_name}")
                    print(f"Class Name: {plant.class_name}")
                    print(f"Light Conditions: {requirements.light_conditions}")
                    print(f"Frequency of Watering: {requirements.frequency_watering}")
                    print(f"Soil Type: {requirements.soil_type}")
                    print(f"Growing Time: {requirements.growing_time}")
                    print(f"Toxicity: {requirements.toxicity}")
                    print(f"Date planted: {plant.date_planted}")
                    print("---------------------")
            else:
                print("Your logbook is empty.")
        else:
            print("No logbook found for the user.")
    # Search functions -------------------------------------------------------------------------------------------------
    # Main search function ---------------------------------------------------------------------------------------------
    def search_and_add_to_logbook(self, user_id):
        query = input("\nSearch for a plant by its name: ")
        results = self.search_plants(query)

        if not results:
            print("No results found.")
            return

        print("\nSearch results:")
        for index, plant in enumerate(results, start=1):
            print(f"{index}. {plant.plant_id}: {plant.plant_name}")

        while True:
            plant_index = input("\nEnter the number of the plant to add to your logbook (or 'done' to go back): ")
            if plant_index.lower().strip() == 'done':
                break

            try:
                plant_index = int(plant_index)
                if plant_index < 1 or plant_index > len(results):
                    print("Invalid plant index. Please try again.")
                    continue

                plant = results[plant_index - 1]
                requirements = self.get_plant_requirements(plant.plant_id)
                self.add_plant_to_logbook(user_id, plant, requirements)
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as e:
                print(f"Error: {e}")
                print("Plant not added to your logbook.")

    # Helper: used in search and add to logbook ------------------------------------------------------------------------
    def add_plant_to_logbook(self, user_id, plant, requirements):
        if user_id in self.user_logbooks:
            logbook = self.user_logbooks[user_id]
            for entry in logbook.logbook:
                if entry[0].plant_id == plant.plant_id:
                    print("Plant already exists in your logbook.")
                    return
            logbook.add_plant(plant, requirements)
        else:
            logbook = UserLogbook(user_id)
            logbook.add_plant(plant, requirements)
            self.user_logbooks[user_id] = logbook

        self.insert_logbook_entry(user_id, plant.plant_id, plant.date_planted)
        print("Plant added to your logbook.")

    # Helper: deletes logbook entry from local and DB ------------------------------------------------------------------
    def remove_plant_from_logbook(self, user_id, plant_id):
        if user_id in self.user_logbooks:
            logbook = self.user_logbooks[user_id]
            logbook.remove_plant(plant_id)
            self.delete_logbook_entry(user_id, plant_id)
            print("Plant removed from your logbook.")
        else:
            print("No logbook found for the user.")

    # Helper: used in search and add to logbook ------------------------------------------------------------------------
    def search_plants(self, query):
        select_query = "SELECT * FROM plant_id WHERE plant_name LIKE '%{}%'".format(query)
        try:
            self.db.connect()  # Establish database connection
            with self.db.connection.cursor() as cursor:
                cursor.execute(select_query)
                results = cursor.fetchall()

            plants = []
            for result in results:
                plant_id = result[0]
                plant_name = result[1]
                latin_name = result[2]
                class_name = result[3]
                plant = Plant(plant_id, plant_name, latin_name, class_name, date_planted=datetime.today().strftime('%Y-%m-%d'))
                plants.append(plant)

            return plants
        except Exception as e:
            print(f"An error occurred while searching plants: {e}")
            return None

    # Helper: used in search and add to logbook ------------------------------------------------------------------------
    def get_plant_by_id(self, plant_id):
        try:
            select_query = "SELECT * FROM plant_id WHERE id = %s"
            self.db.connect()  # Establish database connection
            with self.db.connection.cursor() as cursor:
                cursor.execute(select_query, (plant_id,))
                result = cursor.fetchone()

            if result:
                plant_id = result[0]
                plant_name = result[1]
                latin_name = result[2]
                class_name = result[3]
                plant = Plant(plant_id, plant_name, latin_name, class_name, date_planted=datetime.today().strftime('%Y-%m-%d'))
                return plant

            return None
        except Exception as e:
            print(f"An error occurred while fetching plant by id: {e}")
            return None

    # Helper: used in search and add to logbook ------------------------------------------------------------------------
    def get_plant_requirements(self, plant_id):
        select_query = "SELECT * FROM plant_requirements WHERE id = %s"
        try:
            self.db.connect()  # Establish database connection
            with self.db.connection.cursor() as cursor:
                cursor.execute(select_query, (plant_id,))
                result = cursor.fetchone()

            if result:
                light_conditions = result[1]
                frequency_watering = result[2]
                soil_type = result[3]
                growing_time = result[4]
                toxicity = result[5]
                requirements = PlantRequirements(light_conditions, frequency_watering, soil_type, growing_time,
                                             toxicity)
                return requirements

            return None
        except Exception as e:
            print(f"An error occurred while fetching plant requirements: {e}")
            return None

    # Helper: used in search and add to logbook ------------------------------------------------------------------------
    def insert_logbook_entry(self, user_id, plant_id, date_planted):
        insert_query = "INSERT INTO logbook (user_id, plant_id, date_planted) VALUES (%s, %s, %s)"
        self.db.connect()  # Establish database connection
        with self.db.connection.cursor() as cursor:
            cursor.execute(insert_query, (user_id, plant_id, date_planted))
            self.db.connection.commit()

    # Delete logbook entry from logbook table on DB --------------------------------------------------------------------
    def delete_logbook_entry(self, user_id, plant_id):
        try:
            delete_query = "DELETE FROM logbook WHERE user_id = %s AND plant_id = %s;"
            self.db.connect()  # Establish database connection
            with self.db.connection.cursor() as cursor:
                cursor.execute(delete_query, (user_id, plant_id))
                self.db.connection.commit()
            print("Plant removed from your logbook.")
        except Exception as e:
            print(f'Error: {e}')


# Logbook menu for homepage --------------------------------------------------------------------------------------------
def run_logbook(user_id):
    plant_logbook = PlantLogbook(user_id)

    while True:
        print("\n----- Logbook and Plant Search Menu -----")
        print("1. Search and Add Plant to Logbook")
        print("2. Remove Plant from Logbook")
        print("3. View Logbook")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            plant_logbook.search_and_add_to_logbook(user_id)
        elif choice == "2":
            plant_id = input("Enter the plant ID to remove from your logbook: ")
            plant_logbook.remove_plant_from_logbook(user_id, plant_id)
        elif choice == "3":
            plant_logbook.populate_logbook_entries(user_id)
            plant_logbook.display_logbook(user_id)
        elif choice == "4":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")