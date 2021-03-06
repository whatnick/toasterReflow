"""
 toasterReflow.py
 Alexander Hiam
 
 A web interface for the toasterReflow reflow toaster oven control
 library.

 Apache 2.0 license.
"""

import inspect, json, threading
from flask import Flask, g, redirect, url_for, request,\
                  session, render_template, flash
from functools import wraps

from toasterReflow import *
from bbio import *
from bbio.libraries.MAX31855 import MAX31855

# Set variables for the pins connected to the ADC:
#PyBBIO now uses hardware SPI for MAX31855
#data_pin = GPIO1_15  # P8.15
#clk_pin  = GPIO1_14  # P8.16
#cs_pin   = GPIO0_27  # P8.17

heater2_pin = "GPIO2_25"  # P8.18
heater3_pin = "GPIO2_24"
heater_pin = "GPIO2_23"
#fan_pin    = GPIO1_31  # P8.20


#data_pin = GPIO2_6
#clk_pin  = GPIO2_10
#cs_pin   = GPIO2_8

fan_pin    = "GPIO2_22"
SPI1.open()
thermo = MAX31855(SPI1,0)
print thermo.readTempC()
delay(100)

reflow_oven = Oven(heater_pin, 0, fan_pin ,heater2_pin, heater3_pin)
rs_buzz = buzzer("P8_12")
#Do a test buzz
rs_buzz.buzz(1000,0.5)

app = Flask(__name__)
app.config.from_pyfile('toasterReflow.cfg')

app.config['NAVIGATION'] = [['Oven Control', '/'],
                            ['Profile Editor', '/profile-editor']]


#Initialise OLED
oled_init()
oled_clearDisplay()
oled_setNormalDisplay()

# Global variable to store the currently selected profile; used when
# starting reflow:
current_profile = None

def requireLogin(f):
  @wraps(f)
  def loginCheck(*args, **kwargs):
    if session.get('logged_in') is None:
      # User not logged in, redirect to login page
      return redirect(url_for('login', next=request.url))
    return f(*args, **kwargs)
  return loginCheck

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      return redirect(url_for('ovenControl'))
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  """ Log user out and redirect to the root page. """
  session.pop('logged_in', None)
  flash('Logged out')
  return redirect('/')

@app.route('/')
@requireLogin
def ovenControl():
  return render_template('oven.html')

@app.route('/profile-editor')
@requireLogin
def list_profiles():
  #for i in inspect.getmembers(profiles, lambda member: type(member) == dict):
  #  if i[0] in dir(profiles) and i[0] != "__builtins__":
  #  #  profiles_str += "<h3>%s:</h3>\n<p>%s<\p>\n" % (i[0], i[1])
  #    profiles_str += '<h3><a href="/profiles/%s">%s</a></h3>' % (i[0], i[0])
  
  return render_template('profile-editor.html')


#-- Oven API --#
@app.route('/profiles', methods=['GET'])
@requireLogin
def getProfileNames():
  """ Returns a JSON list of all the profile names. """
  profile_names = []
  for name, content in inspect.getmembers(profiles, 
                                          lambda member: type(member)==dict):
    if name in dir(profiles) and name != "__builtins__":
      profile_names.append(name)
  return json.dumps(profile_names)

@app.route('/profiles/<profile_name>', methods=['GET'])
@requireLogin
def getProfile(profile_name):
  """  """
  for name, content in inspect.getmembers(profiles, 
                                          lambda member: type(member)==dict):
    if (name == profile_name):
      global current_profile
      current_profile = content
      return json.dumps(reflow_oven.generateMap(content))
  return "Error: profile not found: '%s'" % name, 404

@app.route('/phases', methods=['GET'])
@requireLogin
def getPhases():
  """ Returns JSON list of the reflow phases. """
  return json.dumps(PHASES)

@app.route('/current-phase', methods=['GET'])
@requireLogin
def getCurrentPhase():
  """ Returns the current reflow phases. """
  oled_setTextXY(3,0)
  oled_putString(reflow_oven.current_phase+"     ")
  return json.dumps(reflow_oven.current_phase)

@app.route('/current-step', methods=['GET'])
@requireLogin
def getCurrentStep():
  """ Returns the current step number in the current reflow phase. """
  return json.dumps(reflow_oven.current_step)

@app.route('/time-step', methods=['GET'])
@requireLogin
def getTimeStep():
  """ Returns the reflow oven's time step. """
  return json.dumps(TIME_STEP_MS)

@app.route('/realtime-data', methods=['GET'])
@requireLogin
def getRealtimeData():
  """ Returns the reflow oven's real-time data series. """
  return json.dumps(reflow_oven.realtime_data)

@app.route('/status', methods=['GET'])
@requireLogin
def getStatus():
  """ Returns 'on' if the oven is running, 'off' if not. """
  return json.dumps('on' if reflow_oven.current_phase else 'off')

@app.route('/error', methods=['GET'])
@requireLogin
def getError():
  """ Returns oven error message. """
  return json.dumps(reflow_oven.error)


@app.route('/control/temperature', methods=['GET'])
@requireLogin
def temperature():
  """ Returns the oven temperature in Celsius, or error message if error 
      encountered. """
  temp = reflow_oven.getTemp()
  if (temp == None): 
    return json.dumps(reflow_oven.thermocouple.error)
  oled_setTextXY(2,0)
  oled_putString("Temp:"+str(temp))
  return json.dumps(temp)

@app.route('/control/heater', methods=['GET', 'POST'])
@requireLogin
def heaterControl():
  if (request.method == 'GET'):
    return json.dumps(reflow_oven.heat_state)
  else:
    state = request.form['state']
    if (state == 'on'):
      reflow_oven.heatOn()
      return json.dumps(state)
    elif (state == 'off'):
      reflow_oven.heatOff()
      return json.dumps(state)
    return "Error: Unkown heater state '%s'" % state, 404

@app.route('/control/fan', methods=['GET', 'POST'])
@requireLogin
def fanControl():
  if (request.method == 'GET'):
    return json.dumps(reflow_oven.fan_state)
  else:
    state = request.form['state']
    if (state == 'on'):
      reflow_oven.fanOn()
      return json.dumps(state)
    elif (state == 'off'):
      reflow_oven.fanOff()
      return json.dumps(state)
    return "Error: Unkown heater state '%s'" % state, 404

@app.route('/control/start', methods=['POST'])
@requireLogin
def startReflow():
  def reflowInThread():
    try: reflow_oven.run(current_profile)
    except Exception, e:
      print e
  threading.Thread(target=reflowInThread).start()
  return ''

@app.route('/control/stop', methods=['POST'])
@requireLogin
def stopReflow():
  reflow_oven.abort = True
  return ''

#--------------------#


if __name__ == "__main__":
  app.debug=True
  app.run(host='0.0.0.0',port=8000)

  # Make sure the oven is off once the server is stopped:
  reflow_oven.abort = True
