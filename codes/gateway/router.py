# coding: utf-8
       

class Router:    
    
    def __init__(self):
        self.routing_table = {}
        # self.routing_table = {self.eui: {self.eui: 0}}
    

    def update_route_from_packet(self, pkt, clear_first = True):
        kwargs = {'node_eui': pkt.pay_load.frm, 
                  'gateway_eui': pkt.gateway_eui, 
                  'rssi': pkt.rssi, 
                  'clear_first': clear_first}
        self.update_route(**kwargs)
                    

    def update_route(self, node_eui, gateway_eui, rssi, clear_first = False):
        if node_eui is not None:
            if clear_first: self.routing_table[node_eui] = {}
            routes = self.routing_table.get(node_eui, {})
            routes[gateway_eui] = rssi
            self.routing_table[node_eui] = routes
            
        print('**** Routing Table *****\n', self.routing_table)
        print('******* Networks *******\n', self.get_networks())  
                    
                    
    def notice_route_from_packet(self, pkt, clear_first = False):
        kwargs = {'node_eui': pkt.pay_load.frm, 
                  'gateway_eui': pkt.gateway_eui, 
                  'rssi': pkt.rssi, 
                  'clear_first': clear_first}
        self.notice_route(**kwargs)
        
        
    def notice_route(self, node_eui, gateway_eui, rssi, clear_first = False):
        message = {'receiver': 'Hub',
                   'message_type': 'function',
                   'function': 'update_route',
                   'kwargs': {'node_eui': node_eui, 
                              'gateway_eui': gateway_eui, 
                              'rssi': rssi, 
                              'clear_first': clear_first}}
        self.request(message)
        

    def get_nearest_gateway_eui(self, node_eui):         
        routes = self.routing_table.get(node_eui, {})
        routes = [(v, k) for k, v in routes.items()]
        routes = sorted(routes, reverse = True)
        if len(routes) > 0:
            return routes[0][1]
            
            
    def is_nearest_gateway(self, node_eui): 
        return self.get_nearest_gateway_eui(node_eui) == self.eui
            

    def get_networks(self):
        networks = {}
        for node_eui, gateways_rssi in self.routing_table.items():
            for gateway_eui, rssi in gateways_rssi.items():
                network = networks.get(gateway_eui, [])
                network.append((node_eui, rssi))
                networks[gateway_eui] = network
            
        return networks 
        

    def get_network(self, gateway_eui):
        networks = self.get_networks()
        return networks.get(gateway_eui)