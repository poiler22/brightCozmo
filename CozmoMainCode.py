import cleverwrap
import cozmo
import time
import sys
import ast
#import asyncio
#from cozmo.util import degrees, distance_mm, speed_mmps
import voiceParse
#from gtts import gTTS
#import speech_recognition as sr
import os.path
import re
import webbrowser
import smtplib
import requests
import random
import functionsCozmo
import face_follower
from weather import Weather
import asyncio


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

import threading
def mainLoop(robot: cozmo.robot.Robot):
    threadFace = threading.Thread(target=face_follower.follow_faces, args=(robot,))
    threadFace.start()


    while True:
        print('Expression:' + face_follower.notifyExpression())

        # In a loop, we grab the user input
        print("Listening...")
        humanString = (voiceParse.parseVoice()).lower()
        ListOfCommand = [str(s) for s in (humanString.lower()).split()]


        # Check it for a quit condition.
        if {'shut','down'} <= set(ListOfCommand) or {'cosmo','shut','down'} <= set(ListOfCommand):
            # If we quit, we log the quit and leave the program.
            addEntry(log, "Conversation ended.")
            ListOfCommand.clear()
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
            robot.say_text("Done",in_parallel=True).wait_for_completed()
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
            robot.say_text("Done",in_parallel=True).wait_for_completed()
            continue

        if 'open my favorite song' in humanString:
            robot.say_text("What song?",in_parallel=True).wait_for_completed()
            humanString1 = (voiceParse.parseVoice()).lower()
            print("Human says: " + humanString1)
            reg_ex = re.search('(.+)', humanString1)

            if reg_ex:
                SongName = reg_ex.group(1)
                #you can add any song you want in the ListofSongs, by adding key word with its watch?v=?????????
                json_file = open('texttest.json')
                json_str = json_file.read()
                dictOfSong = ast.literal_eval(json_str)
                """ListofSongs = {"part of your world": "watch?v=gtpLsPPtC88", "full nocturne": 'watch?v=liTSRH4fix4',
                               'eyes on fire': 'watch?v=LAxCqlU-OAo', 'nocturne in f minor': 'watch?v=E3qHO9aOQYM',
                               'moonlight sonata': 'watch?v=4Tr0otuiQuU', 'clair de lune': 'watch?v=ea2WoUtbzuw',
                               'hello': 'watch?v=YQHsXMglC9A', 'skyfall': 'watch?v=DeumyOzKqgI'}"""

                subUrl = 'https://www.youtube.com/search?q=' + SongName
                has_Song=False
                for x in range(len(dictOfSong['song'])):
                    if (dictOfSong['song'][x]['name']).lower() == SongName:
                        webbrowser.open(dictOfSong['song'][x]['url'])
                        has_Song=True
                        break
                if has_Song == False:
                    webbrowser.open(subUrl)
                    continue
                continue
            elif type(SongName) == type(None):
                robot.say_text("No command found",in_parallel=True).wait_for_completed()
                continue
            robot.say_text("Done",in_parallel=True).wait_for_completed()
            addEntry(log, "Cozmo says: " + "Done")
            print("Cozmo says: " + "Done")
            continue



        if 'open website' in humanString:
            robot.say_text("What do you want me to open",in_parallel=True).wait_for_completed()
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
                robot.say_text("What are you looking for in " + domain,in_parallel=True).wait_for_completed()
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
            robot.say_text("Done",in_parallel=True).wait_for_completed()
            addEntry(log, "Cozmo says: " + "Done")
            print("Cozmo says: " + "Done")
            continue


        if  ({"cosmo", "email"} <= set(ListOfCommand)) or ({"cozmo", "email"} <= set(ListOfCommand)):
            ListOfCommand.clear()
            robot.say_text("Who is the recipient?",in_parallel=True).wait_for_completed()
            addEntry(log, "Cozmo says: " + "Who is the recipient?")
            print("Cozmo says: " + "Who is the recipient?")
            recipient = (voiceParse.parseVoice()).lower()
            addEntry(log, "Human says: " + recipient)
            print("Human says: " + recipient)
            #you can add any email in the line below
            """ListofEmails = {"bright":"bright_ra2@hotmail.com","boss":"biggerbosssuper@gmail.com",
                            "tim":"tim.dettmar@gmail.com","lucky":"vorachat1239@gmail.com"}"""

            json_file1 = open('texttest.json')
            json_str1 = json_file1.read()
            dictOfEmail = ast.literal_eval(json_str1)

            has_Email = False
            for x in range(len(dictOfEmail['email'])):
                if (dictOfEmail['email'][x]['name']).lower == recipient:
                    robot.say_text("What should I say?", in_parallel=True).wait_for_completed()
                    addEntry(log, "Cozmo says: " + "What should I say?")
                    print("Cozmo says: " + "What should I say?")
                    content = (voiceParse.parseVoice()).lower()
                    addEntry(log, "Human says: " + content)
                    print("Human says: " + content)

                    # init gmail SMTP
                    ListOfSmtp = {'gmail':[{'name':'smtp.gmail.com','key': '587'}],
                    'outlook':[{'name':'smtp-mail.outlook.com','key':'587' }],
                    'hotmail': [{'name': 'smtp.live.com', 'key': '25'}]}
                    checkSmtp = dictOfEmail['email'][x]['url'].split(".")
                    b = checkSmtp.split("@")
                    c = b[1].split(".")
                    d = c[0]
                    #check email whether our email is outlook or gmail
                    if d in ListOfSmtp:
                        mail = smtplib.SMTP(ListOfSmtp[d][0]['name'], ListOfSmtp[d][0]['key'])
                        # smtp-mail.outlook.com

                        # identify to server
                        mail.ehlo()

                        # encrypt session
                        mail.starttls()

                        # In this line, we open text file from gui
                        json_file = open('useradding.json')
                        json_str = json_file.read()
                        dictOfUser = ast.literal_eval(json_str)

                        # In this line, put your email and password
                        mail.login(dictOfUser['email'][0]['name'], dictOfUser['email'][0]['password'])

                        # send to the recipient
                        mail.sendmail('recipient', dictOfEmail['email'][x]['url'], content + "\n" + "sent via Cozmo")

                        # end mail connection
                        mail.close()

                        robot.say_text("Sent", in_parallel=True).wait_for_completed()
                        addEntry(log, "Cozmo says: " + "Sent")
                        print("Cozmo says: " + "Sent")
                        has_Email = True
                        break

                    else:
                        robot.say_text("I can\'t send because I don't know the SMTP name", in_parallel=True).wait_for_completed()
                        addEntry(log, "Cozmo says: " + "I can\'t send because I don't know the SMTP name")
                        print("Cozmo says: " + "I can\'t send because I don't know the SMTP name")
                        return mainLoop()

            if has_Email == False:
                robot.say_text("I don\'t know him", in_parallel=True).wait_for_completed()
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
                robot.say_text(TempetureForecast, use_cozmo_voice=False,duration_scalar=0.7, in_parallel=True).wait_for_completed()
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
                robot.say_text(str(res.json()['joke']),in_parallel=True).wait_for_completed()
                print("Cozmo says: " + str(res.json()['joke']))
                addEntry(log, "Cozmo says: " + str(res.json()['joke']))

            else:
                robot.say_text(str(res.json()['oops!I ran out of jokes']),in_parallel=True).wait_for_completed()
                print("Cozmo says: " + 'oops!I ran out of jokes')
                addEntry(log, "Cozmo says: " + 'oops!I ran out of jokes')
            continue

        #Action Commands

        if ({"sing", "song", "cosmo","stupid"} <= set(ListOfCommand)) or ({"sing", "song", "cozmo","stupid"} <= set(ListOfCommand)):
            addEntry(log, "Human says: " + humanString)
            print("Human says: " + humanString)
            ListOfCommand.clear()
            functionsCozmo.cozmo_singing(robot)
            robot.say_text("Do you like my song?",play_excited_animation=True,in_parallel=True).wait_for_completed()
            print("Cozmo says: " + "Do you like my song?")
            addEntry(log, "Cozmo says: " + "Do you like my song?")
            continue

        if ({"random", "cosmo",'emotion'} <= set(ListOfCommand)) or ({"random", "cozmo",'emotion'} <= set(ListOfCommand)):
            ListOfCommand.clear()
            functionsCozmo.motion_step(robot)
            continue


        # Else, we log what the human said.
        addEntry(log, "Human says: " + humanString)
        print("Human says: " + humanString)

        # Grab the response from CleverBot
        cozmoString = cleverbot.say(humanString)

        # Print the response to the screen and add it to the log
        print("Cozmo says: " + cozmoString)
        addEntry(log, "Cozmo says: " + cozmoString)

        # Then we make Cozmo say it.
        robot.say_text(cozmoString,in_parallel=True).wait_for_completed()
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

def run():
    cozmo.run_program(mainLoop, use_viewer=False, force_viewer_on_top=False)