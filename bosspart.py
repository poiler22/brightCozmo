import cozmo

def cozmo_neutral_reactions(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.PetDetectionDog).wait_for_completed()
    robot.say_text("Hello! How are you today?").wait_for_completed()
    
def cozmo_anger_reactions(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabScaredCozmo).wait_for_completed()
    robot.say_text("Why are you angry? Be happy!").wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabHappy).wait_for_completed()
    
def cozmo_unknown_reactions(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabExcited).wait_for_completed()
    robot.say_text("Hello! How are you today?").wait_for_completed()

#def cozmo_disgust_reactions(robot: cozmo.robot.Robot):
#    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabCurious).wait_for_completed()
#    robot.say_text("Hello! What am I do wrong?").wait_for_completed()
    
#def cozmo_fear_reactions(robot: cozmo.robot.Robot):
#    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabScaryCozmo).wait_for_completed()
#    robot.say_text("Hello! Don't be afraid!").wait_for_completed()
    

def cozmo_happy_reactions(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabHappy).wait_for_completed()
    robot.say_text("Hello! This is a good day isn't it? Let's have fun!").wait_for_completed()

def cozmo_surprise_reactions(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.PetDetectionShort_Cat).wait_for_completed()
    robot.say_text("Hello! Cozmo here!").wait_for_completed()

def cozmo_sad_reactions(robot: cozmo.robot.Robot):
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabReactHappy).wait_for_completed()
    robot.say_text("Are you okay? You can talk to me.").wait_for_completed()

#Hi =
#if Hi  == "neutral": cozmo.run_program(cozmo_neutral_reactions)
#elif Hi == "anger": cozmo.run_program(cozmo_anger_reactions)
#elif Hi == "unknown": cozmo.run_program(cozmo_unknown_reactions)
#
#elif Hi == "happy": cozmo.run_program(cozmo_happy_reactions)
#elif Hi == "surprise":cozmo.run_program(cozmo_surprise_reactions)
#elif Hi == "sad": cozmo.run_program(cozmo_sadness_reactions)


