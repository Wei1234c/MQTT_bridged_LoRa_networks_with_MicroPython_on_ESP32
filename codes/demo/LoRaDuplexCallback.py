import time
import config_lora
import payload

msgCount = 0            # count of outgoing messages
INTERVAL = 10000         # interval between sends
INTERVAL_BASE = 10000    # interval between sends base
 

def duplexCallback(lora):    
    print("LoRa Duplex with callback")    
    lora.onReceive(on_receive)  # register the receive callback
    do_loop(lora)


def do_loop(lora):    
    global msgCount
    
    lastSendTime = 0
    interval = 0
    
    while True:
        now = config_lora.millisecond()
        if now < lastSendTime: lastSendTime = now 
        
        if (now - lastSendTime > interval):
            lastSendTime = now                                      # timestamp the message
            interval = (lastSendTime % INTERVAL) + INTERVAL_BASE    # 2-3 seconds
            
            message = "{} {}".format(config_lora.NODE_NAME, msgCount)
            pl = payload.Payload(frm = config_lora.NODE_EUI, 
                                 to = None,
                                 message = message)
            sendMessage(lora, pl.dumps())                     # send message
            msgCount += 1 

            lora.receive()                                          # go into receive mode
    

def sendMessage(lora, outgoing):
    lora.println(outgoing)
    # print("Sending message:\n{}\n".format(outgoing))

    
def on_receive(lora, payload_bytes):
    lora.blink_led()   

    try:
        payload_string = payload_bytes.decode()
        rssi = lora.packetRssi()
        print("*** Received message ***\n{}".format(payload_string))
        if config_lora.IS_TTGO_LORA_OLED: lora.show_packet(payload_string, rssi)
    except Exception as e:
        print(e)
    print("with RSSI {}\n".format(rssi))    