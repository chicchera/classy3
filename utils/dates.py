from datetime import datetime, timedelta

# Function to convert Unix UTC timestamp to Python datetime object
def convert_unix_utc_to_datetime(unix_utc):
    """
    Convert a Unix timestamp in UTC to a datetime object.
    Parameters:
        unix_utc (float): The Unix timestamp in UTC.
    Returns:
        datetime: The corresponding datetime object.
    """
    return datetime.utcfromtimestamp(unix_utc)

# Function to get the start of a day (UTC time)
def get_start_of_day(dt):
    """
    Replace the hour, minute, second, and microsecond components of the given datetime object
    with zero to get the start of the day.
    Parameters:
        dt (datetime): The datetime object for which the start of the day needs to be calculated.
    Returns:
        datetime: A new datetime object with the hour, minute, second, and microsecond components set to zero.
    """
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

# Function to get the end of a day (UTC time)
def get_end_of_day(dt):
    """
    Returns a DateTime object representing the end of the day for the given DateTime object.
    Parameters:
        dt (DateTime): The DateTime object for which to find the end of the day.
    Returns:
        DateTime: A new DateTime object with the hour set to 23, the minute set to 59, the second set to 59, and the microsecond set to 999999.
    """
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)

# Function to get the start of a month (UTC time)
def get_start_of_month(dt):
    """
    Generate the start of the month for the given date.
    Args:
        dt (datetime): The input date.
    Returns:
        datetime: The start of the month for the given date.
    """
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

# Function to get the end of a month (UTC time)
def get_end_of_month(dt):
    """
    Calculates the end of the month for the given date.
    Args:
        dt (datetime): The date to calculate the end of the month for.
    Returns:
        datetime: The end of the month for the given date.
    """
    next_month = dt.replace(day=28) + timedelta(days=32)
    return get_start_of_month(next_month) - timedelta(seconds=1)

# Function to get the difference in days between two UTC dates
def get_days_difference(start_dt, end_dt):
    """
    Calculate the difference in days between two given dates.
    Parameters:
        start_dt (datetime): The start date.
        end_dt (datetime): The end date.
    Returns:
        int: The number of days between the start and end dates.
    """
    delta = end_dt - start_dt
    return delta.days

def datetime_to_utc_int(dt):

    """
    Converts a given datetime object to a UTC timestamp.
    Parameters:
        dt (datetime): The datetime object to be converted.
    Returns:
        int: The UTC timestamp of the given datetime object.
    """
    return int(dt.timestamp())



def GetFirstDayUtc(timestamp):

    # get the date of the current timestamp
    date = datetime.datetime.fromtimestamp(timestamp).date()

    # get the start of the first day of the month
    first_day_month = datetime.date(date.year, date.month, 1)

    # convert it to a utc timestamp
    return first_day_month.timestamp()


