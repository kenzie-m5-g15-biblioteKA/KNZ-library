import os
from datetime import date

import holidays


def working_day(date: date) -> bool:
    """Verifies if a given date is a working day (not a weekend or holiday).

    :param input_date: The date to check.
    :type input_date: date

    :return: True if the date is a working day, False otherwise.
    :rtype: bool
    """
    country = os.getenv("COUNTRY", "BR")
    country_holidays = holidays.country_holidays(country)

    week_day = date.weekday() < 5
    working_day = date not in country_holidays

    return week_day and working_day
