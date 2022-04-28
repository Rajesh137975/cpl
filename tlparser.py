import time
import sys
import os

# Global variables
SECONDS = 60
YEAR = 2022
TIME_1 = '%I %M %p %Y %d'
TIME_2 = '%I %M %p %Y'

def readTime(s, v , content ):
    index = content.find(v)
    length = len(v)
    while index != -1:
        content = content[:index] + \
            s + content[index + length :]
        index = content.find(v)
    return content

def readLine(line, separator):
    list_ = []
    l = line.find(separator)
    while l != -1:
        list_.append(line[:l])
        line = line[l + len(separator):]
        l = line.find(separator)
    list_.append(line)
    return list_

def calcTime(type_,format_, minute, hour ):
    hour = str(hour)
    minute = str(minute)
    if type_:
        return time.mktime(time.strptime( hour + " " + minute + " " + format_ + " " + str(YEAR) + " 2", TIME_1))
    else:
        return time.mktime(time.strptime( hour + " " + minute + " " + format_ + " " + str(YEAR), TIME_2))

def GetTimePeriod(line):
    difference_time = 0
    list_ = list()
    i = line.find(":")
    while i != -1:
        list_.append(line[:i])
        line = line[i + len(":"):]
        i = line.find(":")
    list_.append(line)
    temp = list_
    if len(temp) > 1 and len(temp[0]) <= 2:
        h2 = int(temp[1].split("-")[1])
        mB = temp[2][2:4]
        mA = temp[1][2:4]
        m1 = int(temp[1][:2])
        h1 = int(temp[0])
        m2 = int(temp[2][:2])
    elif len(temp) >= 3 and len(temp[0]) > 2:
        mA = temp[2][2:4]
        mB = temp[3][2:4]
        h1 = int(temp[1])
        m2 = int(temp[3][:2])
        h2 = int(temp[2].split("-")[1])
        m1 = int(temp[2][:2])
    list_length = len(temp)
    if list_length >= 3:
        t1 = calcTime(False,mA, m1, h1 )
        if (mA == "pm" and mB == "am") or (mA == "PM" and mB == "AM"):
            t2 = calcTime(True, mB, m2, h2 )             
        else:
            t2 = calcTime( False,mB, m2, h2 )
        difference_time = abs(t2 - t1) / SECONDS
    return difference_time

if __name__ == '__main__':
    file_name = sys.argv[1]
    with open(file_name, "r") as f:
        log_A = f.read().lower()
    print(log_A)
    open = log_A.find("time log:")
    print('..',open)
    total_hrs = 0
    total_min = 0
    try:
        if open != -1:
            logs = log_A[open + 10:]
            logs = readTime(""," ",logs)
            parsed_line = readLine(logs, "\n")
            final_time = 0
            log_line = 1
            for i in parsed_line:
                final_time += GetTimePeriod(i)
                log_line += 1

            total_hrs = int(final_time // SECONDS)
            total_min = int(final_time % SECONDS)
    except Exception as e:
        print("Error: ", e)
        exit(0)
    print(file_name[:-4] + " - " + str(total_hrs) +
          " hour(s) " + str(total_min) + " and minute(s)")
