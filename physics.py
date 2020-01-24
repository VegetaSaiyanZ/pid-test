#
# See the notes for the other physics sample
#
import os

import math
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units
from pyfrc import sim
import pathfinder


class PhysicsEngine(object):
    """
    Simulates a 4-wheel robot using Tank Drive joystick control
    """
    reset = False

    def __init__(self, physics_controller):
        self.physics_controller = physics_controller
        self.physics_controller.add_device_gyro_channel("navxmxp_spi_4_angle")

        # Change these parameters to fit your robot!
        bumper_width = 0 * units.inch
        # fmt: off
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,  # motor configuration
            110 * units.lbs,  # robot mass
            6.601,  # drivetrain gear ratio
            2,  # motors per side
            26.7716535 * units.inch,  # robot wheelbase
            (26.7716535 + 1) * units.inch + bumper_width * 2,
            # robot width
            32 * units.inch + bumper_width * 2,  # robot length
            4 * units.inch,  # wheel diameter
        )

    def update_sim(self, hal_data, now, tm_diff):
        """
            Called when the simulation parameters for the program need to be
            updated.
            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        """

        """For drivetrain simulation"""
        # Not needed because front and rear should be in sync
        lm_motor = hal_data['CAN'][1]['value']
        rm_motor = hal_data['CAN'][3]['value']

        x, y, angle = self.drivetrain.get_distance(lm_motor, rm_motor, tm_diff)
        self.physics_controller.distance_drive(x, y, angle)

        constants = {
            "wheel_diam": 4,
            "encoder_ratio": 3,
            "high_gear_ratio": 6.601,
            "low_gear_ratio": 14.999,
            "third_stage_ratio": 1.8,
            "encoder_ticks": 256,
            "wheelbase": 26.7716535,
            "kv": 0.00001079102
        }

        encoder_ratio = constants["encoder_ratio"]
        third_stage_ratio = constants["third_stage_ratio"]
        encoder_ticks = constants["encoder_ticks"]
        wheel_diam = constants["wheel_diam"]

        wheel_circumference = wheel_diam * math.pi/12

        ticks_per_rev = third_stage_ratio * encoder_ratio * encoder_ticks*5
        ticks_per_feet = ticks_per_rev / wheel_circumference

        hal_data['CAN'][1]['quad_position'] = int(self.drivetrain.l_position * ticks_per_feet)
        hal_data['CAN'][3]['quad_position'] = int(self.drivetrain.r_position * ticks_per_feet)
        hal_data.setdefault('custom', {})['left encoder'] = hal_data['CAN'][1]['quad_position']
        hal_data.setdefault('custom', {})['right encoder'] = hal_data['CAN'][3]['quad_position']


        def reset():
            self.drivetrain.l_position = 0
            self.drivetrain.r_position = 0
            hal_data['CAN'][1]['quad_position'] = 0
            hal_data['CAN'][3]['quad_position'] = 0
            hal_data['robot']['navxmxp_spi_4_angle'] = 0
            PhysicsEngine.reset = False

        if PhysicsEngine.reset:
            print("reset")
            reset()
        # TODO convert velocity measurement units
        hal_data['CAN'][2]['quad_velocity'] = self.drivetrain.l_velocity
        hal_data['CAN'][4]['quad_velocity'] = self.drivetrain.r_velocity

