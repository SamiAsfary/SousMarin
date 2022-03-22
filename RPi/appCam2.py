#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  	appCam.py
#  	based on tutorial ==> https://blog.miguelgrinberg.com/post/video-streaming-with-flask
# 	PiCam Local Web Server with Flask
# MJRoBot.org 19Jan18

from flask import Flask, render_template, Response
app = Flask(__name__)

# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera
import RPi.GPIO as GPIO
#import Adafruit_DHT
import time

# get data from DHT sensor
# def getDHTdata():		
# 	DHT22Sensor = Adafruit_DHT.DHT22
# 	DHTpin = 16
# 	hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
# 	
# 	if hum is not None and temp is not None:
# 		hum = round(hum)
# 		temp = round(temp, 1)
# 	return temp, hum


# @app.route("/")
# def test():
# 	timeNow = time.asctime( time.localtime(time.time()) )
# 	#temp, hum = getDHTdata()
# 	
# 	templateData = {
#       'time': timeNow,
#       'temp': 40,
#       'hum'	: 40
# 	}
# 	return render_template('index.html', **templateData)
motors = {
    33 : {'name' : 'Left', 'pin' : 33, 'speed' : 0},
    12 : {'name' : 'Right', 'pin' : 12, 'speed' : 0}   
    }


GPIO.setmode(GPIO.BOARD)


for pin in motors:
    GPIO.setup(motors[pin]['pin'],GPIO.OUT)
    motors[pin]["pwm"] = GPIO.PWM(motors[pin]['pin'],1000)
    motors[pin]["pwm"].start(0)


@app.route('/')
def cam():
	"""Video streaming home page."""
	
	return render_template('index.html')

@app.route('/<motor>/<status>')
def action(motor, status):
    
#     templateData = {
#                 d_percent : status,
#                 g_percent : status
#                 }
    
#     for pin in motors:
#         if motors[pin]['name'] == motor:
#             motors[pin]['speed'] = motors[pin]['speed'] + 10*int(status)
#             if status == '0':
#                 motors[pin]['speed'] = 0
#             if motors[pin]['speed'] < 0:
#                 motors[pin]['speed'] = 0
#             if motors[pin]['speed'] > 100:
#                 motors[pin]['speed'] = 100
#             motors[pin]['pwm'].ChangeDutyCycle(motors[pin]['speed'])
#             
    return render_template('index.html')
    
    


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port =80, threaded=True)
