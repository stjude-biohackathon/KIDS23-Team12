"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from magicgui import magic_factory
from qtpy.QtWidgets import QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLineEdit, QComboBox
import zmq
import pickle
from PIL import Image
import openai
import re
import threading

if TYPE_CHECKING:
    import napari


class Simple_Send_Receive(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        send_btn = QPushButton("Send data to Jupyter hub")
        send_btn.clicked.connect(self._send)
        
        rec_btn = QPushButton("Receive data from Jupyter hub")
        rec_btn.clicked.connect(self._receive)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(send_btn)
        self.layout().addWidget(rec_btn)
        
        self.send_add_line_edt=QLineEdit()
        self.rec_add_line_edt=QLineEdit()
        
        self.layout().addWidget(self.send_add_line_edt)
        self.layout().addWidget(self.rec_add_line_edt)
        
        
        self.send_add="tcp://127.0.0.1:5001"
        self.rec_add="tcp://127.0.0.1:5002"
        
        
        
        self.rec_socket,self.rec_context=self.init_rec_port_2()
    
        self.t1=threading.Thread(target=self.receive_continuously)
        
        self.image_sent_ack=0
        self.image_sent_ack_received=0
        self.t1.start()
        
    def receive_continuously(self):
        flag=True
        while flag:
            flag=self.receive_from_jupyter()
    
    def receive_from_jupyter(self):
        message = self.rec_socket.recv_string()
        if message=="Image Received":
            self.image_sent_ack+=1
            
    def is_image_sent(self):
        if self.image_sent_ack>self.image_sent_ack_received:
            image_sent_ack_received+=1
            return True
        return False
            

    def init_send_port(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        self.send_add=  "tcp://"+self.send_add_line_edt.text()
        socket.bind(self.send_add)
        return socket,context
        
    def init_rec_port(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        self.rec_add= "tcp://"+self.rec_add_line_edt.text()
        socket.connect(self.rec_add)
        socket.setsockopt_string(zmq.SUBSCRIBE, "")
        return socket,context
    
    def init_rec_port_2(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        #self.rec_add= "tcp://"+self.rec_add_line_edt.text()
        socket.connect(self.rec_add)
        socket.setsockopt_string(zmq.SUBSCRIBE, "")
        return socket,context

    def _send(self):
        print("Sending the last layer")
        socket,context=self.init_send_port()
        image = self.viewer.layers[0].data
        print(image.shape)
        serialized_image = pickle.dumps(image)
        # Try 10 times to send - if success then break
        for i in range(10):
            socket.send(serialized_image)
            print(i)
            if self.is_image_sent:
                break
                
        print("Sent")
        socket.close()
        context.term()
        
    def _receive(self):
        print("Receiving from Jupyter hub")
        socket,context=self.init_rec_port()
        serialized_image = socket.recv()  
        image = pickle.loads(serialized_image) 
        print(image.shape)
        self.viewer.add_image(image)
        socket.close()
        context.term()

        
class Full_Flow_Design(QWidget):
    def __init__(self):
        super().__init__()
        self.layout_main=QVBoxLayout()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout_bottom = QVBoxLayout()
        
        self.layout_main.addLayout(self.layout_bottom)
        self.layout_main.addLayout(self.layout)
         
        self.setLayout(self.layout_main)
        self.line_edits = []
        self.dropdowns = []
        self.add_widget_btn = QPushButton('Add New Process')
        self.add_widget_btn.clicked.connect(self.add_widget)
        self.layout_bottom.addWidget(self.add_widget_btn)
        
        self.execute_current_process_btn = QPushButton('Execute Current process')
        self.execute_current_process_btn.clicked.connect(self.execute_current_process)
        self.layout_bottom.addWidget(self.execute_current_process_btn)
        
        self.current_process_index=0
        openai.api_key = "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"
        
    def add_widget(self):
        line_edit = QLineEdit()
        dropdown = QComboBox()
        dropdown.addItems(['JupyterHub', 'ChatGPT', 'Build_Widget_for_this'])
        self.line_edits.append(line_edit)
        self.dropdowns.append(dropdown)
        hbox = QHBoxLayout()
        hbox.addWidget(line_edit)
        hbox.addWidget(dropdown)
        self.layout.addLayout(hbox)
        
    def generate_code_block(self, line_edit):
        input_text = line_edit.text()
        prompt = f"```write a python function to take numpy array as input and perform {input_text} on the array and return numpy array as  output of the function```"  # Wrap input text in code block
        completion = openai.ChatCompletion()
        # Use ChatGPT to generate code completion for the input text
        chat_log=[
            {"role": "system", "content": prompt}
        ]
        
        response = completion.create(model='gpt-3.5-turbo', messages=chat_log)
        code_block = response.choices[0]['message']['content']
        print(code_block)
        
        # Replace the original input text with the generated code block
        code_block = re.sub(r"^(.*)$", r"    \1", code_block, flags=re.MULTILINE)  # Indent code block
        #line_edit.setText(code_block)
        print(code_block)
        return code_block
        
    
    def execute_current_process(self):
        code_to_execute=self.generate_code_block(self.line_edits[self.current_process_index])
        self.current_process_index+=1
        print("Executed this process !!")