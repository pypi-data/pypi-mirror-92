#!/usr/bin/python3
import os
import sys
import time
import keyboard
import datetime
import pyperclip

location = sys.argv[0]
os.system("clear")

if not os.path.isfile(location.replace("__main__.py", "") + "schedule.csv"):
    with open(location.replace("__main__.py", "") + "schedule.csv", "w+") as f:
        import requests
        schedule = requests.get("https://raw.githubusercontent.com/DogAteMyCode/autozoom/master/schedule.csv").text
        f.write(schedule)
def print_schedule():
    from texttable import Texttable
    location_inner = sys.argv[0].replace(__name__, "").strip(".py")
    with open(location_inner + "schedule.csv", "r") as csvfile:
        csvTable = []
        for row in csvfile.read().split("\n"):
            csvTable.append(row.split(","))
    tableList = []
    colsDType = []
    colSize = []
    table = Texttable()
    for column in csvTable[0]:
        colsDType.append('t')
        colSize.append(10)
    table.set_cols_dtype(colsDType)
    table.set_cols_width(colSize)
    table.set_max_width(400)

    for row in csvTable:
        table.add_row(row)

    print(table.draw())

print("If you want to add your schedule run with -v flag\nto stop use ^c (control+c) keyboardInterrupt\n")
try:
    sys.argv.index("-v")
    v = True
except ValueError:
    v = False
    pass
if v:
    if sys.platform == "darwin":
        print("Appliciation won't start untill the .csv editor is fully closed")
        os.system("open "+location.replace("__main__.py", "") + "schedule.csv -W")
    else:
        print("only works in OS X")
print("Started")
print_schedule()

with open(location.replace("__main__.py", "") + "schedule.csv", "r+") as f:
    rows = [row.strip('\n').split(",") for row in f.readlines()]
columns = []
column_count = len(rows[0])
column = []
for i in range(column_count):
    for row in rows:
        column.append(row[i])
    columns.append(column)
    column = []
hour_dict = {"*":""}
for column in columns:
    hour_dict[column.pop(0)] = column
while True:
    while True:
        time.sleep(60)
        now = datetime.datetime.now()
        hour = now.strftime('%H:%M')
        if hour.startswith("0"):
            hour = hour.replace("0", "", 1)
        hour_classes = hour_dict.get(hour, "")
        if hour_classes != "":
            meetCode = (hour_classes[now.weekday()])
            if meetCode != "":
                break

    os.system("clear")
    print("If you want to add your schedule run with -v flag\nto stop use ^c (control+c) keyboardInterrupt\n")
    print(meetCode)
    os.system("open -a /Applications/zoom.us.app &")
    time.sleep(2)
    keyboard.press_and_release('command+j')
    time.sleep(1)
    keyboard.press_and_release('command+a')
    keyboard.press_and_release('delete')
    time.sleep(1)
    pyperclip.copy(meetCode)
    keyboard.write(meetCode)
    keyboard.press_and_release('enter')
