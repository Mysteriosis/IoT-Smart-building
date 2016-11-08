#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Pierre-Alain Curty
# Date: 3 Novembre 2016

import argparse
import sys
import socket
from knxnet import *

class MyKNX():
    ACTION_READ = "READ"
    ACTION_WRITE = "WRITE"
    ACPI = {'READ': 0, 'WRITE': 0x2}

    # CONSTRUCTOR
    def __init__(self, gateway_ip, gateway_port, socket_port, data_endpoint=('0.0.0.0', 0), control_enpoint=('0.0.0.0', 0)):
        self.gateway_ip = None
        self.gateway_port = None
        self.data_endpoint = None
        self.control_enpoint = None
        self.conn_state_resp = None
        self.debug = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.gateway_ip = gateway_ip
        self.gateway_port = gateway_port
        self.data_endpoint = data_endpoint
        self.control_enpoint = control_enpoint
        self.sock.bind(('', socket_port))

    # TOGGLE DEBUG
    def setDebug(self, value):
        if isinstance(value, bool):
            self.debug = value

    # CONNECTION
    def connect(self):
        conn_req_object = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_REQUEST, self.control_enpoint, self.data_endpoint)
        if self.debug:
            print()
            print("Connection Request:")
            print(conn_req_object)
        self.sock.sendto(conn_req_object.frame, (self.gateway_ip, self.gateway_port))

        data_recv, addr = self.sock.recvfrom(1024)
        self.conn_resp = knxnet.decode_frame(data_recv)
        if self.debug:
            print("Connection Response:")
            print(self.conn_resp)

        conn_state_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_STATE_REQUEST, self.conn_resp.channel_id, self.control_enpoint)
        if self.debug:
            print()
            print("Connection State Request:")
            print(conn_state_req)
        self.sock.sendto(conn_state_req.frame, (self.gateway_ip, self.gateway_port))

        data_recv, addr = self.sock.recvfrom(1024)
        conn_state_resp = knxnet.decode_frame(data_recv)
        if self.debug:
            print("Connection State Response:")
            print(conn_state_resp)

        print("Connected to KNX network.")
        print()

    # DISCONNECTION
    def disconnect(self):
        if self.conn_resp:
            disconnect_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.DISCONNECT_REQUEST, self.conn_resp.channel_id, self.control_enpoint)
            if self.debug:
                print()
                print('Disconnect Request:')
                print(disconnect_req)
            self.sock.sendto(disconnect_req.frame, (self.gateway_ip, self.gateway_port))

            data_recv, addr = self.sock.recvfrom(1024)
            disconnect_resp = knxnet.decode_frame(data_recv)
            if self.debug:
                print('Disconnect Response:')
                print(disconnect_resp)

            print("Disconnected from KNX network.")
            print()

        else:
            print('No active connection.')
            print()

    # REQUEST METHOD
    def request(self, action, destination, donnees):
        dest = knxnet.GroupAddress.from_str(destination)
        data = int(donnees)
        data_size = 1 if dest.main_group == 1 else 2

        print("Sending " + action + " request...")
        read_req = knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_REQUEST, dest, self.conn_resp.channel_id, data, data_size, self.ACPI[action])
        if self.debug:
            print()
            print("Client Tunnelling Request:")
            print(read_req)
        self.sock.sendto(read_req.frame, (self.gateway_ip, self.gateway_port))

        data_res, addr = self.sock.recvfrom(1024)
        ack = knxnet.decode_frame(data_res)
        if self.debug:
            print("Server Tunnelling ACK:")
            print(ack)

        data_res, addr = self.sock.recvfrom(1024)
        tunnel_req = knxnet.decode_frame(data_res)
        if self.debug:
            print("Server Tunnelling Request:")
            print(tunnel_req)

        tunnel_ack = knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_ACK, tunnel_req.channel_id, 0, tunnel_req.sequence_counter)
        if self.debug:
            print("Client Tunnelling ACK:")
            print(tunnel_ack)
        self.sock.sendto(tunnel_ack.frame, (self.gateway_ip, self.gateway_port))

        if action == "READ":
            data_res, addr = self.sock.recvfrom(1024)
            answer = knxnet.decode_frame(data_res)
            if self.debug:
                print("Server Tunnelling Request:")
                print(answer)

            print('KNXnet/IP answer: ', answer.data)
            print()

    def run(self):
        while True:
            print("-- KNX Console --")
            print("0. Help")
            print("1. READ Request")
            print("2. WRITE Request")
            print("3. Exit")
            choice = input(">>> ")
            if(choice == "0"):
                print('Main group addr: 0 = valve (read or write)')
                print('                 1 -> blind up or down (write)')
                print('                 3 -> blind position (write)')
                print('                 4 -> blind position (read)')
            elif choice == "1" or choice == "2":
                action = self.ACTION_READ if choice == "1" else self.ACTION_WRITE
                addresse = input("GroupAddress (ex. 4/4/11): ")
                donnees = input("Data [0-255]: ")
                self.connect()
                try:
                    self.request(action, addresse, donnees)
                except utils.KnxnetUtilsException as err:
                    print("BAD ARGUMENT: ", err)
                    print()
                self.disconnect()
            elif choice == "3":
                print("Bye !")
                sys.exit(0)
            else:
                print("Wrong input.")

if __name__ == '__main__':
    #Distant IP: 195.176.0.157
    knx = MyKNX("127.0.0.1", 3671, 3672)
    knx.run()

    """knx.setDebug(True)
    knx.connect()
    knx.request(knx.ACTION_READ, "4/4/11", 0)
    knx.disconnect()"""
