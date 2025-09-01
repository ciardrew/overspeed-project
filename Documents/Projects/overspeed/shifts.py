from datetime import datetime, timedelta
import pandas as pd

format_code = "%d/%m/%Y %H:%M"
past_date = datetime(2025, 7, 1, 6, 0, 0) #6am 1st Jul 2025 - red shift beginning

shift_cycle = ['red', 'green', 'red', 'green', 'brown', 'red', 'brown', 'red', 'blue', 'brown', 'blue', 'brown', 'green', 'blue', 'green', 'blue']
shift = timedelta(hours=12)
shift_min = shift.total_seconds() / 60

def shift_finder(timestamp):
    """Returns correct shift colour based on given timestamp."""
    timestamp = datetime.strptime(timestamp, format_code)
    time_since = timestamp - past_date

    seconds_elapsed = time_since.total_seconds()
    minutes_elapsed = seconds_elapsed / 60
    
    shift_index = int(minutes_elapsed // 720) % len(shift_cycle)
    colour = shift_cycle[shift_index]
    return colour