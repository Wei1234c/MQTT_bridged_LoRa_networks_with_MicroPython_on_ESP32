# coding: utf-8

from config_lora import millisecond
from config_mbln import LINK_EXPIRATION_SECONDS
       

class Router:    
    
    def __init__(self):
        self.links = {}
                    

    def update_link(self, gateway_eui, node_eui, rssi):
        if node_eui is not None: 
            self.links[(gateway_eui, node_eui)] = (rssi, millisecond()) 
        
            # receive notice from other gateway, and the node doesn't show on this gateway, probably out of range.
            if gateway_eui != self.eui:
                if is_link_expired(self.eui, node_eui):
                    self.delete_link(self.eui, node_eui)
                    self.notice_link(self.eui, node_eui, to_add = False)
                
            print('******** Links *********\n', self.links)
            print('******* Networks *******\n', self.get_networks())  
            # print(self.get_nearest_gateway_eui('32aea4fffe054928'))
                    
                    
    def delete_link(self, gateway_eui, node_eui, rssi = None):
        if node_eui is not None: 
            self.links.pop((gateway_eui, node_eui), None)
        

    def update_link_from_packet(self, pkt):
        if pkt.pay_load.via is None:  # not relayed. only packet from LoRa node counts.
            kwargs = {'node_eui': pkt.pay_load.frm, 
                      'gateway_eui': pkt.gateway_eui, 
                      'rssi': pkt.rssi}
            self.update_link(**kwargs)
            self.notice_link(**kwargs)
        
        
    def notice_link(self, gateway_eui, node_eui, rssi = None, to_add = True):
        message = {'receiver': 'Hub',
                   'message_type': 'function',
                   'function': 'update_link' if to_add else 'delete_link',
                   'kwargs': {'node_eui': node_eui, 
                              'gateway_eui': gateway_eui, 
                              'rssi': rssi}}
        self.request(message)
        
        
    def is_link_expired(self, gateway_eui, node_eui):
        last_status = self.links.get((gateway_eui, node_eui))
        if last_status:
            rssi, last_seen_time = last_status
            return abs(millisecond() - last_seen_time) > LINK_EXPIRATION_SECONDS * 1000
            
    
    def get_nearest_gateway_eui(self, node_eui):
        # {(gateway_eui, node_eui): (rssi, last_seen_time)}        
        links = [(v[0], k[0]) for k, v in self.links.items() if k[1] == node_eui]        
        if len(links) > 0:
            links = sorted(links, reverse = True)
            return links[0][1]
            
            
    def is_nearest_gateway(self, node_eui): 
        return self.get_nearest_gateway_eui(node_eui) == self.eui
            

    def get_networks(self):
        networks = {}
        
        # {(gateway_eui, node_eui): (rssi, last_seen_time)}
        for k, v in self.links.items(): 
            networks.setdefault(k[0], []).append((k[1], v[0])) 
            
        return networks 
        

    def get_network(self, gateway_eui):
        return self.get_networks().get(gateway_eui)
        

    def is_a_gateway(self, eui):
        return eui in self.get_networks().keys()