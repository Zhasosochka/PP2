from datetime import datetime, timedelta

# 1
now = datetime.now() #now() gets immutable time object from OS
five_days_ago = now - timedelta(days=5)
print(f"Current date: {now.date()}")
print(f"Five days ago: {five_days_ago.date()}")

# 2
today = datetime.now().date()
yesterday = today - timedelta(days=1) #timedelta() is difference between datetime objects
tomorrow = today + timedelta(days=1)
print(f"Yesterday: {yesterday}")
print(f"Today: {today}")
print(f"Tomorrow: {tomorrow}")

# 3
with_ms = datetime.now()
without_ms = with_ms.replace(microsecond=0) # replace() creates a copy with cha*nges
print(f"Time with microseconds: {with_ms}")
print(f"Time without microseconds: {without_ms}")

# 4.
date1 = datetime(2024, 1, 20)
date2 = datetime(2024, 1, 27)
difference = date2 - date1
seconds = difference.total_seconds()

print(f"Difference in seconds: {seconds} seconds.")