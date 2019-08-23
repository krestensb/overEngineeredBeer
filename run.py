from w1thermsensor import W1ThermSensor
from time import sleep
from gpiozero import LED, Button

## Setup brewing parameters
strike_temp = 78
mash_temp   = 65
sparge_temp = 78

mash_time   = 60
boil_time   = 60

mash_settle_time = 60 #seconds

first_hop   = 40
second_hop  = 10
third_hop   = 10
forth_hop   = 10

## Setup GPIO pins
heater_1 = LED(17)
heater_2 = LED(27)
heater_3 = LED(25)

pump_1   = LED(99)
pump_2   = LED(99)

valve_sol  = LED(99)
valve_ball  = (99) ## Need driver

level_1  = Button(99)
level_2  = Button(99)

buzzer   = LED(99)

## Status parameters

strike_status     = 0
mash_status       = 0
sparge_status     = 0
boil_status       = 0
mash_level_status = 0
transfer_strike_status = 0

## Start - Code to get sensor ID's
#for sensor in W1ThermSensor.get_available_sensors():
#    print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
##

## Setup temp sensors
sensor1 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "sensorID_1")
sensor2 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "sensorID_2")
##

temp1 = sensor1.get_temperature()
temp2 = sensor2.get_temperature()

## Main loop

heat_strike_water()
transfer_strike_water()
timer(mash_settle_time) # Mash settle for 1 minute
circulate_mash(1)

mash_pid_controller()

## Heat strike water (wait for temp)
def heat_strike_water():
    while strike_status == 0:
        temp1 = sensor1.get_temperature()
        if temp1 > strike_temp:
            strike_status = 1
            heater1.off
        else: 
            heater_1.on
            strike_status = 0
    print ("Strike water is on temperature!")
    return strike_status

## Transfer strike water (open valve and wait for level sensor)
def transfer_strike_water():
    while transfer_strike_status == 0:
        if level_1.when_released():
            pump1.on()
            transfer_strike_status = 0
        else:
            pump1.off()
            transfer_strike_status = 1
    print ("Strike water is transfered")
    return transfer_strike_status

## Timer
def timer(wait_time):
    for i in range(wait_time):
        time.sleep(1)
        print (wait_time - i)
    return

## Circulate mash (turn on pump)
def circulate_mash(status):
    if status == 1:
        pump2.on()
    elif status == 0:
        pump2.of()
    return mash_status = 0

## Control temp in mash (pid controll)
def mash_pid_controller():
    return

## Transfer worth to boiler (turn on pump)
def transfer_to_boil():
    return

## Sparge (turn on pump)
def sparge():
    return

## Boil (wait)
def boil():
    return


