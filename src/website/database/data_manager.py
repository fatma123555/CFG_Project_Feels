try:
    from src.website.database.feels_database import FeelsDatabase
except Exception as e:
    print("Some modules are missing {}".format(e))
from src.website.database.feels_database import FeelsDatabase
feels_database = FeelsDatabase()

"""
    This method is essentially a getter method for the main moods return function from the feels_database
"""


def get_all_moods():
    return feels_database.get_main_moods()


""" 
    This function will create a dictionary of the main moods and its submoods as a list within each entry
"""


def build_moods_dict():
    main_moods = feels_database.get_main_moods()
    all_moods = dict()
    for main_mood in main_moods:
        all_moods[main_mood] = feels_database.get_sub_moods(main_mood)
    return all_moods


"""
    These are the key variables that are necessary to build the choices for the quiz forms
"""
all_moods = build_moods_dict()
main_moods_tuples = zip(feels_database.get_main_moods(), feels_database.get_main_moods())
