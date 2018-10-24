def songright(robot: cozmo.robot.Robot):
    # scales is a list of the words for Cozmo to sing
    # scales = ["Doe", "Ray", "Mi", "Fa", "So", "La", "Ti", "Doe"]
    scales = ["Doe", "Doe", "So", "So", "La", "La", "So", "Fa", "Fa", "Mi", "Mi", "Ray", "Ray", "Doe"]
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
        robot.say_text(note, voice_pitch=voice_pitch, duration_scalar=0.1).wait_for_completed()
        voice_pitch += voice_pitch_delta


def cozmo_singing(robot: cozmo.robot.Robot):
    # Create an array of SongNote objects, consisting of all notes from C2 to C3_Sharp
    notes = [
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.G2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.G2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.A2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.A2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.G2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.F2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.F2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.E2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.E2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.D2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.D2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C2, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.Rest, cozmo.song.NoteDurations.Quarter)]

    # Play the ascending notes
    robot.play_song(notes, loop_count=1)

    # Create an array of SongNote objects, consisting of the C3 pitch with varying durations
    notes = [
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.Half),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.ThreeQuarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.Rest, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.Quarter),
        cozmo.song.SongNote(cozmo.song.NoteTypes.C3, cozmo.song.NoteDurations.Whole)]

    # Play the notes with varying durations
    # robot.play_song(notes, loop_count=1).wait_for_completed()


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
