from src.website.database.feels_database import get_main_moods, get_sub_moods
from src.website import database

def get_all_moods():
    return get_main_moods()

def build_moods_dict():
    main_moods = get_main_moods()
    all_moods = dict()
    for main_mood in main_moods:
        all_moods[main_mood] = get_sub_moods(main_mood)
    return all_moods

all_moods = build_moods_dict()
main_moods_tuples = zip(get_main_moods(), get_main_moods())