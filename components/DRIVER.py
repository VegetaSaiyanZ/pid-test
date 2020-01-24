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

    def setup(self):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        self.left_slave.follow(self.left_master)
        self.right_slave.follow(self.right_master)

        self.drive = DifferentialDrive(self.left_master, self.right_master)
        self.drive.setSafetyEnabled(True)
        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")

    def set_motors_values(self, left_power: float, right_power: float):
        self.left_master.set(left_power)
        self.right_master.set(right_power)

    def set_speed(self, y_speed, z_speed):
        self.y_speed = y_speed
        self.z_speed = z_speed

    def wtf(self, y_speed, z_speed):
        self.drive.arcadeDrive(y_speed, z_speed)

    def disable(self):
        self.teleop = False
        self.auto = False

    def reset(self):
        print("wtf is a reset")

    def is_auto(self):
        return True

    def gogopowerrangers(self):
        if True:
            self.drive.arcadeDrive(self.y_speed, self.z_speed)
