from database import get_doctors

doctor_cache = None


def get_cached_doctors():
    global doctor_cache

    if doctor_cache is None:
        print("CACHE MISS - Loading doctors from SQLite")
        doctor_cache = get_doctors()
    else:
        print("CACHE HIT - Loading doctors from memory")

    return doctor_cache


def clear_cache():
    global doctor_cache
    doctor_cache = None