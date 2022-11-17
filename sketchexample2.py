import schedule
import time
import datetime as dt

def runtime():
    print(dt.datetime.now())

schedule.every().day.at("14:56:00").do(runtime)

while True:
    schedule.run_pending()