#!/usr/bin/env python3

# Copyright (c) 2016 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Make Cozmo turn toward a face.
This script shows off the turn_towards_face action. It will wait for a face
and then constantly turn towards it to keep it in frame.
'''

import asyncio
import time
import functionsCozmo
import cozmo
import random
import requests
# import faces

sentimental = ''
def notifyExpression():
    return sentimental

def follow_faces(robot: cozmo.robot.Robot):
    '''The core of the follow_faces program'''

    # Move lift down and tilt the head up
    robot.move_lift(-3)
    robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
    robot.enable_facial_expression_estimation()
    face_to_follow = None

    checkfeelingsad = 0
    checkfeelingangry = 0
    checkfeelinghappy = 0
    checkfeelingunknown = 0
    checkfeelingneutral = 0
    checkfeelingsurprised = 0
    print("Press CTRL-C to quit")
    global sentimental
    while True:
        turn_action = None
        if face_to_follow:
            # start turning towards the face
            turn_action = robot.turn_towards_face(face_to_follow,in_parallel=True)

        
            # find a visible face, timeout if nothing found after a short while
        try:
            face_to_follow = robot.world.wait_for_observed_face()#timeout=30)
            print(face_to_follow)
            if face_to_follow.expression == "unknown":
                sentimental = "unknown"
                checkfeelingunknown = checkfeelingunknown + 1
            if face_to_follow.expression == "happy":
                sentimental = "happy"
                checkfeelinghappy = checkfeelinghappy + 1
            if face_to_follow.expression == "sad":
                sentimental = "sad"
                checkfeelingsad = checkfeelingsad + 1
            if face_to_follow.expression == "surprised":
                sentimental = "surprised"
                checkfeelingsurprised = checkfeelingsurprised + 1
            if face_to_follow.expression == "angry":
                sentimental = "angry"
                checkfeelingangry = checkfeelingangry + 1
            if face_to_follow.expression == "neutral":
                sentimental = "neutral"
                checkfeelingneutral = checkfeelingneutral + 1
        except asyncio.TimeoutError:
            print("Didn't find a face - exiting!")
            return
        if checkfeelingsad >= 3:
            print('Are you sad?')
            checkfeelingsad = 0
            res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept": "application/json"}
            )
            if res.status_code == requests.codes.ok:
                a = random.randint(1,2)
                if a == 1:
                    robot.say_text("you know " + str(res.json()['joke']),in_parallel=True,duration_scalar=1.2).wait_for_completed()
                else:
                    robot.say_text("Do you want some Burger?", in_parallel=True, duration_scalar=1.2).wait_for_completed()
                print("Cozmo says: " + str(res.json()['joke']))


            else:
                robot.say_text(str(res.json()['oops!I ran out of jokes']),in_parallel=True).wait_for_completed()

                print("Cozmo says: " + 'oops!I ran out of jokes')

            continue

        elif checkfeelingangry >= 3:
            print('Are you ok?')
            checkfeelingangry = 0
            robot.say_text("Are you ok? Want some lasanga?", in_parallel=True).wait_for_completed()
            
        elif checkfeelinghappy >= 3:
            print('You look happy which is good')
            checkfeelinghappy = 0
            robot.say_text("You look happy which is good", in_parallel=True).wait_for_completed()
        
        elif checkfeelingneutral >= 3:
            print('How was your day?')
            functionsCozmo.motion_step(robot)
            functionsCozmo.motion_step(robot)
            checkfeelinghappy = 0
            robot.say_text("How was your day?", in_parallel=True).wait_for_completed()
        if turn_action:
            # Complete the turn action if one was in progress
            turn_action.wait_for_completed()
        time.sleep(5)
