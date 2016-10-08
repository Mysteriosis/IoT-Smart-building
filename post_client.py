import requests
import json

#############################################################
#### This script sends POST or PUT http request to server ###
#############################################################
#### You have to uncomment the request you want to send   ###
#############################################################
#### POST requests contain parameters in JSON format      ###
#############################################################


 
#### Configuration of nodes
#req = requests.post('http://192.168.1.2:5000/network/set_nodes_basic_configuration',headers={'Content-Type': 'application/json'}, data=json.dumps({'Group_Interval': '240','Group_Reports':'240', 'Wake-up_Interval': '480'}))


#### Config a specific parameter
#req = requests.post('http://192.168.1.2:5000/nodes/set_parameter',headers={'Content-Type': 'application/json'}, data=json.dumps({'node_id': '4','value':'480', 'parameter_index': '111', 'size': '4'}))


#### Set node location
#req = requests.post('http://192.168.1.2:5000/nodes/set_location',headers={'Content-Type': 'application/json'}, data=json.dumps({'node_id': '4','value':'A402'}))


#### Set node name
#req = requests.post('http://192.168.1.2:5000/nodes/set_name',headers={'Content-Type': 'application/json'}, data=json.dumps({'node_id': '4','value':'sensor'}))


#### Send command to switch
#req = requests.post('http://192.168.1.2:5000/switches/send_command',headers={'Content-Type': 'application/json'}, data=json.dumps({'node_id': '3','value':'on'}))

#### Send command to dimmer
req = requests.post('http://192.168.1.2:5000/dimmers/set_level',headers={'Content-Type': 'application/json'}, data=json.dumps({'node_id': '6','value':'120'}))

#### Put controller in inclusion mode
#req = requests.put('http://192.168.1.2:5000/nodes/add_node')


#### Put controller in exclusion mode
#req = requests.put('http://192.168.1.2:5000/nodes/remove_node')


print (req.text)  # print server response
