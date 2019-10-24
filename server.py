import tradfriActions
import tradfriStatus
import codecs
import json
import ConfigParser
from flask import Flask
from flask import request
from flask_restful import Resource, Api
from flask import render_template, make_response
from json import JSONEncoder
from flask import abort

app = Flask(__name__)
api = Api(app)
conf = ConfigParser.ConfigParser()
#script_dir = os.path.dirname(os.path.realpath(__file__))
conf.read('tradfri.cfg')
security_id = conf.get('tradfri', 'apikey')
hub_ip = conf.get('tradfri', 'hubip')
user_id = conf.get('tradfri', 'userid')
print(security_id)
print(hub_ip)
            
class Device:
	def __init__(self, DeviceID, isActive):
		self.DeviceID = DeviceID
		self.isActive = isActive

class Power(Resource):
	def post(self):
		lightbulb_id = request.args.get("id")
		command = request.args.get("powerOn")
		response = tradfriActions.tradfri_power_light(hub_ip, user_id,  security_id, lightbulb_id, command)
		return response

class GetAllDevices(Resource):
	def get(self):
		device1 = '{"DeviceID":"65537", "powerOn":"off"}'
		device2 = '{"DeviceID":"65538", "powerOn":"off"}'
		x = json.loads(device1)
		y = json.loads(device2)
		deviceList = [x, y]
		return deviceList

class GetDevice(Resource):
	def get(self):
		lightbulb_id = request.args.get("id")
		response = tradfriStatus.tradfri_get_lightbulb(hub_ip, user_id,  security_id, lightbulb_id)
		try:
			test = json.dumps(response)
		except ValueError as e:
			return 0
		try:
			test2 = json.loads(test)
		except ValueError as e:
			return 0
		return test2['3311']

class Index(Resource):
	def get(self):
		return make_response(render_template('index.html'))

api.add_resource(Power, '/power')
api.add_resource(GetAllDevices, '/getAllDevices')
api.add_resource(GetDevice, '/getDevice')
api.add_resource(Index, '/')
app.run(host='0.0.0.0', port='3000')
