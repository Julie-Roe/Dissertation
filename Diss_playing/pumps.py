import flask
import RPi.GPIO as GPIO
from read_thermometer import read_temp
from flask import Flask, render_template, request
app = flask.Flask(__name__)

GPIO.setmode(GPIO.BCM)



pins = {
    5:{'name' : 'Pump One', 'state' : GPIO.LOW},
    6:{'name' : 'Pump Two', 'state' : GPIO.LOW},
    13:{'name' : 'Heat One', 'state' : GPIO.LOW},
    19:{'name' : 'Heat Two', 'state' : GPIO.LOW}
    }
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    
@app.route("/")

def pump_status():
   
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
        temp_c = read_temp()
        templateData = {'pins' : pins, 'temp_c' : temp_c}
        return render_template("index.html", **templateData)
    
    
@app.route("/<changePin>/<action>")

def action(changePin, action):
    temp_c = read_temp()
    changePin =int(changePin)
    deviceName = pins[changePin]['name']
    if action =="on":
        GPIO.output(changePin, GPIO.HIGH)
        message = " Turned " + deviceName + " on."
    if action =="off":
        GPIO.output(changePin, GPIO.LOW)
        message = "Turned " + deviceName + " off."
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
        
    templateData = {
            'message' : message,
            'pins' : pins,
            'temp_c' : temp_c
            
            }
    return render_template("index.html", **templateData)
app.run()