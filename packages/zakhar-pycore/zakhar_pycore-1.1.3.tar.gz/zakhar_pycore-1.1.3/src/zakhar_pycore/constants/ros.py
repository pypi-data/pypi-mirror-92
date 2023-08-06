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


class ROS:
    class TOPICS:
        I2C = "i2c"
        I2C_EXECUTER = "i2c_executer"
        DEVICECMD = "DeviceCmd_from_ConceptTranslator"
        MAIN_SENSOR_INTERPRETER = "main_sensor_interpreter"
        SENSOR_DATA = "SensorData_for_SensorInterpreter"
        EMOTION_PARAMS = "EmotionParams"

    class SERVICES:
        CONCEPT_TO_COMMAND = "concept2commands_interpreter"
        SENSOR_DATA_TO_CONCEPT = "data2concept_interpreter"
        I2C = "i2c_server"
        EMOTIONCORE_WRITE = "EmotionCoreWrite"
        EMOTIONCORE_DATADSC = "EmotionCoreDataDescriptor"
