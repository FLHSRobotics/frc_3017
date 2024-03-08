#!/usr/bin/env python3
from dataclasses import dataclass
import logging
import math

import rev
import wpilib
import wpilib.drive
import ctre



@dataclass
class SwerveModule:
    def __init__(self, drive_motor_id, steer_motor_id, encoder_id, offset):
        self.drive_motor = ctre.WPI_TalonFX(drive_motor_id)
        self.steer_motor = ctre.WPI_TalonFX(steer_motor_id)
        self.encoder = ctre.CANCoder(encoder_id)
        self.offset = offset
        self.encoder.configMagnetOffset(self.offset)

    def set_speed_and_angle(self, speed, angle):
        current_angle = self.encoder.getAbsolutePosition()
        target_angle = math.degrees(angle) % 360
        angle_difference = target_angle - current_angle
        angle_difference = (angle_difference + 180) % 360 - 180
        if abs(angle_difference) > 90:
            angle_difference = (angle_difference + 180) % 360 - 180
            speed = -speed
        self.steer_motor.set(ctre.ControlMode.Position, math.radians(current_angle + angle_difference))
        self.drive_motor.set(ctre.ControlMode.PercentOutput, speed)




class SwerveDriveBot(wpilib.TimedRobot):
    def robotInit(self):
        # Setting Params
        self.timer = wpilib.Timer()
        self.logger = logging.getLogger('SwerveDriveBot')

        # NO MAGIC VALUES!
        self.joystick = wpilib.Joystick(0)
        self.swerve_modules = [
            SwerveModule(1, 2, 1, 0),
            SwerveModule(3, 4, 2, 0),
            SwerveModule(5, 6, 3, 0),
            SwerveModule(7, 8, 4, 0),
        ]

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.restart()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass

    def teleopInit(self):
        """This function is called once each time the robot enters teleoperated mode."""
        pass

    def teleopPeriodic(self):
        """This function is called periodically during teleoperated mode."""
        # Process
        Drive = -self.joystick.getY()
        Strafe = self.joystick.getX()
        Rotate = self.joystick.getZ()

        for module in self.swerve_modules:
            module.set_speed_and_angle(math.hypot(Drive, Strafe), math.atan2(Drive, Strafe))

        # Telemetry
        self.logger.info("=========================")
        self.logger.info("Player inputs:")
        self.logger.info(f"\tGoal Velocity (Y): {Drive}")
        self.logger.info(f"\tGoal Velocity (X): {Strafe}")
        self.logger.info(f"\tGoal Angular Velocity: {Rotate}")
        return Drive, Strafe, Rotate

    def testInit(self):
        """This function is called once each time the robot enters test mode."""
        pass

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        pass


if __name__ == "__main__":
    wpilib.run(SwerveDriveBot)