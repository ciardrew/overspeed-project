# Shift work
from datetime import datetime, timedelta

# 1st July 2025 (Tuesday - Red Shift beginning)
past_date = datetime(2025, 7, 1, 6, 0, 0) #6am 1st Jul 2025
current_date = datetime.now()
print(past_date)
print(current_date)

time_since = current_date - past_date

seconds_elapsed = time_since.total_seconds()
minutes_elapsed = seconds_elapsed / 60
hours_elapsed = seconds_elapsed / 3600
days_elapsed = seconds_elapsed / 86400

print(f"Seconds elapsed: {seconds_elapsed:.2f}")
print(f"Minutes elapsed: {minutes_elapsed:.2f}")
print(f"Hours elapsed: {hours_elapsed:.2f}")
print(f"Days elapsed: {days_elapsed:.2f}")

shift_cycle = ['red', 'green', 'red', 'green', 'brown', 'red', 'brown', 'red', 'blue', 'brown', 'blue', 'brown', 'green', 'blue', 'green', 'blue']
shift = timedelta(hours=12)
shift_min = shift.total_seconds() / 60

place_in_cycle = days_elapsed % 8
print(f"{place_in_cycle:.4f}")

#each shift is 12 hours = 720 minutes
shift_index = int(minutes_elapsed // 720) % len(shift_cycle)
colour = shift_cycle[shift_index]

print(f"Shift index: {shift_index}")
print(f"Assigned colour: {colour}")