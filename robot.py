#!/usr/bin/env python3
from dataclasses import dataclass
from enum import IntEnum
import logging

import rev
import wpilib
import wpilib.drive

class Intake(IntEnum):
    OFF = 0
    EAT = 1
    SPIT = 2

@dataclass
class ProcessedInputs:
    """ dataclass to capture controller inputs """
    vel_pos: float = 0.0
    vel_angle: float = 0.0
    intake_state: int = Intake.OFF

class SimpleArcadeBot(wpilib.TimedRobot):
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        # Setting Params
        self.timer = wpilib.Timer()
        self.logger = logging.getLogger('SimpleArcadeBot')

        # NO MAGIC VALUES!
        joystick_usb_port = 0
        left_lead_motor_channel = 5
        left_follow_motor_channel = 1
        right_lead_motor_channel = 2
        right_follow_motor_channel = 3
        intake_motor_channel = 4
        
        is_left_lead_motor_reversed = False
        is_left_follow_motor_reversed = False
        is_right_lead_motor_reversed = True
        is_right_follow_motor_reversed = True
        is_intake_motor_reversed = False

        # Initializing Hardware
        self.left_lead_motor = rev.CANSparkMax( left_lead_motor_channel, rev.CANSparkMax.MotorType.kBrushless )
        self.left_follow_motor = rev.CANSparkMax( left_follow_motor_channel, rev.CANSparkMax.MotorType.kBrushless )
        self.right_lead_motor = rev.CANSparkMax( right_lead_motor_channel, rev.CANSparkMax.MotorType.kBrushless )
        self.right_follow_motor = rev.CANSparkMax( right_follow_motor_channel, rev.CANSparkMax.MotorType.kBrushless )
        self.intake_motor = rev.CANSparkMax( intake_motor_channel, rev.CANSparkMax.MotorType.kBrushless )
        self.joystick = wpilib.Joystick( joystick_usb_port )

        # Configuration
        self.left_lead_motor.setInverted( is_left_lead_motor_reversed )
        self.left_follow_motor.setInverted( is_left_follow_motor_reversed )
        self.right_lead_motor.setInverted( is_right_lead_motor_reversed )
        self.right_follow_motor.setInverted( is_right_follow_motor_reversed )
        self.left_follow_motor.follow( self.left_lead_motor )
        self.right_follow_motor.follow( self.right_lead_motor )
        self.intake_motor.setInverted( is_intake_motor_reversed )

        self.drivetrain = wpilib.drive.DifferentialDrive( self.left_lead_motor, self.right_lead_motor )


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
        # Joystick Config
        invert_roll = True
        invert_pitch = False
        spit_button = 2

        # Process
        data = ProcessedInputs()
        data.vel_pos = (-1)**invert_roll * self.joystick.getY()
        data.vel_angle = (-1)**invert_pitch * self.joystick.getX()

        if self.joystick.getTrigger():
            data.intake_state = Intake.EAT
        elif self.joystick.getRawButton(spit_button):
            data.intake_state = Intake.SPIT

        # Telemetry
        self.logger.info("=========================")
        self.logger.info("Player inputs:")
        self.logger.info(f"\tGoal Velocity: {data.vel_pos}")
        self.logger.info(f"\tGoal Angular Velocity: {data.vel_angle}")
        self.logger.info(f"\tIntake: {data.intake_state}")
        return data

    def actuate(self, goal):
        # angle needs to be negated
        # https://robotpy.readthedocs.io/projects/robotpy/en/stable/wpilib.drive/DifferentialDrive.html#wpilib.drive.DifferentialDrive
        self.drivetrain.arcadeDrive( goal.vel_pos, -goal.vel_angle )

        match goal.intake_state:
            case Intake.EAT:
                self.intake_motor.set(1.0)

            case Intake.SPIT:
                self.intake_motor.set(-1.0)

            case Intake.OFF:
                self.intake_motor.set(0)


    def teleopPeriodic(self):
        """This function is called periodically during teleoperated mode."""
        goals = self.process_player_input()
        self.actuate(goals)


    def testInit(self):
        """This function is called once each time the robot enters test mode."""
        pass

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        pass

if __name__ == "__main__":
    wpilib.run(SimpleArcadeBot)