#!/usr/bin/python3
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import RPi.GPIO as GPIO
import Adafruit_DHT
import datetime
import time
# To connect to MariaDB using the MySQL Python module in your program
import mysql.connector as mariadb

sampleFreq = 20

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
    sys.exit(1)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
# get data from DHT sensor
def getDHTdata():	
	hum, temp = Adafruit_DHT.read_retry(sensor,pin)
	# Un-comment the line below to convert the temperature to Fahrenheit.
	# temp = temp * 9/5.0 + 32

	
	if hum is not None and temp is not None:
		hum = round(hum,1)
		temp = round(temp, 1)
	else:
                print('Failed to get reading. Try again!')
                sys.exit(1)

	return temp, hum

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!

# log sensor data on database
def logData (temp, hum):	
	#get the current date and time
	now = datetime.datetime.now()

	# establish a database connection
	mariadb_connection = mariadb.connect(user='rabiy', password='tel27652322', database='Weather')
	# to start interacting with the database and running queries, you need to instantiate the cursor object
	cursor = mariadb_connection.cursor()
	#You can insert rows into a table with the following
	cursor.execute("INSERT INTO DHT11 values(%s, %s, %s)", (now.strftime("%Y-%m-%d %H:%M:%S"),temp,hum))
	# By default AUTOCOMMIT is disabled, meaning queries are not committed, so no data will be saved until you manually commit with the connection commit method
	mariadb_connection.commit()
	mariadb_connection.close()

# display database data
def displayData():
	mariadb_connection = mariadb.connect(user='rabiy', password='tel27652322', database='Weather')
	cursor = mariadb_connection.cursor()
	cursor.execute("SELECT * FROM DHT11 ORDER BY Timestamp DESC LIMIT 1 ")
	record = cursor.fetchone()
	print ('| DateTime: {}  ||  Temperature: {}°C  ||  Humidity: {}% |'.format(record[0],record[1],record[2]))
	mariadb_connection.close()


if __name__ == "__main__":

	try :
		while True :		
			temp, hum = getDHTdata()
			logData (temp, hum)
			displayData()
			time.sleep(sampleFreq)

	except KeyboardInterrupt:
		GPIO.cleanup()
	except mariadb.Error as error:
    		print("Error: {}".format(error))


