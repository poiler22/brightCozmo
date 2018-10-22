import cleverwrap
import cozmo
import time
import sys
import asyncio
from cozmo.util import degrees, distance_mm, speed_mmps
import voiceParse
from gtts import gTTS
import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests
import random
import functionsCozmo
from weather import Weather


APIKEY = "CC8o4IwXba1_aD74BgI46ZHxFBQ"

# Charger
cozmo.robot.Robot.drive_off_charger_on_connect = False

# Strings
cozmoString = ""
humanString = ""


# Function to get the log started
def initLog():
    log = 0
    # Let's try to open the log file to append to. If we fail, we are forced to
    # exit the program. Otherwise, we state that the log file is opened.
    try:
        log = open("log.txt", "a")
    except:
        print("Error opening log file!")
        sys.exit()
    else:
        print("Log file opened.")

    return log


# Function to add entry to the log file.
def addEntry(log, entry):
    entryTime = time.gmtime()

    # Time format: Day-Month-Year Hour:Minute:Second
    parsedTime = str(entryTime.tm_mday) + "-" + str(entryTime.tm_mon) + "-" + \
                 str(entryTime.tm_year) + " " + str(entryTime.tm_hour) + ":" + \
                 str(entryTime.tm_min) + ":" + str(entryTime.tm_sec)

    # Now we patch together the log message
    logMessage = parsedTime + "# " + entry

    # Let's try to log it. If it fails, we simply skip logging the message
    try:
        log.write(logMessage + "\n")
    except:
        print("Error logging message! Skipping...")


# A simple error checking wrapper for the cleverwrap script
def initBot(apiKey):
    bot = 0
    # Let's try to open it, if it fails, we log and exit.
    try:
        bot = cleverwrap.CleverWrap(apiKey)
    except:
        print("Error connecting to CleverBot!")
        sys.exit()
    else:
        print("Connected to CleverBot!")

    return bot

def mainLoop(robot: cozmo.robot.Robot):
    while True:
        # In a loop, we grab the user input
        print("Listening...")
        humanString = (voiceParse.parseVoice()).lower()
        ListOfCommand = [str(s) for s in (humanString.lower()).split()]


        # Check it for a quit condition.
        if humanString.lower() == "quit":
            # If we quit, we log the quit and leave the program.
            addEntry(log, "Conversation ended.")
            sys.exit()


        if 'open reddit' in humanString:
            reg_ex = re.search('open reddit(.*)', humanString.lower())
            url = 'https://www.reddit.com/'
            addEntry(log, "Human says: " + humanString)
            print("Human says: " + humanString)
            if reg_ex:
                subreddit = reg_ex.group(1)
                url = url + 'r/' + subreddit
            webbrowser.open(url)
            addEntry(log, "Cozmo says: " + humanString)
            print("Cozmo says: " + "Done")
            robot.say_text("Done").wait_for_completed()
            continue


        if 'open google' in humanString:
            reg_ex = re.search('open google(.*)', humanString.lower())
            url = 'https://www.google.com/'
            if reg_ex:
                subreddit = reg_ex.group(1)
                url = url + 'search?q=' + subreddit
            webbrowser.open(url)
            addEntry(log, "Human says: " + humanString)
            print("Human says: " + humanString)
            addEntry(log, "Cozmo says: " + humanString)
            print("Cozmo says: " + "Done")
            robot.say_text("Done").wait_for_completed()
            continue

        if 'open my favorite song' in humanString:
            robot.say_text("What song?").wait_for_completed()
            humanString1 = (voiceParse.parseVoice()).lower()
            print("Human says: " + humanString1)
            reg_ex = re.search('(.+)', humanString1)

            if reg_ex:
                SongName = reg_ex.group(1)
                ListofSongs = {"part of your world": "watch?v=gtpLsPPtC88", "full nocturne": 'watch?v=liTSRH4fix4',
                               'eyes on fire': 'watch?v=LAxCqlU-OAo', 'nocturne in f minor': 'watch?v=E3qHO9aOQYM',
                               'moonlight sonata': 'watch?v=4Tr0otuiQuU', 'clair de lune': 'watch?v=ea2WoUtbzuw',
                               'hello': 'watch?v=YQHsXMglC9A', 'skyfall': 'watch?v=DeumyOzKqgI'}

                subUrl = 'https://www.youtube.com/search?q=' + SongName
                if SongName not in ListofSongs:
                    webbrowser.open(subUrl)
                else:
                    url = 'https://www.youtube.com/' + str(ListofSongs.get(SongName))
                    webbrowser.open(url)
            elif type(SongName) == type(None):
                robot.say_text("No command found").wait_for_completed()
                continue
            robot.say_text("Done").wait_for_completed()
            addEntry(log, "Cozmo says: " + "Done")
            print("Cozmo says: " + "Done")
            continue



        if 'open website' in humanString:
            robot.say_text("What do you want me to open").wait_for_completed()
            humanString1 = (voiceParse.parseVoice()).lower()
            print("Human says: " + humanString1)
            reg_ex = re.search('(.+)', humanString1)
            if reg_ex:
                domain = reg_ex.group(1)
                url = 'https://www.' + domain + ".com"
                ListofDictionaries = {"google":"search?q=","youtube":'search?q=',"reddit":"r/",
                                      'amazon':'s?url=search-alias%3Daps&field-keywords='}
                if domain not in str(ListofDictionaries):
                    webbrowser.open(url)
                    continue
                robot.say_text("What are you looking for in " + domain).wait_for_completed()
                addEntry(log, "Cozmo says: " + "What are you looking for in " + domain)
                print("Cozmo says: " + "What are you looking for in " + domain)
                humanString2 = (voiceParse.parseVoice()).lower()
                addEntry(log, "Human says: " + humanString2)
                print("Human says: " + humanString2)
                if "nothing" in humanString2:
                    webbrowser.open(url)
                else:
                    newurl = url + "/" + ListofDictionaries.get(domain) + humanString2
                    webbrowser.open(newurl)
            else:
                pass
            robot.say_text("Done").wait_for_completed()
            addEntry(log, "Cozmo says: " + "Done")
            print("Cozmo says: " + "Done")
            continue


        if  ({"cosmo", "email"} <= set(ListOfCommand)) or ({"cozmo", "email"} <= set(ListOfCommand)):
            ListOfCommand.clear()
            robot.say_text("Who is the recipient?").wait_for_completed()
            addEntry(log, "Cozmo says: " + "Who is the recipient?")
            print("Cozmo says: " + "Who is the recipient?")
            recipient = (voiceParse.parseVoice()).lower()
            addEntry(log, "Human says: " + recipient)
            print("Human says: " + recipient)
            #you can add any email in the line below
            ListofEmails = {"bright":"bright_ra2@hotmail.com","boss":"biggerbosssuper@gmail.com",
                            "tim":"tim.dettmar@gmail.com","lucky":"vorachat1239@gmail.com"}
            if recipient in ListofEmails:
                robot.say_text("What should I say?").wait_for_completed()
                addEntry(log, "Cozmo says: " + "What should I say?")
                print("Cozmo says: " + "What should I say?")
                content = (voiceParse.parseVoice()).lower()
                addEntry(log, "Human says: " + content)
                print("Human says: " + content)

                # init gmail SMTP
                mail = smtplib.SMTP('smtp.gmail.com', 587)

                # identify to server
                mail.ehlo()

                # encrypt session
                mail.starttls()

                # In this line, put your email and password
                mail.login('bright.ra5@gmail.com', 'BrighT01p')

                # send to the recipient
                mail.sendmail('recipient', ListofEmails.get(recipient), content +"\n" + "sent via Cozmo")

                # end mail connection
                mail.close()

                robot.say_text("Sent").wait_for_completed()
                addEntry(log, "Cozmo says: " + "Sent")
                print("Cozmo says: " + "Sent")

            else:
                robot.say_text("I don\'t know him").wait_for_completed()
                addEntry(log, "Cozmo says: " + "I don\'t know him")
                print("Cozmo says: " + "I don\'t know him")
            continue


        if 'weather forecast in' in humanString:
            addEntry(log, "Human says: " + humanString)
            print("Human says: " + humanString)
            reg_ex = re.search('weather forecast in (.*)', humanString)
            if reg_ex:
                city = reg_ex.group(1)
                weather = Weather()
                location = weather.lookup_by_location(city)
                forecasts = location.forecast
                for i in range(0, 3):
                    TempetureForecast = ('On %s will it %s. The maximum temperture will be %.1f degrees Celcius.'
                             'The lowest temperature will be %.1f degrees Celcius.' % (
                             forecasts[i].date, forecasts[i].text, int(forecasts[i].high),
                             int(forecasts[i].low)))
                robot.say_text(TempetureForecast).wait_for_completed()
                addEntry(log, "Cozmo says: " + TempetureForecast)
                print("Cozmo says: " + TempetureForecast)
                continue


        if ({"cosmo", "joke"} <= set(ListOfCommand)) or ({"cozmo", "joke"} <= set(ListOfCommand)):
            ListOfCommand.clear()
            res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept": "application/json"}
            )
            if res.status_code == requests.codes.ok:
                robot.say_text(str(res.json()['joke'])).wait_for_completed()
                print("Cozmo says: " + str(res.json()['joke']))
                addEntry(log, "Cozmo says: " + str(res.json()['joke']))

            else:
                robot.say_text(str(res.json()['oops!I ran out of jokes'])).wait_for_completed()
                print("Cozmo says: " + 'oops!I ran out of jokes')
                addEntry(log, "Cozmo says: " + 'oops!I ran out of jokes')
            continue

        #Action Commands

        if ({"sing", "song", "cosmo","stupid"} <= set(ListOfCommand)) or ({"sing", "song", "cozmo","stupid"} <= set(ListOfCommand)):
            addEntry(log, "Human says: " + humanString)
            print("Human says: " + humanString)
            ListOfCommand.clear()
            functionsCozmo.cozmo_singing(robot)
            robot.say_text("Do you like my song?").wait_for_completed()
            print("Cozmo says: " + "Do you like my song?")
            addEntry(log, "Cozmo says: " + "Do you like my song?")
            continue

        if ({"angry", "cosmo"} <= set(ListOfCommand)) or ({"cosmo", "mad"} <= set(ListOfCommand)) or (
                {"cozmo", "mad"} <= set(ListOfCommand)) or ({"cozmo", "angry"} <= set(ListOfCommand)):
            ListOfCommand.clear()
            functionsCozmo.motion_step(robot)



        # Else, we log what the human said.
        addEntry(log, "Human says: " + humanString)
        print("Human says: " + humanString)

        # Grab the response from CleverBot
        cozmoString = cleverbot.say(humanString)

        # Print the response to the screen and add it to the log
        print("Cozmo says: " + cozmoString)
        addEntry(log, "Cozmo says: " + cozmoString)

        # Then we make Cozmo say it.
        robot.say_text(cozmoString).wait_for_completed()
        ListOfCommand.clear()


# This is where our code begins. We can first initialize everything,
# Then once it's all started, we log that the conversation has started
# and print the quit instructions to the user.
voiceParse.initSpeech()
log = initLog()
cleverbot = initBot(APIKEY)
addEntry(log, "Conversation started.")
print("######################")
print("#Type 'quit' to exit.#")
print("######################")

cozmo.run_program(mainLoop)
