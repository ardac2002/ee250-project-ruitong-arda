import paho.mqtt.client as mqtt
import os
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)


@app.route('/')
def home():
    global TempValue
    return render_template("index.html", Temperature = TempValue)

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == "POST":
        if 'manual' in request.form.keys():
            client.publish("RC_AC/manual", "true")
        else:
            client.publish("RC_AC/manual", "false")
        r = request.form["red"]
        b = request.form["blue"]
        g = request.form["green"]
        client.publish("RC_AC/ledR", r)
        client.publish("RC_AC/ledG", g)
        client.publish("RC_AC/ledB", b)
    return redirect(url_for('home'))
    
def custom_callback(client, userdata, message):
    # prints the temperature value 
    print("VM: " + str(message.payload, "utf-8"))
    global TempValue
    TempValue = int(float(str(message.payload, "utf-8")))
   
    
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to interested topics here
    client.subscribe("RC_AC/TempSensor")
    client.message_callback_add("RC_AC/TempSensor", custom_callback)


if __name__ == "__main__":
    client = mqtt.Client()
    #client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
    TempValue = 0
    app.secret_key = os.urandom(12)
    app.run()