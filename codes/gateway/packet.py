# coding: utf-8

from config_lora import millisecond 
       

class Packet:    
    
    def __init__(self,
                 gateway_eui = None,
                 rssi = None,
                 pay_load = None,
                 time_stamp = None):
                 
        self.gateway_eui = gateway_eui
        self.rssi = rssi
        self.pay_load = pay_load
         
        self.time = time_stamp if time_stamp else millisecond()
        