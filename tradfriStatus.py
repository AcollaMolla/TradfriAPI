# file        : tradfri/tradfriStatus.py
# purpose     : getting status from the Ikea tradfri smart lights
#
# author      : harald van der laan
# date        : 2017/11/01
# version     : v1.2.0
#
# changelog   :
# - v1.2.0      update for new gateway 1.1.15 issues                    (harald)
# - v1.1.0      refactor for cleaner code                               (harald)
# - v1.0.0      initial concept                                         (harald)

"""
    tradfriStatus.py - module for getting status of the Ikea tradfri smart lights
    This module requires libcoap with dTLS compiled, at this moment there is no python coap module
    that supports coap with dTLS. see ../bin/README how to compile libcoap with dTLS support
"""
import sys
import os
import json
global coap
coap = '/usr/local/bin/coap-client'
timeout = 5

def tradfri_get_lightbulb(hubip, apiuser, apikey, deviceid):
	tradfriHub = 'coaps://{}:5684/15001/{}' .format(hubip, deviceid)
	api = '{} -m get -u "{}" -k "{}" "{}" -B {} 2> /dev/null' .format(coap, apiuser, apikey, tradfriHub, timeout)
	if(os.path.exists(coap)):
		result = os.popen(api)
		errorResult = os.popen(api +  " 2>&1")
		errorResponse =  (errorResult.read().strip('\n').split('\n')[-3])
	else:
		sys.stderr.write('[-] libcoap: could not find libcoap.\n')
		sys.exit(1)
	try:
		response = json.loads(result.read().strip('\n').split('\n')[-1])
	except:
		response =  errorResponse
	return response

def tradfri_get_devices(hubip, apiuser, apikey):
	tradfriHub = 'coaps://{}:5684/15001' .format(hubip)
	api = '{} -m get -u "{}" -k "{}" "{}" -B {} 2> /dev/null' .format(coap, apiuser, apikey, tradfriHub, timeout)
	if os.path.exists(coap):
		result = os.popen(api)
	else:
		sys.stderr.write('[-] libcoap: could not find libcoap.\n')
		sys.exit(1)
	return json.loads(result.read().strip('\n').split('\n')[-1])
