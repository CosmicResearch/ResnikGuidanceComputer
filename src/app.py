			#!/usr/bin/python3

"""
    Guidance Computer Software
    Copyright (C) 2016 Associacio Cosmic Research

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import ConfigParser
from Queue import Queue
from Processes import SensorProcess, CommunicatorProcess
import RPi.GPIO as GPIO

def main():
    config = ConfigParser.ConfigParser()
    config.read("./config.ini")
    led = int(config.get("LED", "PowerLedPin"))
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, GPIO.HIGH)
    readings = Queue()
    orders = Queue()
    logger = CommunicatorProcess.CommunicatorProcess(orders, readings)
    sensor = SensorProcess.SensorProcess(readings, orders)
    logger.start()
    sensor.start()
    try:
        logger.join()
        sensor.join()
    except:
        sensor.stop()
        logger.stop()

if __name__ == "__main__":
    main()
