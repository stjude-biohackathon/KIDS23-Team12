# Imports
import zmq
import pickle
import numpy as np
import threading
import json
from json import JSONEncoder

class Napari_Jupyter_coms():
    def __init__(self):
        super().__init__()
        # Initailizing with local host address - as default - Can be overwritten with getters and setters
        self.Receive_address="tcp://127.0.0.1:5001"
        self.Send_address="tcp://127.0.0.1:5002"
        self.sendsocket=None
        self.sendcontext=None
        self.receivesocket=None
        self.receivecontext=None
    
    def set_receive_address(self,address):
        self.Receive_address="tcp://"+address
        
    def set_send_address(self,address):
        self.Send_address="tcp://"+address
        
    def get_send_address(self):
        return self.Send_address
    
    def get_receive_address(self):
        return self.Receive_address
        
    def establish_sending_socket_connection(self):
        try:
            self.sendcontext = zmq.Context()
            #self.sendsocket = self.sendcontext.socket(zmq.PUB)
            self.sendsocket = self.sendcontext.socket(zmq.PUSH)
            self.sendsocket.bind(self.Send_address)
            print("Send : connection established at",self.Send_address)
        except Exception as e:
            print("...Connection Failed ! - Send ",self.Send_address)
            print(e)
            
    def terminate_sending_socket_connection(self):
        try:
            self.sendsocket.close()
            self.sendcontext.term()
            print("Send Connection Closed Successfully ",self.Send_address)
        except Exception as e:
            print("Unable to disconnect")
            print(e)
            
    def send_data(self,message,data=None,operator=None):
        new_dict={}
        new_dict["message"]=message
        if data is not None:
            data_list_version=data.tolist()
            #data_list_version = pickle.dumps(data)
            new_dict["data"]=data_list_version
        if operator is not None:
            new_dict["operator"]=operator
        # Convert to Json
        serialized_info = json.dumps(new_dict)
        try:
            # Send through socket
            self.sendsocket.send_string(serialized_info)
            print("Send Successful")
        except Exception as e:
            print("Unable to Send")
            print(e)
            
            
    def establish_receiving_socket_connection(self):
        try:
            self.receivecontext = zmq.Context()
            #self.receivesocket = self.receivecontext.socket(zmq.SUB)
            self.receivesocket = self.receivecontext.socket(zmq.PULL)
            self.receivesocket.connect(self.Receive_address)
            #self.receivesocket.setsockopt_string(zmq.SUBSCRIBE, "")
            print("Receive : connection established at",self.Receive_address)
        except Exception as e:
            print("...Connection Failed ! - Receive ",self.Receive_address)
            print(e)
            
    def terminate_receiving_socket_connection(self):
        try:
            self.receivesocket.close()
            self.receivecontext.term()
            print("Receive Connection Closed Successfully ",self.Receive_address)
        except Exception as e:
            print("Unable to disconnect")
            print(e)
            
    def receive_data(self):
        try:
            print("Receiving")
            serialized_info = self.receivesocket.recv_string() 
            new_dict = json.loads(serialized_info) 
            print("Received !")
            return new_dict
        except Exception as e:
            print("Unable to Receive")
            print(e)
            
    def terminate_all_connections(self):
        self.terminate_sending_socket_connection()
        self.terminate_receiving_socket_connection()
        