from typing import TYPE_CHECKING

from magicgui import magic_factory
from qtpy.QtWidgets import QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLineEdit, QComboBox,QLabel
from qtpy.QtCore import QThread, Signal
from qtpy import uic
import os
from Napari_Jupyter import Napari_Jupyter_coms
from Napari_ChatGPT import Napari_ChatGPT_coms
import matplotlib.pyplot as plt
import numpy as np
import imageio.v2 as imageio
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

if TYPE_CHECKING:
    import napari
     
class Trio(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        
        script_dir = os.path.dirname(__file__) 
        rel_path = "trio.ui"
        abs_file_path = os.path.join(script_dir, rel_path)
        uic.loadUi(abs_file_path,self)
        
        #Get Address
        self.jsend_lineedt = self.findChild(QLineEdit,"Jupyter_send_lineedt")
        self.jrec_lineedt = self.findChild(QLineEdit,"Jupyter_receive_lineedt")
        self.csend_lineedt = self.findChild(QLineEdit,"send_chatGPT")
        self.crec_lineedt = self.findChild(QLineEdit,"receive_chatGPT")
        
        
        # Get Buttons
        self.send_data = self.findChild(QPushButton,"Send_data_btn")
        self.rec_data = self.findChild(QPushButton,"Receive_data_btn")
        self.create_process = self.findChild(QPushButton,"create_process")
        
        # Hook buttont to events
        self.create_process.clicked.connect(self.add_widget)
        self.send_data.clicked.connect(self.execute_current_process)
        self.rec_data.clicked.connect(self.data_from_current_process)
        
        
        #Get label
        self.status_label=self.findChild(QLabel,"status_label")
        
        #Process_space
        self.process_space_layout=self.findChild(QVBoxLayout,"Process_space")
        self.process_space_layout.setSpacing(10)
        
        self.line_edits = []
        self.dropdowns = []    
        self.dropdowns_layers = []     
        self.current_process_index=0
        
        self.njc=None
        self.ncc=None
        self.connector=None
        
        
    def add_widget(self):
        line_edit = QLineEdit()
        dropdown = QComboBox()
        dropdown.addItems(['JupyterHub', 'ChatGPT'])
        self.line_edits.append(line_edit)
        self.dropdowns.append(dropdown)
        hbox = QHBoxLayout()
        hbox.addWidget(line_edit)
        hbox.addWidget(dropdown)
        self.process_space_layout.addLayout(hbox)
    
    def set_up_connection(self):
        Receive_data_from_jupyter=str(self.jrec_lineedt.text())
        Send_data_to_jupyter=str(self.jsend_lineedt.text())
        Receive_data_from_chatgpt=str(self.crec_lineedt.text())
        Send_data_to_chatgpt=str(self.csend_lineedt.text())
        
        self.njc=Napari_Jupyter_coms()
        self.njc.set_receive_address(Receive_data_from_jupyter)
        self.njc.set_send_address(Send_data_to_jupyter)
        
        self.ncc=Napari_ChatGPT_coms()
        self.ncc.set_receive_address(Receive_data_from_chatgpt)
        self.ncc.set_send_address(Send_data_to_chatgpt)
        
        # Establishing Coms
        self.njc.establish_sending_socket_connection()
        self.njc.establish_receiving_socket_connection()
        # Establishing Coms
        self.ncc.establish_sending_socket_connection()
        self.ncc.establish_receiving_socket_connection()
    
        
    def execute_current_process(self):
        if self.current_process_index==0:
            self.set_up_connection()
            
        #message
        message="Napari data from process number "+str(self.current_process_index)
        #operator
        operator_name=str(self.line_edits[self.current_process_index].text())
        #Data
        I=self.viewer.layers[0].data
        print(I.shape)
        
        this_dropdown=self.dropdowns[self.current_process_index]
        #choose connection
        if this_dropdown.currentText()=="JupyterHub":
            self.connector=self.njc
            print("Choosen Jupyter hub")
        else:
            self.connector=self.ncc
            print("Choosen chatGPT")
            
        
        # Perform send
        self.connector.send_data(message,data=I,operator=operator_name)
        self.status_label.setText("Data Sent to process .. Use jupyterhub or chatgpt_jupyterhub to process next steps")
        self.current_process_index+=1
            
    def data_from_current_process(self):
        Data=self.connector.receive_data()
        self.status_label.setText("Data Received and added to napari.. Process Completed")
        print(Data["message"])
        image=np.array(Data["data"])
        self.viewer.add_image(image)