#!/usr/bin/env python3
from dataclasses import dataclass
import logging

import wpilib
import wpilib.drive

@dataclass
class ProcessedInputs:
    """ dataclass to capture controller inputs """
    vel_pos: float = 0.0
    vel_angle: float = 0.0

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        # General Params
        self.timer = wpilib.Timer()
        self.logger = logging.getLogger(type(self).__name__)

        # Hardware Configuration
        joystick_usb_port = 0
        left_motor_channel = 0
        right_motor_channel = 1

        is_left_motor_inverted = False
        is_right_motor_inverted = False

        # Hardware Initialization
        self.joystick = wpilib.Joystick(joystick_usb_port)
        self.leftDrive = wpilib.PWMSparkMax( left_motor_channel )
        self.rightDrive = wpilib.PWMSparkMax( right_motor_channel )

        self.drivetrain = wpilib.drive.DifferentialDrive( self.leftDrive, self.rightDrive )
        self.leftDrive.setInverted(is_left_motor_inverted)
        self.rightDrive.setInverted(is_right_motor_inverted)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.restart()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass

    def teleopInit(self):
        """This function is called once each time the robot enters teleoperated mode."""
        pass

    def process_player_input(self):
        """ Gets inputs from joystick and converts to set of goals """
        # Config 
        invert_roll = False
        invert_pitch = False

        # Process
        data = ProcessedInputs()
        data.vel_pos = (-1)**invert_pitch * self.joystick.getX()
        data.vel_angle = (-1)**invert_roll * self.joystick.getY()

        return data

    def teleopPeriodic(self):
        """This function is called periodically during teleoperated mode."""
        goal = self.process_player_input()
        self.drivetrain.arcadeDrive( goal.vel_pos, goal.vel_angle )

    def testInit(self):
        """This function is called once each time the robot enters test mode."""
        pass

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        pass


if __name__ == "__main__":
    wpilib.run(MyRobot)
