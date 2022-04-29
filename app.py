from flask import Flask, make_response, request
import time
import sys
import os
import io

# Global variables
SECONDS = 60
YEAR = 2022
TIME_1 = '%I %M %p %Y %d'
TIME_2 = '%I %M %p %Y'

app = Flask(__name__)
debug = True

@app.route('/')
def form():
    return """
       <html>
        <head >
           <title>Rajesh👨‍🎓 CPL Project</title>

        
        </head>
        <body style="
        width: 100%;
margin: auto;
  margin-top: auto;
max-width: 438px;
font-size: 24px;
font-family: serif;
box-shadow: blue 0px 0px 0px 2px inset, rgb(255, 255, 255) 10px -10px 0px -3px, rgb(31, 193, 27) 10px -10px, rgb(255, 255, 255) 20px -20px 0px -3px, rgb(255, 217, 19) 20px -20px, rgb(255, 255, 255) 30px -30px 0px -3px, rgb(255, 156, 85) 30px -30px, rgb(255, 255, 255) 40px -40px 0px -3px, rgb(255, 85, 85) 40px -40px;
padding: 26px;
margin-top: 66px;
"
>
            <div>
            <h3>CPL Course Project </h3>
            <div class="container">
                <div>
                <div>
                    <div>
                    <form
                        method="post" enctype="multipart/form-data"
                        action="/parser"
                        id="login-form" >
                        <h2>Upload Parser File</h2>
                        <input type="file" name="data_file" />
                        <input type="submit" />
                        <br><p>Rajesh Pasumarthi</p>
                        <p>CSU ID: 2832688</p>
                    </form>
                    </div>
                </div>
                </div>
            </div>
            </div>
        </body>
        </html>
    """

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

@app.route('/parser', methods=["POST"])
def main_funtion():
    f = request.files['data_file']
    if not f:
        return "Provide Input file"
    filename = f.filename
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    log_A = ''
    for x in stream.readlines():
        log_A = log_A+''+x.lower()
    open = log_A.find("time log:")
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
    print ( f.filename + " - " + str(total_hrs) +
          " hours " + str(total_min) + "  minutes")
    return ( f.filename + " - " + str(total_hrs) +
          " hours " + str(total_min) + "  minutes")