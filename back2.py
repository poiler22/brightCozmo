elif ({"sing", "song", "cosmo"} <= set(ListOfCommand)) or ({"sing", "song", "cozmo"} <= set(ListOfCommand)):
cozmo_singing(robot)
ListOfCommand.clear()
elif {"face", "follower"} <= set(ListOfCommand):
follow_faces(robot)
ListOfCommand.clear()
elif {"square", "cosmo"} <= set(ListOfCommand) or {"square", "cozmo"} <= set(ListOfCommand):
cozmo_squares(robot)
ListOfCommand.clear()
elif {"dance", "cosmo"} <= set(ListOfCommand):
running(robot)
ListOfCommand.clear()
elif ({"angry", "cosmo"} <= set(ListOfCommand)) or ({"cosmo", "mad"} <= set(ListOfCommand)) or (
        {"cozmo", "mad"} <= set(ListOfCommand)) or ({"cozmo", "angry"} <= set(ListOfCommand)):
motion_step(robot)
ListOfCommand.clear()
elif ({"spin", "cozmo"} <= set(ListOfCommand)) or ({"cosmo", "spin"} <= set(ListOfCommand)):
cozmo_spin(robot)
ListOfCommand.clear()
elif ({"cozmo", "refuse"} <= set(ListOfCommand)) or ({"cosmo", "refuse"} <= set(ListOfCommand)):
cozmo_refuse(robot)
ListOfCommand.clear()
elif ({"cozmo", "nod"} <= set(ListOfCommand)) or ({"cosmo", "nod"} <= set(ListOfCommand)):
cozmo_nod(robot)
ListOfCommand.clear()