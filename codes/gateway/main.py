# coding: utf-8
import gc
gc.collect()

import sx127x
gc.collect()

# SF8_NODE_EUI = 'f3d308fffe00'
# SF8_GATEWAY_EUI = '32aea4fffe809528'
# SF9_NODE_EUI = '32aea4fffe054928'
# SF9_GATEWAY_EUI = '260ac4fffe0c1764'

import config_lora
gateways = ['32aea4fffe809528', '260ac4fffe0c1764']
IS_GATEWAY = config_lora.NODE_EUI in gateways 



def run():
    
    if IS_GATEWAY:
        
        import gateway
        
        def setup_wifi(): 
            
            def wait_for_wifi():
                import network

                sta_if = network.WLAN(network.STA_IF)
                if not sta_if.isconnected():
                    print('connecting to network...')
                    sta_if.active(True)        
                    # sta_if.connect(SSID, PASSWORD)
                    sta_if.connect('Lin_841', '51557010') 
                    while not sta_if.isconnected():
                        pass
                print('Network configuration:', sta_if.ifconfig())
                
            wait_for_wifi()

            import led
            led.blink_on_board_led(times = 2)
            

        def start_gateway():
            
            if config_lora.IS_ESP8266: 
                PIN_ID_SS = 15
                PIN_ID_FOR_LORA_DIO0 = 5
            if config_lora.IS_ESP32:
                PIN_ID_SS = 15
                PIN_ID_FOR_LORA_DIO0 = 5
            if config_lora.IS_RPi:        
                PIN_ID_SS = 25
                PIN_ID_FOR_LORA_DIO0 = 17
                
            import node         
            nd = node.Node()
            gateway = nd.worker            
            lora = gateway.add_transceiver(sx127x.SX127x(name = 'LoRa'),
                                           pin_id_ss = PIN_ID_SS,
                                           pin_id_RxDone = PIN_ID_FOR_LORA_DIO0) 
                                              
            lora.onReceive(gateway.received_packet_update_route)
            lora.receive()

            nd.run() 

            
        setup_wifi()
        start_gateway()

    else: 

        import test 
        gc.collect()
        test.main()

run()        