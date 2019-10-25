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
cookie_name = conf.get('cookie', 'cookiename')
cookie_value = conf.get('cookie', 'cookievalue')
print(security_id)
print(hub_ip)
            
class Device:
	def __init__(self, DeviceID, isActive):
		self.DeviceID = DeviceID
		self.isActive = isActive

def GetCookie(cookies):
	if cookie_name in cookies:
		if cookie_value in cookies.get(cookie_name):
			return True
		else:
			return False
	else:
		return False

class Power(Resource):
	def post(self):
		if GetCookie(request.cookies):
			lightbulb_id = request.args.get("id")
			command = request.args.get("powerOn")
			response = tradfriActions.tradfri_power_light(hub_ip, user_id,  security_id, lightbulb_id, command)
			return response
		else:
			abort(404)

class GetAllDevices(Resource):
	def get(self):
		if GetCookie(request.cookies):
			deviceList = tradfriStatus.tradfri_get_devices(hub_ip, user_id, security_id)
			return deviceList
		else:
			abort(404)

class GetDevice(Resource):
	def get(self):
		if GetCookie(request.cookies):
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
		else:
			abort(404)

class GetDeviceType(Resource):
	def get(self):
		if GetCookie(request.cookies):
			device_id = request.args.get("id")
			response = tradfriStatus.tradfri_get_lightbulb(hub_ip, user_id, security_id, device_id)
			return response
		else:
			abort(404)

class SetDeviceBrightness(Resource):
	def post(self):
		if GetCookie(request.cookies):
			device_id = request.args.get("id")
			value = request.args.get("value")
			response = tradfriActions.tradfri_dim_light(hub_ip, user_id, security_id, device_id, value)
			return response
		else:
			abort(404)

class Ulvsby(Resource):
	def get(self):
		res = make_response(render_template('ulvsby.html'))
		res.set_cookie(cookie_name, cookie_value, max_age=63113852)
		return res

class Index(Resource):
	def get(self):
		if GetCookie(request.cookies):
			res = make_response(render_template('index.html'))
			return res
		else:
			abort(404)

api.add_resource(Power, '/power')
api.add_resource(GetAllDevices, '/getAllDevices')
api.add_resource(GetDevice, '/getDevice')
api.add_resource(GetDeviceType, '/getDeviceType')
api.add_resource(SetDeviceBrightness, '/setDeviceBrightness')
api.add_resource(Ulvsby, '/ulvsby')
api.add_resource(Index, '/')
app.run(host='0.0.0.0', port='3000')
