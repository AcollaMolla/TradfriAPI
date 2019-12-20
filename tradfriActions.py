#!/usr/bin/env python

# file        : tradfri/tradfriActions.py
# purpose     : module for controling status of the Ikea tradfri smart lights
#
# author      : harald van der laan
# date        : 2017/04/10
# version     : v1.1.0
#
# changelog   :
# - v1.1.0      refactor for cleaner code                               (harald)
# - v1.0.0      initial concept                                         (harald)

"""
    tradfri/tradfriActions.py - controlling the Ikea tradfri smart lights

    This module requires libcoap with dTLS compiled, at this moment there is no python coap module
    that supports coap with dTLS. see ../bin/README how to compile libcoap with dTLS support
"""

# pylint convention disablement:
# C0103 -> invalid-name
# pylint: disable=C0103

import sys
import os

global coap
coap = '/usr/local/bin/coap-client'

def tradfri_power_light(hubip, userid, securityid, lightbulbid, value):
    """ function for power on/off tradfri lightbulb """
    print('here now')
    tradfriHub = 'coaps://{}:5684/15001/{}' .format(hubip, lightbulbid)

    if value == 'on':
        payload = '{ "3311": [{ "5850": 1 }] }'
    else:
        payload = '{ "3311": [{ "5850": 0 }] }'

    api = '{} -m put -u "{}" -k "{}" -e \'{}\' "{}"' .format(coap, userid, securityid,
                                                                          payload, tradfriHub)

    if os.path.exists(coap):
        os.popen(api)
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)

    return True


def tradfri_dim_light(hubip, userid, securityid, lightbulbid, value):
    """ function for dimming tradfri lightbulb """
    print('dim light func')
    tradfriHub = 'coaps://{}:5684/15001/{}'.format(hubip, lightbulbid)
    payload = '{ "3311" : [{ "5851" : %s }] }' % int(value)

    api = '{} -m put -u "{}" -k "{}" -e \'{}\' "{}"'.format(coap, userid, securityid,
                                                                         payload, tradfriHub)

    if os.path.exists(coap):
        result = os.popen(api)
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)
    return True

def tradfri_color_light(hubip, securityid, lightbulbid, value):
    """ function for color temperature tradfri lightbulb """
    tradfriHub = 'coaps://{}:5684/15001/{}'.format(hubip, lightbulbid)

    if value == 'warm':
        payload = '{ "3311" : [{ "5709" : %s, "5710": %s }] }' % ("33135", "27211")
    elif value == 'normal':
        payload = '{ "3311" : [{ "5709" : %s, "5710": %s }] }' % ("30140", "26909")
    elif value == 'cold':
        payload = '{ "3311" : [{ "5709" : %s, "5710": %s }] }' % ("24930", "24684")

    api = '{} -m put -u "Client_identity" -k "{}" -e \'{}\' "{}"'.format(coap, securityid,
                                                                         payload, tradfriHub)

    if os.path.exists(coap):
        result = os.popen(api)
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)

    return result

def tradfri_power_group(hubip, securityid, groupid, value):
    """ function for power on/off tradfri lightbulb """
    tradfriHub = 'coaps://{}:5684/15004/{}' .format(hubip, groupid)

    if value == 'on':
        payload = '{ "5850" : 1 }'
    else:
        payload = '{ "5850" : 0 }'

    api = '{} -m put -u "Client_identity" -k "{}" -e \'{}\' "{}"' .format(coap, securityid,
                                                                          payload, tradfriHub)

    if os.path.exists(coap):
        result = os.popen(api)
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)

    return result


def tradfri_dim_group(hubip, securityid, groupid, value):
    """ function for dimming tradfri lightbulb """
    tradfriHub = 'coaps://{}:5684/15004/{}'.format(hubip, groupid)
    dim = float(value) * 2.55
    payload = '{ "5851" : %s }' % int(dim)

    api = '{} -m put -u "Client_identity" -k "{}" -e \'{}\' "{}"'.format(coap, securityid,
                                                                         payload, tradfriHub)

    if os.path.exists(coap):
        result = os.popen(api)
    else:
        sys.stderr.write('[-] libcoap: could not find libcoap\n')
        sys.exit(1)

    return result

def tradfri_set_device_name(hubip, userid, securityid, deviceid, value):
	tradfriHub = 'coaps://{}:5684/15001/{}' .format(hubip,deviceid)
	payload = '{ "9001" : "'+value+'" }'
	api = '{} -m put -u "{}" -k "{}" -e \'{}\' "{}"' .format(coap, userid, securityid, payload, tradfriHub)
	if os.path.exists(coap):
		os.popen(api)
	else:
		sys.stderr.write('[-] libcoap: could not find libcoap')
		sys.exit(1)
	return True 
