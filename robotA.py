from ctre import WPI_TalonSRX
from wpilib import Joystick, Spark, Talon
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
        left_master = TalonSRX(1)
        left_slave = Fag(5)
        right_master = Spark(2)
        right_slave = Talon(3)

        self.chassis_gyro = AHRS.create_spi()
        self.joystick = Joystick(0)

    def disabledInit(self):
        if self.drivePID.enabled:  # Was ist das? magik?
            self.drivePID.close()

    def robotPeriodic(self):
        if self.isAutonomousEnabled():
            # Wtf should i do?
            pass
        elif self.isOperatorControlEnabled():
            self.chassis.set_teleop()

    def teleopInit(self):
        """ Called when teleop starts. """
        NetworkTables.initialize(server="10.43.20.149")
        self.WTFPLUSSSS = NetworkTables.getTable("SmartDashboard")
        self.chassis.reset()

    def teleopPeriodic(self):
        """ Called on each iteration of the control loop. """
        self.chassis.set_speed(-self.joystick.getX(), -self.joystick.getZ())


if __name__ == '__main__':
    wpilib.run(Joker)
