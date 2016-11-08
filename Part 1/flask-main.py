#! /usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import time
import logging
import configpi
import os

file_path = os.path.dirname(__file__)
sys.path.insert(0, file_path)

from flask import Flask, render_template, jsonify, Response, request
from backend import *

app = Flask(__name__)

backend = Backend_with_dimmers_and_sensors()






#######################################################################################################################
############# INDEX PAGE ##############################################################################################
#######################################################################################################################


@app.route('/', strict_slashes=False)
def index():
    # returns a html page with a list of routes
    return render_template("index.html", title=configpi.name)



#######################################################################################################################
############# NETWORK #################################################################################################
#######################################################################################################################

"""
@api {get} /network/info  get_network_info
@apiName get_network_info
@apiGroup Network




@apiSuccess {String} Network_Home_ID Network's ID

@apiSuccess {JSON} Node_<Number> A JSON containing node's information (for each node). See below

@apiSuccess {boolean} Is_Ready Node status

@apiSuccess {String[]} Neighbours Node's neighbours

@apiSuccess {Number} Node_ID Node's ID

@apiSuccess {String} Node_location Node's location

@apiSuccess {String} Node_name Node's name

@apiSuccess {String} Product_name Node's product name

@apiSuccess {String} Query_stage Query Stage

@apiSuccess {Number} Query_stage_(%) Query Stage (percentage)





@apiSuccessExample {json} Example of result in case of success:
{
"Network Home ID": "0xe221b13f",
"Node 1": {
    "Is Ready": true,
    "Neighbours": "2",
    "Node ID": "1",
    "Node location": "",
    "Node name": "",
    "Product name": "Z-Stick Gen5",
    "Query Stage": "Complete",
    "Query Stage (%)": "100 %"
  },
"Node 2": {
    "Is Ready": true,
    "Neighbours": "1",
    "Node ID": "2",
    "Node location": "",
    "Node name": "",
    "Product name": "MultiSensor 6",
    "Query Stage": "Complete",
    "Query Stage (%)": "100 %"
  }
}



@apiDescription Gets information about the Z-Wave network in a JSON format
"""

@app.route('/network/info', strict_slashes=False)
def network_info():
    return backend.network_info()




"""
@api {post} /network/set_nodes_basic_configuration set_nodes_basic_configuration
@apiName set_nodes_basic_configuration
@apiGroup Network

@apiParam {Number} Group_Interval Number of seconds between two successive transfers of measures
@apiParam {Number} Group_Reports Number identifying measures sent by the sensor
@apiParam {Number} Wake-up_Interval Number of seconds between two node's wake-ups

@apiParamExample {json} Request-Exemple :
    {
        'Group_Interval' : '241',
        'Group_Reports' : '480',
        'Wake-up_Interval' : '480'
    }

@apiSuccess {String} Message Description of the new nodes' configuration.

@apiDescription Configure all nodes of the network with a predefined configuration. This methods configures only Group 1. All measurements (temperature, luminosity, motion and humidity) must be retrieved from the sensors after a given period of time (Group_Interval Number).
"""
@app.route('/network/set_nodes_basic_configuration', methods=['GET','POST'], strict_slashes=False)
def network_configureNodes():
    # configure all the nodes of the network with a specific configuration
    if request.method=='POST':
        content = request.get_json()
        if all(item in content.keys() for item in ['Group_Interval','Group_Reports','Wake-up_Interval']):
            Grp_interval = int(content['Group_Interval'])
            Grp_reports = int(content['Group_Reports'])
            Wakeup_interval = int(content['Wake-up_Interval'])
            return backend.set_basic_nodes_configuration(Grp_interval,Grp_reports,Wakeup_interval)
        return 'wrong input'
    return 'use POST method'


"""
@api {get} /network/get_nodes_configuration get_nodes_configuration
@apiName get_nodes_configuration
@apiGroup Network




@apiSuccess {String} Network_Home_ID Network's ID

@apiSuccess {JSON} Node_<Number> A JSON containing node's informations that are detailed above (for each node except the controller)

@apiSuccess {String} Enable_Motion_Sensor Motion sensor level

@apiSuccess {Number} Group1_Interval Number of seconds between two Group1 measurements transmissions

@apiSuccess {Number} Group1_Reports A number specifying measurements sent in this group (set to 241 to send all measurements on this group)

@apiSuccess {Number} Group2_Interval Number of seconds between two Group2 measurements transmissions

@apiSuccess {Number} Group2_Reports A number specifying measurements sent in this group (set to 0 because no measurements will be sent on this group)

@apiSuccess {Number} Group3_Interval Number of seconds between two Group3 measurements transmissions

@apiSuccess {Number} Group3_Reports A number specifying measurements sent in this group (set to 0 because no measurements will be sent on this group)

@apiSuccess {Number} Node_ID Node's ID

@apiSuccess {Number} Wake_up_Interval Number of seconds between two wake-ups




@apiSuccessExample {json} Example of result in case of success:
{
"Network Home ID": "0xe221b13f",
"Node 2": {
    "Enable Motion Sensor": "Enabled level 5 (maximum sensitivity",
    "Group 1 Interval": "3600",
    "Group 1 Reports": "241",
    "Group 2 Interval": "3600",
    "Group 2 Reports": "0",
    "Group 3 Interval": "3600",
    "Group 3 Reports": "0",
    "Node ID": "2",
    "Wake-up Interval": "3600"
  }
}
@apiDescription Gets the list of nodes and their configuration parameters in a JSON format. For each node, the system should provide the following information: Node ID, Motion sensor level, Wake_up_Interval and the report and interval of each group (there are three groups). See details in the documentation of the sensor: Aeon Labs MultiSensor 6 (Z-wave MultiSensor).

"""

@app.route('/network/get_nodes_configuration', strict_slashes=False)
def get_nodes_Configuration():
    # gets a html with the list of nodes with their config parameters
    return backend.get_nodes_Configuration()  ######## a revoir





"""
@api {get} /network/start start_network
@apiName start_network
@apiGroup Network

@apiSuccess {String} Message Confirmation that the Z-Wave Network Restarted

@apiDescription Starts the openzwave software representation of the network

"""

@app.route('/network/start', strict_slashes=False)
def start():
    # start software representation
    backend.start()
    return "Z-Wave Network Started"




"""
@api {get} /network/stop stop_netowrk
@apiName stop_netowrk
@apiGroup Network

@apiSuccess {String} Message Confirmation that the Z-Wave Network has stopped

@apiDescription Stops the openzwave software representation of the network

"""

@app.route('/network/stop', strict_slashes=False)
def stop():
    # stop the software representation
    backend.stop()
    time.sleep(2)
    return "Z-Wave Network Stopped"




"""
@api {get} /network/reset reset_network
@apiName Reset Network
@apiGroup Network

@apiSuccess {String} Message Confirmation that the Z-Wave Network has been reset

@apiDescription Resets the network's controller. Do not call this method before excluding (removing) the sensors connected to the controller.

"""

@app.route('/network/reset', strict_slashes=False)
def reset():
    # restart software representation
    backend.reset()
    return "Z-Wave Network Reset"





######################################################################################################################
############# NODES ##################################################################################################
######################################################################################################################
### THESE METHODS ARE SPECIALLY MADE FOR ALL TYPES OF NODES ##########################################################
######################################################################################################################


"""
@api {get} /nodes/get_nodes_list get_nodes_list
@apiName get_nodes_list
@apiGroup Nodes

@apiSuccess {String[]} JSON List of all nodes in the network in a JSON format

@apiDescription Lists all nodes in the network

"""

@app.route('/nodes/get_nodes_list', strict_slashes=False)
def nodes():
    # gets a list of all nodes in the network in a JSON format
    return backend.get_nodes_list()




"""
@api {put} /nodes/add_node add_node
@apiName add_node
@apiGroup Nodes

@apiSuccess {String} Message Node added successfully

@apiDescription Adds Node to the network by getting the controller into inclusion mode for 20 seconds. The node can not be a controller.

"""

@app.route('/nodes/add_node', methods=['PUT'], strict_slashes=False)
def add_node():
    # passes controller to inclusion mode
    return backend.addNode()



"""
@api {put} /nodes/remove_node remove_node
@apiName remove_node
@apiGroup Nodes

@apiSuccess {String} Message Node removed successfully

@apiDescription Removes Node from the network by getting the controller into exclusion mode for 20 seconds

"""

@app.route('/nodes/remove_node', methods=['PUT'], strict_slashes=False)
def remove_node():
    # passes controller to exclusion mode
    return backend.removeNode()




"""
@api {post} /nodes/set_parameter set_parameter
@apiName set_parameter
@apiGroup Nodes

@apiParam {Number} node_id Sensor's unique ID
@apiParam {Number} parameter_index Parameter's unique index  (See sensor manual)
@apiParam {Number} value new value of the parameter
@apiParam {Number} size size of value of the parameter (See sensor manual)

@apiParamExample {json} Request-Exemple :
    {
        'node_id' : '4',
        'parameter_index' : '101',
        'value' : '227',
        'size' : '4'
    }

@apiSuccess {String} parameter parameter's new value

@apiDescription Sets the value of a given parameter of a node

"""

@app.route('/nodes/set_parameter', methods=['GET', 'POST'],strict_slashes=False)
def set_config_param():
   # sets a config parameter of a sensor node
    if request.method=='POST':
        content = request.get_json()
        if all(item in content.keys() for item in ['node_id','parameter_index','value','size']):
            node = int(content['node_id'])
            param = int(content['parameter_index'])
            value = int(content['value'])
            size = int(content['size'])
            return backend.set_node_config_parameter(node, param, value, size)
        return 'wrong input'
    return 'use POST method'




"""
@api {get} /nodes/<node_id>/get_parameter/<parameter> get_parameter
@apiName get_parameter
@apiGroup Nodes

@apiParam {Number} node_id Sensor's unique ID
@apiParam {Number} parameter Parameter's unique index

@apiSuccess {String} parameter parameter's value

@apiDescription Gets the value of a given parameter of a node

"""

@app.route('/nodes/<int:node>/get_parameter/<int:param>', strict_slashes=False)
def get_config_param(node, param):
    # gets a config parameter of a sensor node
    return backend.get_node_config_parameter(node, param)




"""
@api {get} /nodes/<node_id>/get_battery get_battery_level
@apiName get_battery_level
@apiGroup Nodes

@apiParam {Number} node_id Sensor's unique ID

@apiSuccess {String} controller Controller name
@apiSuccess {String} location Location of the sensor
@apiSuccess {String} sensor Sensor's ID
@apiSuccess {String} type type of measurement
@apiSuccess {Number} value battery level (%)
@apiSuccess {Number} updateTime Timestamp at the measures' reception

@apiSuccessExample {json} Example of result in case of success:
{
  "controller": "Pi lab1",
  "location": "Room A401",
  "sensor": 2,
  "type": "battery",
  "updateTime": 1454684168,
  "value": 100
}
@apiDescription Gets the battery level of a given sensor, in a JSON format

"""

@app.route('/nodes/<int:node>/get_battery', strict_slashes=False)
def get_battery(node):
    return backend.get_battery(node)



"""
@api {post} /nodes/set_location set_location
@apiName set_location
@apiGroup Nodes

@apiParam {Number} node_id Sensor's unique ID
@apiParam {String} value new location value

@apiParamExample {json} Request-Exemple :
    {
        'node_id' : '4',
        'value' : 'A401'
    }

@apiSuccess {String} location location's new value

@apiDescription Sets location of a given node

"""

@app.route('/nodes/set_location', methods=['GET','POST'], strict_slashes=False)
def set_node_location():
    if request.method=='POST':
        content = request.get_json()
        if all(item in content.keys() for item in ['node_id','value']):
            node = int(content['node_id'])
            value = content['value']
            return backend.set_node_location(node, value)
        return 'wrong input'
    return 'use POST method'




"""
@api {post} /nodes/set_name set_name
@apiName set_name
@apiGroup Nodes

@apiParam {Number} node_id Sensor's unique ID
@apiParam {String} value new name value

@apiParamExample {json} Request-Exemple :
    {
        'node_id' : '4',
        'value' : 'A401-multisensor'
    }

@apiSuccess {String} name name's new value

@apiDescription Sets name of a given node

"""

@app.route('/nodes/set_name', methods=['GET','POST'], strict_slashes=False)
def set_node_name():
    if request.method=='POST':
        content = request.get_json()
        if all(item in content.keys() for item in ['node_id','value']):
            node = int(content['node_id'])
            value = content['value']
            return backend.set_node_name(node, value)
        return 'wrong input'
    return 'use POST method'



"""
@api {get} /nodes/<node_id>/get_location get_location
@apiName get_location
@apiGroup Nodes

@apiParam {Number} node_id Sensor's unique ID

@apiSuccess {String} location location's value

@apiDescription Gets location of a given node

"""

@app.route('/nodes/<int:node>/get_location', strict_slashes=False)
def get_node_location(node):
    return backend.get_node_location(node)



"""
@api {get} /nodes/<node_id>/get_name get_name
@apiName get_name
@apiGroup Nodes

@apiParam {Number} node_id Sensor's unique ID

@apiSuccess {String} name name's value

@apiDescription Gets name of a given node

"""

@app.route('/nodes/<int:node>/get_name', strict_slashes=False)
def get_node_name(node):
    return backend.get_node_name(node)



"""
@api {get} /nodes/<node_id>/get_neighbours get_neighbours
@apiName get_neighbours
@apiGroup Nodes

@apiParam {Number} node_id Sensor's unique ID

@apiSuccess {String[]} neighbors list of a node's neighbours

@apiDescription Gets list of a node's neighbours

"""

@app.route('/nodes/<int:node>/get_neighbours', strict_slashes=False)
def get_neighbours_list(node):
    return backend.get_neighbours_list(node)







#######################################################################################################################
############# SENSORS #################################################################################################
#######################################################################################################################
### THESE METHODS WERE SPECIALLY MADE FOR SENSOR NODES ################################################################
#######################################################################################################################
"""
@api {get} /sensors/get_sensors_list get_sensors_list
@apiName get_sensors_list
@apiGroup Sensors

@apiSuccess {String[]} JSON List of all sensor nodes in the network i a JSON format

@apiDescription Lists all sensors nodes in the network. The controller is excluded.

"""

@app.route('/sensors/get_sensors_list', strict_slashes=False)
def get_sensors_list():
    # returns a list of all sensors in the network in a JSON format(only sensors)
    return backend.get_sensors_list()





"""
@api {get} /sensors/<node_id>/get_all_measures get_all_measures_sensor
@apiName get_all_measures_sensor
@apiGroup Sensors

@apiParam {Number} node_id Sensor's unique ID

@apiSuccess {String} controller Controller name
@apiSuccess {String} location Location of the sensor
@apiSuccess {String} sensor Sensor's ID
@apiSuccess {Number} battery battery level (%)
@apiSuccess {Number} humidity humidity level (%)
@apiSuccess {Number} luminance luminance level (lux)
@apiSuccess {Number} temperature temperature level (C)
@apiSuccess {String} motion motion state (true or false)
@apiSuccess {Number} updateTime Timestamp at the measures' reception

@apiSuccessExample {json} Example of result in case of success:
{
  "battery": 100,
  "controller": "Pi lab1",
  "humidity": 22,
  "location": "Room A401",
  "luminance": 60,
  "motion": false,
  "sensor": 2,
  "temperature": 30.0,
  "updateTime": 1454682568
}
@apiDescription Gets all measures of a given sensor, in a JSON format

"""

@app.route('/sensors/<int:node>/get_all_measures', strict_slashes=False)
def get_all_measures(node):
    return backend.get_all_Measures(node)



"""
@api {get} /sensors/<node_id>/get_temperature get_temperature
@apiName get_temperature
@apiGroup Sensors

@apiParam {Number} node_id Sensor's unique ID

@apiSuccess {String} controller Controller name
@apiSuccess {String} location Location of the sensor
@apiSuccess {String} sensor Sensor's ID
@apiSuccess {String} type Type of measurement
@apiSuccess {Number} value Temperature level (C)
@apiSuccess {Number} updateTime Timestamp of the measure

@apiSuccessExample {json} Example of result in case of success:
{
  "controller": "Pi lab1",
  "location": "Room A401",
  "sensor": 2,
  "type": "temperature",
  "updateTime": 1454682568,
  "value": 30.4
}
@apiDescription Gets temperature of a given sensor in a JSON format

"""

@app.route('/sensors/<int:node>/get_temperature', strict_slashes=False)
def get_temperature(node):
    return backend.get_temperature(node)



"""
@api {get} /sensors/<node_id>/get_humidity get_humidity
@apiName get_humidity
@apiGroup Sensors

@apiParam {Number} node_id Sensor's unique ID

@apiSuccess {String} controller Controller name
@apiSuccess {String} location Location of the sensor
@apiSuccess {String} sensor Sensor's ID
@apiSuccess {String} type type of measurement
@apiSuccess {Number} value humidity level (%)
@apiSuccess {Number} updateTime Timestamp at the measures' reception

@apiSuccessExample {json} Example of result in case of success:
{
  "controller": "Pi lab1",
  "location": "Room A401",
  "sensor": 2,
  "type": "relative humidity",
  "updateTime": 1454682996,
  "value": 21
}
@apiDescription Gets humidity of a given sensor in a JSON format

"""

@app.route('/sensors/<int:node>/get_humidity', strict_slashes=False)
def get_humidity(node):
    return backend.get_humidity(node)



"""
@api {get} /sensors/<node_id>/get_luminance get_luminance
@apiName get_luminance
@apiGroup Sensors

@apiParam {Number} node_id Sensor's unique ID

@apiSuccess {String} controller Controller name
@apiSuccess {String} location Location of the sensor
@apiSuccess {String} sensor Sensor's ID
@apiSuccess {String} type type of measurement
@apiSuccess {Number} value luminance level (lux)
@apiSuccess {Number} updateTime Timestamp at the measures' reception

@apiSuccessExample {json} Example of result in case of success:
{
  "controller": "Pi lab1",
  "location": "Room A401",
  "sensor": 2,
  "type": "luminance",
  "updateTime": 1454682996,
  "value": 49
}
@apiDescription Gets humidity of a given sensor in a JSON format

"""

@app.route('/sensors/<int:node>/get_luminance', strict_slashes=False)
def get_luminance(node):
    return backend.get_luminance(node)



"""
@api {get} /sensors/<node_id>/get_motion get_motion
@apiName get_motion
@apiGroup Sensors

@apiParam {Number} node_id Sensor's unique ID

@apiSuccess {String} controller Controller name
@apiSuccess {String} location Location of the sensor
@apiSuccess {String} sensor Sensor's ID
@apiSuccess {String} type type of measurement
@apiSuccess {Number} value motion state (boolean)
@apiSuccess {Number} updateTime Timestamp at the measures' reception

@apiSuccessExample {json} Example of result in case of success:
{
  "controller": "Pi lab1",
  "location": "Room A401",
  "sensor": 2,
  "type": "sensor",
  "updateTime": 1454682996,
  "value": true
}
@apiDescription Gets motion of a given sensor in a JSON format

"""

@app.route('/sensors/<int:node>/get_motion', strict_slashes=False)
def get_motion(node):
    return backend.get_motion(node)










#############################################################################################
############## DIMMERS ################################### ##################################
#############################################################################################
### THESE METHODS WERE SPECIALLY MADE FOR DIMMER NODES ######################################
#############################################################################################

"""
@api {get} /dimmers/get_dimmers_list get_dimmers_list
@apiName get_dimmers_list
@apiGroup Actuators

@apiSuccess {String[]} JSON List of all dimmer nodes in the network i a JSON format

@apiDescription Lists all dimmer nodes in the network. The controller is excluded.

"""

@app.route('/dimmers/get_dimmers_list', strict_slashes=False)
def get_dimmers():
    return backend.get_dimmers()


"""
@api {get} /dimmers/<node_id>/get_level get_dimmer_level
@apiName get_dimmer_level
@apiGroup Actuators

@apiParam {Number} node_id Dimmer's unique ID

@apiSuccess {String} controller Controller name
@apiSuccess {String} location Location of the sensor
@apiSuccess {String} dimmer Dimmer's ID
@apiSuccess {String} type type of measurement
@apiSuccess {Number} value dimmer level
@apiSuccess {Number} updateTime Timestamp at the measures' reception

@apiSuccessExample {json} Example of result in case of success:
{
  "controller": "Pi lab1",
  "location": "Room A401",
  "dimmer": 4,
  "type": "Level",
  "updateTime": 1454682996,
  "value": 50
}
@apiDescription Gets level of a given dimmer in a JSON format


"""

@app.route('/dimmers/<int:node_id>/get_level', strict_slashes=False)
def get_dimmer_level(node_id):
    return backend.get_dimmer_level(node_id)




"""
@api {post} /dimmers/set_level get_dimmer_level
@apiName get_dimmer_level
@apiGroup Actuators

@apiParam {Number} node_id Dimmer's unique ID
@apiParam {Number} value level value ( 0<value<99 )

@apiParamExample {json} Request-Exemple :
    {
        'node_id' : '4',
        'value' : '50'
    }

@apiSuccess {String} command dimmer's new level

@apiDescription Sends command to dimmer node

"""

@app.route('/dimmers/set_level', methods=['GET', 'POST'], strict_slashes=False)
def set_dimmer_level():
    if request.method=='POST':
        content = request.get_json()
        if all(item in content.keys() for item in ['node_id','value']):
            node = int(content['node_id'])
            value = int(content['value'])
            if 99 < value :
                value = 99
            elif value < 0:
                value = 0
            backend.set_dimmer_level(node,value)
            return "dimmer %s is set to level %s" % (node,value)
        return 'wrong input'
    return 'use POST method'


#################################################################
#################################################################



from logging import FileHandler, Formatter, DEBUG

if __name__ == '__main__':
    try:
        backend.start()
        file_handler = FileHandler("flask.log")
        file_handler.setLevel(DEBUG)
        file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(file_handler)

        app.run(host='::', debug=True, use_reloader=False)

    except KeyboardInterrupt:
        backend.stop()
