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


def songright(robot: cozmo.robot.Robot):
    # scales is a list of the words for Cozmo to sing
    scales = ["Doe", "Ray", "Mi", "Fa", "So", "La", "Ti", "Doe"]

    # Find voice_pitch_delta value that will range the pitch from -1 to 1 over all of the scales
    voice_pitch = -1.0
    voice_pitch_delta = 20.0 / (len(scales) - 1)

    # Move head and lift down to the bottom, and wait until that's achieved
    robot.move_head(-5)  # start moving head down so it mostly happens in parallel with lift
    robot.set_lift_height(0.0).wait_for_completed()
    robot.set_head_angle(degrees(-25.0)).wait_for_completed()

    # Start slowly raising lift and head
    robot.move_lift(0.15)
    robot.move_head(0.15)

    # "Sing" each note of the scale at increasingly high pitch
    for note in scales:
        robot.say_text(note, voice_pitch=voice_pitch, duration_scalar=0.3).wait_for_completed()
        voice_pitch += voice_pitch_delta


def cozmo_singing(robot: cozmo.robot.Robot):
    # Create an array of SongNote objects, consisting of all notes from C2 to C3_Sharp
    notes = [
        cozmo.song.SongNote(cozmo.song.NoteTypes.E2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2_Sharp, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.D2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.D2_Sharp, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.E2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.F2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.F2_Sharp, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.G2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.G2_Sharp, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.A2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.A2_Sharp, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.B2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3_Sharp, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.Rest, cozmo.song.NoteDurations.Quarter)]

    # Play the ascending notes
    robot.play_song(notes, loop_count=1).wait_for_completed()

    # Create an array of SongNote objects, consisting of the C3 pitch with varying durations
    notes = [
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.Half),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.ThreeQuarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.Rest, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.Whole)]

    # Play the notes with varying durations
    robot.play_song(notes, loop_count=1).wait_for_completed()


# The main loop to our program. Runs after all the initialization.
def follow_faces(robot: cozmo.robot.Robot):
    '''The core of the follow_faces program'''

    # Move lift down and tilt the head up
    robot.move_lift(-3)
    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
    # look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    face_to_follow = None
    print("Press CTRL-C to quit")
    while True:
        turn_action = None
        if face_to_follow:
            # start turning towards the face
            turn_action = robot.turn_towards_face(face_to_follow)
        if not (face_to_follow and face_to_follow.is_visible):
            # find a visible face, timeout if nothing found after a short while
            try:
                face_to_follow = robot.world.wait_for_observed_face(timeout=5)
            except asyncio.TimeoutError:
                print("Didn't find a face - exiting!")
                return

        if turn_action:
            # Complete the turn action if one was in progress
            turn_action.wait_for_completed()

        time.sleep(.1)


def cozmo_squares(robot: cozmo.robot.Robot):
    # Use a "for loop" to repeat the indented code 4 times
    # Note: the _ variable name can be used when you don't need the value
    for _ in range(4):
        robot.drive_straight(distance_mm(150), speed_mmps(50)).wait_for_completed()
        robot.turn_in_place(degrees(90)).wait_for_completed()


def running(robot: cozmo.robot.Robot):
    # Drive forwards for 150 millimeters at 50 millimeters-per-second.
    robot.drive_straight(distance_mm(150), speed_mmps(50)).wait_for_completed()

    # Turn 90 degrees to the left.
    # Note: To turn to the right, just use a negative number.
    robot.turn_in_place(degrees(90)).wait_for_completed()


def motion_step(robot: cozmo.robot.Robot):
    # grab a list of animation triggers
    all_animation_triggers = robot.anim_triggers

    # randomly shuffle the animations
    random.shuffle(all_animation_triggers)

    # select the first three animations from the shuffled list
    triggers = 3
    chosen_triggers = all_animation_triggers[:triggers]
    print('Playing {} random animations:'.format(triggers))

    # play the three random animations one after the other, waiting for each to complete
    for trigger in chosen_triggers:
        print('Playing {}'.format(trigger.name))
        robot.play_anim_trigger(trigger).wait_for_completed()

    # grab animation triggers that have 'WinGame' in their name
    chosen_triggers = [trigger for trigger in robot.anim_triggers if 'WinGame' in trigger.name]

    # play the three random animations one after the other, waiting for each to complete
    for trigger in chosen_triggers:
        print('Playing {}'.format(trigger.name))
        robot.play_anim_trigger(trigger).wait_for_completed()


def cozmo_nod(robot: cozmo.robot.Robot):
    robot.move_head(-5).wait_for_completed
    robot.move_head(10).wait_for_completed
    robot.move_head(-5).wait_for_completed


def cozmo_refuse(robot: cozmo.robot.Robot):
    robot.turn_in_place(degrees(45)).wait_for_completed
    robot.turn_in_place(degrees(-90)).wait_for_completed
    robot.turn_in_place(degrees(45)).wait_for_completed


def cozmo_spin(robot: cozmo.robot.Robot):
    robot.turn_in_place(degrees(360)).wait_for_completed


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
                            "tim":"tim.dettmar@gmail.com"}
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
