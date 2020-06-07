import datetime
import re
import os
import winsound
import time
# written by tom cohen
date = str(datetime.datetime.now())
adlist = list()
workinglist = list()
notworkinglist = list()
while True:

    tellme = input("1. load your file and website \n2. check your connectivity(and after this write to your file)\n3. the list of the website that has been loaded\n4. add more website to the list \n5. remove website from the list \n.6 track your website\n:    ")

    #Function for checking if you can connect to a website
    def check(adlist):
        for ip in adlist:
            ip.strip()
            response = os.popen(f"ping {ip} -n 1").read()
            if "Received = 1" and "Approximate" in response:
                print(f"UP {ip} Ping Successful")
                workinglist.append(ip)
            else:
                notworkinglist.append(ip)
                print(f"Down {ip} Ping Unsuccessful")

    #Function to check the website url
    def recon(file):
        for line in file:
             for m in re.findall('http[s]?://|www?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line):
                    adlist.append(m)
        print("Those are your website that you have written" + str(adlist))

    #Function to track website
    def track():
        Working = True
        trackip = input("write the website you want to track : ")
        tracknumber = input(
            "how much time you want to track the website in seconds (please write in multiple of ten) : ")
        response = os.popen(f"ping {trackip} -n 1").read()
        print(response)
        tracknumber = int(tracknumber)
        counter = 0
        while Working:
            if "Received = 1" and "Approximate" in response:
                print(f"UP {trackip} Ping Successful")
                duration = 1000  # milliseconds
                freq = 440  # Hz
                winsound.Beep(freq, duration)
                Working = False
            if counter == tracknumber:
                print("Im sorry but i guess its not gonna work . Going back to the menu\n")
                Working = False
                continue
            else:
                print(f"Down {trackip} Ping Unsuccessful")
                print("Still trying to connect....")
                time.sleep(10)
                counter += 10
                continue

    #Options of the menu
    if tellme == "stop":
        break
    elif tellme =="restart":
        continue
    elif tellme =="1":
            giveme = input("write your file path so i can test your website: ")
            file = open(giveme,"r")
            recon(file)
            print("Your file has been loaded")
            file.close()
    elif tellme =="2":
        check(adlist)
        iknow2 = input("do you want me to save connectivity result ?")
        if iknow2 == "yes":
            file = open("E://website.txt", "w")
            for each in workinglist:
                file.write("the website " + each + " is on at " + date + "\n")
            for noteach in notworkinglist:
                file.write("the website " + noteach + " is off at " + date + "\n")
            file.close()
            print("back to the menu ....")
            continue
        if iknow2 == "no":
            print("back to the menu ....")
            continue
    elif tellme == "3":
        print(adlist)
    elif tellme =="4":
        addon = input("write your website down :")
        raw = addon.split()
        adlist.extend(raw)
        continue
    elif tellme =="5":
        print(adlist)
        addon2 = input("write the website you want to remove:")
        adlist.remove(addon2)
        continue
    elif tellme =="6":
        track()
    #well that's all of my script it was enjoyable :D



