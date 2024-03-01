# FRC Team 3017

## Intro

The goal of this document is to provide a Python-centric guided tour of the FRC documentation. You will be expected to thoroughly read through the referenced docs. You will not be expected to have any programming knowledge. Hopefully by the end of reading through all of this you will have a fully programmed robot along with the confidence of tackle more complex problems.

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
  3. [Programming in Python](#programming-in-pythong)

## System Overview

We want to give a high level overview of:
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

More technically, a circuit breaker is a safety device in a circuit that automatically stops the flow of current if there is too much of it. Current is measured in Amps and so our robot will automatically turn off at 120 Amps. The battery we use is 12 Volts, so another way of thinking about it is our robot will turn off if the amount of power it uses exceeds 120A x 12V = 1440 Watts.

#### Motor Controllers

Motor controllers do as the name implies: control signal to whatever motor it is attached to. The main motor controllers we might use are from the Spark (from REV Robotics) or Talon (CTR Electronics) series.

##### Configuration Tools

  - [REV Hardware Client](https://docs.revrobotics.com/rev-hardware-client/)
  - [CTRE Phoenix 6](https://v6.docs.ctr-electronics.com/en/stable/)

<p align="center" width="100%">
  <img src="https://cdn11.bigcommerce.com/s-t3eo8vwp22/images/stencil/1280x1280/products/360/2795/MAX_HERO-noflag__60247.1692730069.png" width="30%">
  <img src="https://cdn11.bigcommerce.com/s-7cuph2j78p/images/stencil/1280x1280/products/224/677/image_1__31850.1697125467.png" width="30%">
</p>

Motor controllers determine how much voltage to send to a motor. The greater the voltage, the faster it spins. If the voltage becomes negative, the motor will spin in the opposite direction. Thus a motor controller outputs a voltage signal between -100% to 100%.

Aside from sending signals to the motor, motor controllers also report information back from the motor, such as encoder readings. You can configure it to do more advanced stuff through the manufacturer's configuration tools.

#### OpenMesh Radio

The Open-Mesh radio is a wifi router that is connected to the robot. We use it to connect to the robot and run or deploy code.

<p align="center" width="100%">
  <img src="https://cdn.andymark.com/product_images/open-mesh-om5p-ac-dual-band-1-17-gbps-access-point-radio/am-3205/5c33d218fe93c61bdeff9b12/detail.jpg" width="25%">
</p>

#### Power Distribution Panel

The Power Distribution Panel (PDP) takes the 12V input from the battery and safely redistributes it across all of the devices.

<p align="center" width="100%">
  <img src="https://www.vexrobotics.com/media/catalog/product/cache/d64bdfbef0647162ce6500508a887a85/2/1/217-4244.jpg" width="40%">
</p>

The slots in the middle are for circuit breakers for each individual channel, allowing you to add an extra layer of safety for each device connected to the system. The PDP also can monitor the status of the battery and current going to each channel.

#### RoboRIO

The RoboRIO is the onboard computer of the robot. This is where our code will be deployed onto and be running on.

<p align="center" width="100%">
  <img src="https://cdn.andymark.com/product_images/ni-roborio/5cd03254fe93c67e8e620dea/detail.jpg" width="40%">
  <img src="https://cdn.andymark.com/product_images/ni-roborio-2/6165f0a8fdc8c543df4a4a5e/detail.jpg" width="40%">
</p>

Note there are two versions of the RoboRIO. The newer version says "RoboRIO 2.0" while the RoboRIO 1.0 just says "NI RoboRIO".

#### Robot Signal Light

The robot signal light is light that let's us quickly discern whether the robot is on or off.

<p align="center" width="100%">
  <img src="https://cdn.andymark.com/product_images/robot-signal-light/5bd8b84d61a10d5948a53665/detail.jpg" width="20%">
</p>

#### Voltage Regulator Module

The voltage regulator module provides stable and clean power to the Open-Mesh Radio.

<p align="center" width="100%">
  <img src="https://cdn.andymark.com/product_images/voltage-regulator-module/5bd3428561a10d292c9646c5/detail.jpg" width="30%">
</p>

In general, voltage regulator modules are devices that convert a higher voltage input to a lower voltage output to power a device that uses lower voltage. It also can make voltage inputs more stable for more sensitive devices.

### Connecting the Components

The focus of this section won't be about how to actually physically join these components together, the official docs are adequate. What we want to do is provide a quick conceptual recap of how our system works.

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

CAN and PWM are both just interfaces computer chips use to talk to each other, kind of like USB.

CAN allows you to daisy-chain all of your devices together and talk on a network. The main concern is you'd have to use the manufacturer's [configuration tool](#configuration-tools) to set the ID of each motor controller.

PWM connects directly to PWM ports on the RoboRIO. You are limited to the number of ports you see and the ID number of the port is not changeable.

## System Setup

Now that we have everything plugged in and turned on, we have the next goals in mind:

  1. [Update the software on the RoboRIO](#update-the-roborio)
  2. [Configure the Open-Mesh Radio](#radio-configuration)
  3. [Setup Python on your local computer to work with FRC](#python-setup)

### Update the RoboRIO

Every year the RoboRIO's system software must be updated or it will not work for that year's game. To do so, we follow the guides:

  1. [Installing the FRC Game Tools](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/frc-game-tools.html)\
  We first need to install the RoboRIO Imaging Tool. An image is a "snapshot" of all the software on a certain device. The way RoboRIO is updated is to wipe everything and install the latest image from the manufacturer. Thus it is called the "Imaging Tool".

  2. [Imaging Your RoboRIO 1](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/imaging-your-roborio.html)\
  Now follow instructions for using the RoboRIO imaging tool. Plug the RoboRIO in via USB cable, select it as the target, and select "Format Target". "Format" is a fancy word for "wipe", which is what we want to do here.

### Radio Configuration

Each year the Open-Mesh Radio also needs to be re-configured.

Note that there are two different configurations of the radio: one for use at events and another for private use. Thus we have multiple radios. Ones labeled "COMP" are not to be configured and are to be brough along to competitions.

[Configure radios for use outside of FRC events](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-3/radio-programming.html)

#### Event vs Non-Event Mode

The RoboRIO is directly connected to the radio via Ethernet cable. When configured for outside of events, the radio broadcasts its own wifi network (named 3017) that we can connect to with our laptop to deploy or run code.

At events, the radio is configured to broadcast a shared network with all the other bots so there isn't interference. This does mean there is a bandwidth restriction of 4Mb/s.

### Python Setup

To get started in Python, we basically need two things:

  1. [IDE](#ide)
  2. [Robotpy](#robotpy)

#### IDE

If you already have a favorite editor, feel free to skip this section and use what you're familiar with.

If you don't know what that is, just get [VSCode](https://code.visualstudio.com/download).

A tutorial can be found [here](https://code.visualstudio.com/docs/python/python-tutorial)

An Integrated Development Environment (IDE) is a suite of tools used for developing programs. At a minimum, they are a combination of file browser, text editor, and build tooling.

Create a new folder somewhere and name it something reasonable, like `FRC`. Open this folder in your IDE.

#### Robotpy

Robotpy is the library we need to connect Python with our FRC electronics.

We need to:
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

## Programming in Python

An example basic drivetrain for Python, along with explanation for the code, can be found [here](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-4/creating-test-drivetrain-program-cpp-java-python.html).

The main things to understand is to not change any of the function names and they will always behave the way it is described in that tutorial. Specifically:
  - `robotInit()` is called once when the robot turns on
  - `autonomousInit()` is called once when we start autonomous mode
  - `autonomousPeriodic()` is called repeatedly during autonomous mode
  - Same for `teleopInit()`, `teleopPeriodic()`, `testInit()`, `testPeriodic()` but for their respective modes.

This repository also contains a slightly more involved example. Feel free to copy and modify the `pyproject.toml` and `robot.py` provided.

The example working code for 2023's bot can also be found in the branches section of github.

### Documentation References

  - [WPILib](https://robotpy.readthedocs.io/projects/robotpy/en/stable/): Your bible for programming anything in Python is going to be this. Every single thing you can do will be explained here.
  - [REV](https://robotpy.readthedocs.io/projects/rev/en/stable/api.html): For programming motor controllers that are Spark or SparkMAX.
  - [CTRE](https://api.ctr-electronics.com/phoenix6/release/python/): For CTR Electronics such as Talon FX.

#### How to Use

The docs tell you about what objects are available to you and what actions each object can take. Let's demonstrate by using the docs to understand more deeply what is going on in the tutorial.

##### Ex 1
For example, on line 33 in `autonomousInit()`, there is a `self.timer.restart()`. The only explanation given in the tutorial is "we restart the Timer in this method," which unfortunately isn't very helpful.

So first we check what type of object `self.timer` even is. Scrolling up to line 24 in `robotInit()`, we see that it is `wpilib.Timer()`. Thus we go to the wpilib documentation.

We first notice there is no wpilib.Timer package, meaning Timer() probably exists in the main wpilib package itself. Checking inside the [wpilib package](https://robotpy.readthedocs.io/projects/robotpy/en/stable/wpilib.html), we indeed do see a Timer() object. Clicking into that we can finally scroll down to [`reset()`](https://robotpy.readthedocs.io/projects/robotpy/en/stable/wpilib.html) to see what it is doing.

##### Ex 2
As a more complicated example, on line 41 we have `self.robotDrive.arcadeDrive(0.5, 0, squareInputs=False)` explained simply as "drives forward at half speed". We can see this is a `wpilib.drive.DifferentialDrive()` object and can be found in package `wpilib.drive`.

In the differential drive [page](https://robotpy.readthedocs.io/projects/robotpy/en/stable/wpilib.drive/DifferentialDrive.html#wpilib.drive.DifferentialDrive) we get a full description of how it works, what coordinate frame it expects, and can see even cooler stuff available to us such as `curvatureDrive()`.
