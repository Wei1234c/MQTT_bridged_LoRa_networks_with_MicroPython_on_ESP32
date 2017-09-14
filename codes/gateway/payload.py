# coding: utf-8

import json
import time
from config_lora import millisecond
       

class Payload:    
    
    def __init__(self, 
                 frm = None,
                 to = None,
                 message = None,
                 time_stamp = None):
                 
        self.frm = frm   
        self.to = to
        self.message = message
        
        self.time = time_stamp if time_stamp else millisecond()
        
          
    def dumps(self):
        pay_load = {'from': self.frm,
                    'to': self.to,
                    'message': self.message,
                    'time': self.time}
        try:
            return json.dumps(pay_load)
        except Exception as e:
            print(e)
 
 
    def loads(self, payload_string = None):
        if payload_string:
            try: 
                pay_load = json.loads(payload_string) 
                self.frm = pay_load.get('from')
                self.to = pay_load.get('to')
                self.message = pay_load.get('message') 
                self.time = pay_load.get('time') 
                return self
            except Exception as e:
                print(e)
                return Payload(message = payload_string)
                
                
    def gen_ack_payload(self, gateway_eui):
        return Payload(frm = gateway_eui, 
                       to = self.frm,
                       message = {'type': 'ACK', 'time': self.time})
        