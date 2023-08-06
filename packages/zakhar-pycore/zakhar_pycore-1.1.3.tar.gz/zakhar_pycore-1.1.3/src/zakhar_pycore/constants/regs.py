# *************************************************************************
#
# Copyright (c) 2021 Andrei Gramakov. All rights reserved.
#
# This file is licensed under the terms of the MIT license.
# For a copy, see: https://opensource.org/licenses/MIT
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************


class Register(int):
    def __new__(cls, address: int, *args, **kwargs):
        if address < 0:
            raise ValueError("positive types must not be less than zero")
        return super().__new__(cls, address)

    def __init__(self, address: int, access_type: str = "", comment="", *args, **kwargs) -> None:
        super().__init__()
        self.access_type = access_type
        self.comment = comment


class REGS:
    class MOVING_PLATFORM:
        CMD = Register(0x00, "R/W", "Command register. The device is reading commands from here")
        ARG = Register(0x01, "R/W", "Optional argument of the command")
        MODE = Register(0x02, "RO", "The Mode register")
        SPEED = Register(0x03, "RO", "Current speed mode (0-3)")
        ANGLE_X_S = Register(0x04, "RO", "Sing of the angle for X (0,1)")
        ANGLE_X = Register(0x05, "RO", "The value of the X angle (0-180)")
        ANGLE_Y_S = Register(0x05, "RO", "Sing of the angle for Y (0,1)")
        ANGLE_Y = Register(0x06, "RO", "The value of the Y angle (0-180)")
        ANGLE_Z_S = Register(0x07, "RO", "Sing of the angle for Z (0,1)")
        ANGLE_Z = Register(0x08, "RO", "The value of the Z angle (0-180)")

    class SENSOR_PLATFORM:
        CMD = Register(0x00, "R/W", "Command register. The device is reading commands from here")
        ARG = Register(0x01, "R/W", "Optional argument of the command")
        DIST_L = Register(0x02, "RO", "Value of the left distance sensor in cm")
        DIST_C = Register(0x03, "RO", "Value of the central distance sensor in cm")
        DIST_R = Register(0x04, "RO", "Value of the right distance sensor in cm")
        LIGHT_HI = Register(0x05, "RO", "Value of the light sensor, higher part. The less the brighter")
        LIGHT_LO = Register(0x06, "RO", "Value of the light sensor, lower part. The less the brighter")

    class FACE_MODULE:
        CMD = Register(0x00, "R/W", "Command register. The device is reading commands from here")
        ARG = Register(0x01, "R/W", "Optional argument of the command")
