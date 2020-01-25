from magicbot import feedback
from wpilib.drive import DifferentialDrive
from ctre import WPI_TalonSRX, FeedbackDevice, ControlMode
from navx import AHRS


class Chassis:
    right_master: WPI_TalonSRX
    left_master: WPI_TalonSRX
    right_slave: WPI_TalonSRX
    left_slave: WPI_TalonSRX
    navx: AHRS
    isArcade: bool

    def setup(self):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        self.left_slave.follow(self.left_master)
        self.right_slave.follow(self.right_master)

        self.drive = DifferentialDrive(self.left_master, self.right_master)
        self.drive.setSafetyEnabled(True)
        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        isArcade= True # Added this
    def set_motors_values(self, left_power: float, right_power: float):
        self.left_master.set(left_power)
        self.right_master.set(right_power)

    def set_speed(self, y_speed, z_speed):
        self.y_speed = y_speed
        self.z_speed = z_speed
    #I Changed this name
    def set_drive_mode(self, y_speed, z_speed):
        self.drive.arcadeDrive(y_speed, z_speed)

    def disable(self):
        self.teleop = False
        self.auto = False

    def reset(self):
        print("wtf is a reset")
        self.set_speed(0,0)
        self.done()
        #Added these ^^

    def is_auto(self):
        #iChanged this V
        return self.auto
    #I Changed thisVV
    def change_drive_mode(self,isArcade):
        if isArcade:
            self.drive.arcadeDrive(self.y_speed, self.z_speed)
        #Im not sure if im supposed to add a tank drive option as well...
