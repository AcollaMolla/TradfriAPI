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
	else:
		sys.stderr.write('[-] libcoap: could not find libcoap.\n')
		sys.exit(1)
	return json.loads(result.read().strip('\n').split('\n')[-1])
