from ctre import WPI_TalonSRX
from wpilib import Joystick, Spark, Talon # OH?
import magicbot
import wpilib
from components.DRIVER import Chassis
from components.mypid import DriveController
from networktables import NetworkTables
from navx import AHRS


class Joker(magicbot.MagicRobot):
    drivePID: DriveController
    chassis: Chassis

    def createObjects(self):
        """ Create motors, sensors and all your components here. """
        self.chassis_left_master = TalonSRX(1)
        self.chassis_left_slave = TalonSRX(5)
        self.chassis_right_master = TalonSRX(2)
        self.chassis_right_slave = TalonSRX(3)

        self.chassis_gyro = AHRS.create_spi()
        self.joystick = Joystick(0)

    def disabledInit(self):
        if self.drivePID.enabled:  # Was ist das? magik? Shirimasen
            self.drivePID.close()

    def robotPeriodic(self):
        if self.isAutonomousEnabled():
            #i need to add a function that is the Exact Opposite of set_teleop()
            pass
        elif self.isOperatorControlEnabled():
            self.chassis.set_teleop()

    def teleopInit(self):
        """ Called when teleop starts. """
        NetworkTables.initialize(server="10.43.20.149")
        #WTH do i suppose to call it?
        self.driverStation = NetworkTables.getTable("SmartDashboard")
        self.chassis.reset()
        #Umm... i dont really know what to do here... 

    def teleopPeriodic(self):
        """ Called on each iteration of the control loop. """
        self.chassis.set_speed(-self.joystick.getX(), -self.joystick.getZ())
        self.chassis.set_drive_mode()


if __name__ == '__main__':
    wpilib.run(Joker)
