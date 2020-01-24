from magicbot import AutonomousStateMachine, state
from components.mypid import DriveController


class Drive:
    drivePID: DriveController

    def auto_drive(self):
        if self.drivePID.finished:
            self.done()
