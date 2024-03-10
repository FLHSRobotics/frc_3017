# FRC Team 3017

## Intro

The goal of this document is to provide a Python-centric guided tour of the FRC documentation. You will be expected to thoroughly read through the referenced documents. You will not be expected to have any FRC programming knowledge but some understanding of basic Python syntax is expected. Hopefully, by the end of reading through all of this, you will have a fully programmed robot and the confidence to tackle more complex problems.

The official FRC Documentation can be found [here](https://docs.wpilib.org/en/stable/index.html)

### Table of Contents

This guide will flow as follows:
  1. [System Overview](#system-overview): We first describe the physical system we are working with.
  - [At a Glance](#at-a-glance): Diagram of system
  - [The Components](#the-components): Description of the components
    - [120A Circuit Breaker](#120a-circuit-breaker)
    - [Motor Controllers](#motor-controllers)
    - [OpenMesh Radio](#openmesh-radio)
    - [Power Distribution Panel](#power-distribution-panel)
    - [RoboRIO](#roborio)
    - [Robot Signal Light](#robot-signal-light)
    - [Voltage Regulator Module](#voltage-regulator-module)
  - [Connecting the Components](#connecting-the-components): How the components interact
    - [Power](#power)
    - [Data](#data)
      - [CAN vs PWM](#can-vs-pwm)
  2. [System Setup](#system-setup): Software we need to set up before coding
  - [Update the RoboRIO](#update-the-roborio)
  - [Radio Configuration](#radio-configuration)
    - [Event vs Non-Event Mode](#event-vs-non-event-mode)
  - [Python Setup](#python-setup)
    - [IDE](#ide)
    - [Robotpy](#robotpy)
  3. [Programming in Python](#programming-in-python)
  - [From a High Level](#from-a-high-level)
    - [Note on Objects and Classes](#note-on-objects-and-classes)
  - [MyRobot Class](#myrobot-class)
  - [Robot Init](#robot-init)
    1. [General Setup](#general-setup)
    2. [Hardware Configuration](#hardware-configuration)
    3. [Hardware Initialization](#hardware-initialization)
      - [PWM](#pwm)
      - [CAN](#can)

## System Overview

We want to give a high-level overview of:
  1. [What are the components and what do they do?](#the-components)
  2. [How do they connect to each other?](#connecting-the-components)

The doc to reference for this section is the [Introduction to FRC Robot Wiring](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-1/intro-to-frc-robot-wiring.html). Make sure to select CTR for all the images as that is the electronics system we use. The default selected company is REV.

### At a Glance

<p align="center" width="100%">
  <img src="https://docs.wpilib.org/en/stable/_images/frc-control-system-layout.svg" width="90%">
</p>

### The Components

Here we describe the function of most of the components we use in our team. In alphabetical order:

  - [120A Circuit Breaker](#120a-circuit-breaker)
  - [Motor Controllers](#motor-controllers)
  - [OpenMesh Radio](#openmesh-radio)
  - [Power Distribution Panel](#power-distribution-panel)
  - [RoboRIO](#roborio)
  - [Robot Signal Light](#robot-signal-light)
  - [Voltage Regulator Module](#voltage-regulator-module)

#### 120A Circuit Breaker:

The 120 Amp circuit breaker is basically the on/off switch for the robot.

Push the little latch that says RESET to turn the robot ON. Pressing the red button turns it OFF and pushes the latch out.

<p align="center" width="100%">
  <img src="https://cdn.andymark.com/product_images/120-amp-breaker/am_0282/5bd3e2f661a10d27d2433225/detail.jpg" width="30%">
</p>

More technically, a circuit breaker is a safety device in a circuit that automatically stops the flow of current if there is too much of it. Current is measured in Amps so our robot will automatically turn off at 120 Amps. The battery we use is 12 Volts, so another way of thinking about it is our robot will turn off if the amount of power it uses exceeds 120A x 12V = 1440 Watts.

#### Motor Controllers

Motor controllers do what their name implies: they send a control signal to whatever motor they are attached to. The main motor controllers we might use are from the Spark (REV Robotics) or Talon (CTR Electronics) series.

##### Configuration Tools

  - [REV Hardware Client](https://docs.revrobotics.com/rev-hardware-client/)
  - [CTRE Phoenix 6](https://v6.docs.ctr-electronics.com/en/stable/)

<p align="center" width="100%">
  <img src="https://cdn11.bigcommerce.com/s-t3eo8vwp22/images/stencil/1280x1280/products/360/2795/MAX_HERO-noflag__60247.1692730069.png" width="30%">
  <img src="https://cdn11.bigcommerce.com/s-7cuph2j78p/images/stencil/1280x1280/products/224/677/image_1__31850.1697125467.png" width="30%">
</p>

Motor controllers determine how much voltage to send to a motor. The greater the voltage, the faster it spins. If the voltage becomes negative, the motor will spin in the opposite direction. Thus, a motor controller outputs a voltage signal between -100% and 100%.

Motor controllers send signals to the motor and report information back from the motor, such as encoder readings. The manufacturer's configuration tools allow you to configure the controller to do more advanced things.

#### OpenMesh Radio

The Open-Mesh radio is a Wi-Fi router connected to the robot. We use it to connect to the robot and run or deploy code.

<p align="center" width="100%">
  <img src="https://cdn.andymark.com/product_images/open-mesh-om5p-ac-dual-band-1-17-gbps-access-point-radio/am-3205/5c33d218fe93c61bdeff9b12/detail.jpg" width="25%">
</p>

#### Power Distribution Panel

The Power Distribution Panel (PDP) takes the 12V input from the battery and safely redistributes it across all of the devices.

<p align="center" width="100%">
  <img src="https://www.vexrobotics.com/media/catalog/product/cache/d64bdfbef0647162ce6500508a887a85/2/1/217-4244.jpg" width="40%">
</p>

The slots in the middle are for circuit breakers for each individual channel, allowing you to add an extra layer of safety for each device connected to the system. The PDP can also monitor the battery's status and the current going to each channel.

#### RoboRIO

The RoboRIO is the robot's onboard computer. This is where our code will be deployed and run.

<p align="center" width="100%">
  <img src="https://cdn.andymark.com/product_images/ni-roborio/5cd03254fe93c67e8e620dea/detail.jpg" width="40%">
  <img src="https://cdn.andymark.com/product_images/ni-roborio-2/6165f0a8fdc8c543df4a4a5e/detail.jpg" width="40%">
</p>

Note there are two versions of the RoboRIO. The newer version says "RoboRIO 2.0" while the RoboRIO 1.0 just says "NI RoboRIO".

#### Robot Signal Light

The robot signal light is a light that lets us quickly discern whether the robot is on or off.

<p align="center" width="100%">
  <img src="https://cdn.andymark.com/product_images/robot-signal-light/5bd8b84d61a10d5948a53665/detail.jpg" width="20%">
</p>

#### Voltage Regulator Module

The voltage regulator module provides stable and clean power to the Open-Mesh Radio.

<p align="center" width="100%">
  <img src="https://cdn.andymark.com/product_images/voltage-regulator-module/5bd3428561a10d292c9646c5/detail.jpg" width="30%">
</p>

In general, voltage regulator modules are devices that convert a higher voltage input to a lower voltage output to power a device that uses a lower voltage. They can also make voltage inputs more stable for more sensitive devices.

### Connecting the Components

The focus of this section won't be about how to actually physically join these components together; the official documents are adequate. What we want to do is provide a quick conceptual recap of how our system works.

There are two ways in which devices are connected: power and data.

#### Power

Everything needs to be powered, so we'll trace the journey starting from the battery.

  - The first thing the battery connects to is the 120A circuit breaker. As our ON/OFF switch, it has direct access to cutting power from the battery.
  - The 120A circuit breaker then connects to the Power Distribution Panel.
  - The PDP supplies power to the RoboRIO, each motor, motor controller, and to the Voltage Regulator Module.
  - The RoboRIO provides power to the Robot Signal Light.
  - The VRM provides power to the Open-Mesh Radio.

#### Data

Among our components, the only things that need to share data with each other are:

  - The RoboRIO and the Open-Mesh Radio connect to each other via an Ethernet cable.

  - The RoboRIO and each motor controller talk to each other via CAN or PWM.


##### CAN vs PWM

CAN and PWM are just interfaces computer chips use to talk to each other, similar to USB.

CAN allows you to daisy-chain all your devices together and talk on a network. The main concern is you'd have to use the manufacturer's [configuration tool](#configuration-tools) to set the ID of each motor controller.

PWM connects directly to PWM ports on the RoboRIO. You are limited to the number of ports you see, and the ID number of the port is not changeable.

## System Setup

Now that we have everything plugged in and turned on, we need to set up the software. Please read the [Software Component Overview](https://docs.wpilib.org/en/stable/docs/controls-overviews/control-system-software.html).

We have the next goals in mind:

  1. [Update the software on the RoboRIO](#update-the-roborio)
  2. [Configure the Open-Mesh Radio](#radio-configuration)
  3. [Setup Python on your local computer to work with FRC](#python-setup)

### Update the RoboRIO

Every year, the RoboRIO's system software must be updated, or it will not work for that year's game. To do so, we follow the guides:

  1. [Installing the FRC Game Tools](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/frc-game-tools.html)\
  We first need to install the RoboRIO Imaging Tool. An image is a "snapshot" of all the software on a certain device. The way RoboRIO is updated is by wiping everything and installing the latest image from the manufacturer. Thus it is called the "Imaging Tool".

  2. [Imaging Your RoboRIO 1](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/imaging-your-roborio.html)\
  Now follow the instructions for using the RoboRIO imaging tool. Plug the RoboRIO in via USB cable, select it as the target, and select "Format Target". "Format" is a fancy word for "wipe", which is what we want to do here.

### Radio Configuration

Each year the Open-Mesh Radio also needs to be re-configured.

Note that there are two different radio configurations: one for use at events and another for private use. Thus, we have multiple radios. The ones labeled "COMP" are not to be configured and are to be brought along to competitions.

[Configure radios for use outside of FRC events](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/radio-programming.html)

#### Event vs Non-Event Mode

The RoboRIO is directly connected to the radio via an Ethernet cable. When configured for non-events, the radio broadcasts its own wifi network (named 3017) that we can connect to with our laptop to deploy or run code.

At events, the radio is configured to broadcast a shared network with all the other bots so there isn't interference. This does mean there is a bandwidth restriction of 4Mb/s.

### Python Setup

To get started in Python, we basically need two things:

  1. [IDE](#ide)
  2. [Robotpy](#robotpy)

#### IDE

If you already have a favorite editor, feel free to skip this section and use what you're familiar with.

If you don't know what that is, just get [VSCode](https://code.visualstudio.com/download).

A tutorial can be found [here](https://code.visualstudio.com/docs/python/python-tutorial)

An Integrated Development Environment (IDE) is a suite of tools for developing programs. At a minimum, it consists of a file browser, text editor, and build tooling.

Create a new folder somewhere and name it something reasonable, like `FRC`. Open this folder in your IDE.

#### Robotpy

Robotpy is the tool we use to connect Python with our FRC electronics. Mainly, we will be using robotpy to push code from our laptop to the robot.

But first, we need to:
  1. Use `pip` to install robotpy
  2. Use `robotpy` to generate template files for our FRC robot.

If you know what you are doing, just follow this [guide](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/python-setup.html):


To do this in VSCode:

  1. Create New Terminal (Ctrl+Shift+\`) and from within:
  - MacOS: `python3 -m pip install robotpy`
  - Windows: `py -3 -m pip install robotpy`
  2. From the same terminal, run:
  - MacOS: `python3 -m robotpy init`
  - Windows: `py -3 -m robotpy init`

Inside the folder you created for this project you should see two new files: `pyproject.toml` and `robot.py`

## Running the Robot

### Deploying Code

_Deployment_ is the process of putting software on the system it will actually be used.

The way we deploy our code is to connect to the radio, which should have been configured to be broadcasting a wifi signal with name 3017. Make sure our wifi settings are set to this network.

From the terminal, navigate to the folder where `pyproject.toml` and `robot.py` are. From there, we will run `deploy`. In VSCode, you can do the same as the previous section and:
  - Create New Terminal (Ctrl+Shift+\`) and from within:
    - MacOS: `python3 -m robotpy deploy`
    - Windows: `py -3 -m robotpy deploy`

The first time you run this it will ask you if you would like to generate test files. Hit yes as we would like it to try to catch our silly mistakes.

### FRC Driver Station

  - [Detailed Overview](https://docs.wpilib.org/en/stable/docs/software/driverstation/driver-station.html)

With our wifi still on 3017, launch the driver station and select the tab that looks like a steering wheel. From there, select a mode, such as "TeleOperated", and hit "Enable" to start the robot.

## Programming in Python

### Quick Start

An example basic drivetrain for Python, along with an explanation of the code, can be found [here](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-4/creating-test-drivetrain-program-cpp-java-python.html).Make sure to select Python as the programming language.

The main thing to understand is not to change any of the function names, and they will always behave the way it is described in that tutorial. Specifically:
  - `robotInit()` is called once when the robot turns on
  - `autonomousInit()` is called once when we start autonomous mode
  - `autonomousPeriodic()` is called repeatedly during autonomous mode
  - Same for `teleopInit()`, `teleopPeriodic()`, `testInit()`, `testPeriodic()` but for their respective modes.

This repository also contains a slightly more involved example. Feel free to copy and modify the `pyproject.toml` and `robot.py` provided.

The example working code for 2023's bot can also be found in the branches section of GitHub.

### Documentation References

  - [WPILib](https://robotpy.readthedocs.io/projects/robotpy/en/stable/): Your bible for programming anything in Python is going to be this. Every single thing you can do will be explained here.
  - [REV](https://robotpy.readthedocs.io/projects/rev/en/stable/api.html): For programming motor controllers that are Spark or SparkMAX.
  - [CTRE](https://api.ctr-electronics.com/phoenix6/release/python/): For CTR Electronics such as Talon FX.

#### How to Use the Docs

The docs tell you about what objects are available to you and what actions each object can take. Let's demonstrate by using the docs to understand more deeply what is going on in the tutorial.

##### Ex 1
For example, on line 33 in `autonomousInit()`, there is a `self.timer.restart()`. Unfortunately, the tutorial only explains, "We restart the Timer in this method," which isn't very helpful.

So, first, we check what type of object `self.timer` is. Scrolling up to line 24 in `robotInit()`, we see that it is `wpilib.Timer()`. Thus, we go to the wpilib documentation.

We first notice there is no wpilib.Timer package, which means Timer() probably exists in the main wpilib package itself. Checking inside the [wpilib package](https://robotpy.readthedocs.io/projects/robotpy/en/stable/wpilib.html), we indeed do see a Timer() object. Clicking into that, we can finally scroll down to [`reset()`](https://robotpy.readthedocs.io/projects/robotpy/en/stable/wpilib.html) to see what it is doing.

##### Ex 2
As a more complicated example, on line 41, we have `self.robotDrive.arcadeDrive(0.5, 0, squareInputs=False)` explained simply as "drives forward at half speed". We can see this is a `wpilib.drive.DifferentialDrive()` object and can be found in package `wpilib.drive`.

In the differential drive [page](https://robotpy.readthedocs.io/projects/robotpy/en/stable/wpilib.drive/DifferentialDrive.html#wpilib.drive.DifferentialDrive), we get a full description of how it works, what coordinate frame it expects, and can see even cooler stuff available to us such as `curvatureDrive()`.

### How to Program

#### From a High Level

If you're staring at the code in `robot.py` and wondering where to start, this is where you should start reading.

Let's look at the skeleton of the example code:

```
import wpilib

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):

    def autonomousInit(self):

    def autonomousPeriodic(self):

    def teleopInit(self):

    def teleopPeriodic(self):

    def testInit(self):

    def testPeriodic(self):

if __name__ == "__main__":
    wpilib.run(MyRobot)
```

From top to bottom, this does 3 things.

  1. We import wpilib. [Wpilib](https://docs.wpilib.org/en/stable/docs/software/what-is-wpilib.html) is a set of software tools, called a _library_, that provide a framework for our Python code to work within the FRC ecosystem.
  2. Create a class called `MyRobot`. A class is a definition of an _object_, explained [below](#side-note-on-classes).
  3. Check that we are the main Python program (as opposed to being a library that is imported). If so, give the definition of `MyRobot` to wpilib's `run()` function.

The bulk of our coding will be done inside the class definition.

##### Note on Objects and Classes

In programming languages, variables are our nouns and functions are our verbs. Usually certain actions are only associated with certain things. So we group them together into something called an _object_: a container of variables and functions. The way we define objects is to classify them, that's why we create a _class_.

For example, think of an apple. If you hold up an apple and show it to me, that is an object. But the concept of an apple is really just a classification of objects. Not all objects are apples, only those that fit a certain description. It has properties (taste, smell, size, color, etc) and it has ways you can interact with it (bite, chop, skin, etc).

Classes can also _inherit_ properties and interactions from other classes, meaning it can have access to all the variables and functions of its _parent/super class_ and extend upon it. For example, "fruit" is another class, and "apple" would be a _child/sub class_ and inherit properties like having a harvest time or actions like "eat".

The way that classes work is we are given a special keyword called `self`, which will refer to the object that is created using the class. Inside our class we can define functions such as `def my_func(self)`. Notice that `self` is the first input argument passed to the function. We can access the _members_ of our class (our variables and functions) via a dot `.`, so we can also define variables using `self.x = 123`. It is best practice to define all your variables in the init function.

#### MyRobot Class

The `MyRobot` class is a class we create the inherits from wpilib's `TimedRobot` class. This is meant to work with the FRC driver station. Its [docs](https://robotpy.readthedocs.io/projects/robotpy/en/stable/wpilib/TimedRobot.html) state that it is meant to just be inherited from.

As soon as you turn on the robot (close the 120A circuit breaker), the RoboRIO powers on and calls `robotInit()`. Then, from the FRC driver station you may select between autonomous, teleop, and test modes. When you select these modes, the corresponding functions will be called.

For example, let's say we select teleop. Once we hit "Enable":

  1. The code inside `telopInit()` is executed once.
  2. The code inside `teleopPeriodic()` will be executed in a loop while we haven't hit the "Disable" button.

Generally we want to avoid having while and/or for loops inside ther periodic functions unless we really want our robot to stop everything and wait for whatever is inside the loop to finish first.

#### Robot Init

```
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
```

We need to initialize all the shared variables in our class that we want to use across the functions. Most importantly, we need to assign variable names to the various hardware components of our robot.

---

##### General Setup
```
        self.timer = wpilib.Timer()
        self.logger = logging.getLogger(type(self).__name__)
```

The first thing we do is initialize some generally helpful stuff.

Wpilib's `Timer()` class provides a timer for us to use to check how long it has been since we've enabled whatever mode we're in. We create a `Timer()` object and set it to the class variable `self.timer`.

We also set up a logger. This requires us to have `import logging` at the top of the file. Logging is useful because it helps us print telemetry using set templates, such as recording the time or the value of certain variables. We can also define different types of templates for use in different situations such as "info", "warn", "error", etc...

We create a logger object and assign it to the variable `self.logger`. We can print things using this logger by calling `self.logger.info("my message")`.

  - [Timer Docs](https://robotpy.readthedocs.io/projects/robotpy/en/stable/wpilib/Timer.html#)
  - [Logging Docs](https://docs.python.org/3/library/logging.html)

---
##### Hardware Configuration
```
        joystick_usb_port = 0
        left_motor_channel = 0
        right_motor_channel = 1

        is_left_motor_inverted = False
        is_right_motor_inverted = False
```

There are two main things we have to configure for our hardware.

  1. Identify physical devices and map the ports/channels/etc to variables.
  2. Define hardware settings that we want to persist through all modes. We do this at the top in one place so it's easier for us to organize and debug.

###### How to Identify Devices

  - USB: Check the list of USB devices before and after plugging in your controller.
    - Windows: Go to *Device Manager* -> *Universal Serial Bus Controllers*. This lists all USB ports connected to the system.
    - Mac: Open terminal and type `ls /dev/tty*`.
  - Motor Controllers:
    - PWM: Look along the right side of the RoboRIO for the PWM ports and trace what number each motor controller is connected to.
    - CAN: Use manufacturer software to set the CAN ID for each motor controller.
      - [REV Hardware Client](https://docs.revrobotics.com/rev-hardware-client/)
      - [CTRE Phoenix 6](https://v6.docs.ctr-electronics.com/en/stable/)

---
##### Hardware Initialization

```
        self.joystick = wpilib.Joystick(joystick_usb_port)
        self.leftDrive = wpilib.PWMSparkMax( left_motor_channel )
        self.rightDrive = wpilib.PWMSparkMax( right_motor_channel )

        self.drivetrain = wpilib.drive.DifferentialDrive( self.leftDrive, self.rightDrive )
        self.leftDrive.setInverted(is_left_motor_inverted)
        self.rightDrive.setInverted(is_right_motor_inverted)
```

We now need to:
  1. Create our hardware connections.
  2. Apply our configuration from the previous step.

##### PWM

If using PWM as the interface for communicating with motor controllers, we can use the PWM motor controller classes in wpilib. Check [the docs](https://robotpy.readthedocs.io/projects/robotpy/en/stable/wpilib.html) and search for classes that begin with PWM followed by the name of your motor. For example, if using the Spark MAX motor controller from REV Robotics, we use the `PWMSparkMax()` class.

##### CAN

If using CAN as the interface, you will need to use the class under the manufacturer's library. `rev` package of robotpy.

First, go to `pyproject.toml` and uncomment the line with `rev`. Then add `import rev` to the top of your file.
