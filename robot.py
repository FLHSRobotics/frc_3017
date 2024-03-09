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
        self.steer_motor.configSelectedFeedbackSensor(ctre.FeedbackDevice.IntegratedSensor)

    def set_speed_and_angle(self, speed, angle):

        # Convert angle from radians to degrees and adjust for offset
        desired_angle = math.degrees(angle) - self.offset

        # Ensure the angle is within [0, 360) range
        desired_angle = desired_angle % 360
        current_angle = self.encoder.getAbsolutePosition() - self.offset
        current_angle = current_angle % 360

        # Determine the shortest path to the desired angle
        angle_difference = desired_angle - current_angle
        if angle_difference > 180:
            angle_difference -= 360
        elif angle_difference < -180:
            angle_difference += 360

        # Reverse the wheel if necessary to minimize rotation
        if angle_difference > 90 or angle_difference < -90:
            if angle_difference > 90:
                angle_difference -= 180
            else:
                angle_difference += 180
            speed = -speed

        # Convert angle difference to encoder units, considering the encoder resolution
        encoder_ticks_per_rotation = 4096 # Encoder Resolution
        target_position = (angle_difference / 360.0) * encoder_ticks_per_rotation

        # Set steering motor to the calculated target position
        self.steer_motor.set(ctre.ControlMode.Position, target_position)

        # Set drive motor speed
        self.drive_motor.set(ctre.ControlMode.PercentOutput, speed)




class SwerveDriveBot(wpilib.TimedRobot):
    def robotInit(self):
        self.timer = wpilib.Timer()
        self.logger = logging.getLogger('SwerveDriveBot')

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

        drive = -self.joystick.getY()
        strafe = self.joystick.getX()
        rotate = self.joystick.getZ()

        wheel_angles = [math.pi / 4, 3 * math.pi / 4, 5 * math.pi / 4, 7 * math.pi / 4]

        for i, module in enumerate(self.swerve_modules):
            rotation_x = rotate * math.cos(wheel_angles[i])
            rotation_y = rotate * math.sin(wheel_angles[i])

            wheel_x = strafe + rotation_x
            wheel_y = drive + rotation_y

            speed = math.hypot(wheel_x, wheel_y)
            angle = math.atan2(wheel_y, wheel_x)

            module.set_speed_and_angle(speed, angle)


        # Telemetry
        self.logger.info("=========================")
        self.logger.info("Player inputs:")
        self.logger.info(f"\tGoal Velocity (Y): {drive}")
        self.logger.info(f"\tGoal Velocity (X): {strafe}")
        self.logger.info(f"\tGoal Angular Velocity: {rotate}")
        return drive, strafe, rotate

    def testInit(self):
        """This function is called once each time the robot enters test mode."""
        pass

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        pass


if __name__ == "__main__":
    wpilib.run(SwerveDriveBot)