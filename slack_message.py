#!/usr/bin/env python
import subprocess
import slack_sdk
import re
import markdown
import json

import time

def sendSlackMessage(message, details):
    token = "xoxb-3719420712373-3719431388853-6DOHuR4bq0XVLMBnguqdqC0i"
    client = slack_sdk.WebClient(token=token)

    response = client.chat_postMessage(
        channel="alerts",
        text=message
    )
    print("Request was succesfull:" + str(response["ok"]))

    # replying in thread
    for detail in details:
        s = listToString(detail)
        response = client.chat_postMessage(
                channel="alerts",
                text='```' + s + '```',
                thread_ts=response["ts"],
        )
        print("Request was succesfull:" + str(response["ok"]))

def main():
    while True:
        exit_code = subprocess.call('./bash_command.sh')
        print(exit_code)

        message = 'No deadlock found'
        f = open("thread-dump.txt")
        lines = f.readlines()
        details = []
        for _, line in enumerate(lines):
            try:
                text = line.replace("\n","")
                details.append(text)
            except StopIteration:
                exit()
        sub_details_array = getSubArray(details)
        if len(sub_details_array) > 0:
            message = details[len(details)-1]
        sendSlackMessage(message, sub_details_array)
        time.sleep(10) # will sleep for 10 seconds

def getSubArray(details):
    line1 = re.compile(r'^Found.*Java-level deadlock[s]?:$')
    line2 = re.compile(r'^Java stack information for the threads listed above:$')
    start_index = -1
    end_index = -1
    sub_details_array = []
    for i in range(len(details)):
        if re.match(line1, details[i]):
            start_index = i
        if re.match(line2, details[i]):
            end_index = i
        if start_index > -1 and end_index > -1:
            x = slice(start_index, end_index)
            sub_details_array.append(details[x])
            start_index = -1
            end_index = -1
    return sub_details_array   

def listToString(lines):
    s = ""
    for line in lines:
        s += line + "\n"
    return s

if __name__ == "__main__":
    main()
