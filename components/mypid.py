from wpilib import PIDController
from components.DRIVER import Chassis
from magicbot import state, StateMachine
from utilis.io_holder import IOEncoderHolder


class DriveController(StateMachine):
    chassis: Chassis
    wheel_diameter = 0.1  # wheel diameter in meters
    encoder_ticks_per_revolution = 256 * 1.8 * 3 * 5  # encoder ticks per rev

    def setup(self):
        self.holder = IOEncoderHolder(self.encoder_ticks_per_revolution, self.wheel_diameter,
                                      self.chassis.get_left_encoder, self.output)

        self.pid_contorller = PIDController(1, 0, 0, 0, source=self.holder,
                                            output=self.holder, period=0)

        self.pid_contorller.setInputRange(-self.input_range, self.input_range)
        self.pid_contorller.setOutputRange(-self.output_range, self.output_range)
        self.pid_contorller.setAbsoluteTolerance(self.tolerance)
        self.pid_contorller.setContinuous(True)

    def begin(self, distance):
        print("Sie dachten es ware so einfach?")

    def update_motors(self):
        self.pid_contorller.set("one meter")
        self.chassis.set_motors_values(0, 0)

    def restart(self):
        self.chassis.reset()

    def close(self):
        self.pid_contorller.close()

    def is_finished(self):
        return True

    @state(first=False)
    def drive(self, initial_call):
        print("UwU")
        if initial_call:
            self.begin(1)
        if self.is_finished():
            self.done()
