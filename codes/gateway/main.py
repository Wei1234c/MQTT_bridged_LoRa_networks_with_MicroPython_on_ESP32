# coding: utf-8

import gc
gc.collect()

import sx127x
gc.collect()

# NODE1_EUI = 'f3d308fffe00'
# GATEWAY1_EUI = '32aea4fffe809528'
# NODE2_EUI = '32aea4fffe054928'
# GATEWAY2_EUI = '260ac4fffe0c1764'
# NODE3_EUI = '32aea4fffe375168'
# GATEWAY3_EUI = '32aea4fffe3754c4'

import config_lora
gateways = ['32aea4fffe809528', '260ac4fffe0c1764', '32aea4fffe3754c4']
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
            import node
            nd = node.Node()
            gw = nd.worker
            lora = gw.add_transceiver(sx127x.SX127x(name = 'LoRa'),
                                      pin_id_ss = config_lora.Controller.PIN_ID_FOR_LORA_SS,
                                      pin_id_RxDone = config_lora.Controller.PIN_ID_FOR_LORA_DIO0)                                      
            lora.onReceive(gw.received_packet_update_link)
            lora.receive()

            nd.run()

            
        setup_wifi()
        start_gateway()

    else:
        import test 
        gc.collect()
        test.main()

run()        