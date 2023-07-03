from datetime import date

def working_day(date: date) -> bool:
    """Returns boolean to date check if not weekend
    :params
        date: date format to check if is not weekend
    """
    return date.weekday() < 5
