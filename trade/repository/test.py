import datetime
import pytz

# Get the current time in your local time zone
local_time = datetime.datetime.now()

# Specify the New York time zone
new_york_timezone = pytz.timezone('America/New_York')

# Convert the local time to New York time
new_york_time = local_time.astimezone(new_york_timezone)

print("Current Time (New York):", new_york_time)