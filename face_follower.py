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
import voiceParse
import cozmo
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
    print("Press CTRL-C to quit")
    global sentimental
    while True:
        turn_action = None
        if face_to_follow:
            # start turning towards the face
            turn_action = robot.turn_towards_face(face_to_follow,in_parallel=True)

        if not (face_to_follow and face_to_follow.is_visible):
            # find a visible face, timeout if nothing found after a short while
            try:
                face_to_follow = robot.world.wait_for_observed_face()#timeout=30)
                if face_to_follow.expression == "unknown":
                    sentimental = "unknown"
                if face_to_follow.expression == "happy":
                    sentimental = "happy"
                    checkfeelinghappy = checkfeelinghappy + 1
                if face_to_follow.expression == "sad":
                    sentimental = "sad"
                    checkfeelingsad = checkfeelingsad + 1
                if face_to_follow.expression == "surprised":
                    sentimental = "surprised"
                if face_to_follow.expression == "angry":
                    sentimental = "angry"
                    checkfeelingangry = checkfeelingangry + 1
                if face_to_follow.expression == "neutral":
                    sentimental = "neutral"
            except asyncio.TimeoutError:
                print("Didn't find a face - exiting!")
                return

        if turn_action:
            # Complete the turn action if one was in progress
            turn_action.wait_for_completed()
        time.sleep(.5)

# cozmo.run_program(follow_faces, use_viewer=True, force_viewer_on_top=True)