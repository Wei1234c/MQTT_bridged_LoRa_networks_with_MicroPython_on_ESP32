import sx127x
import config_lora 



# import LoRaSender
# import LoRaReceiverCallback
import LoRaDuplexCallback

if config_lora.IS_ESP8266: 
    PIN_ID_SS = 15
    PIN_ID_FOR_LORA_DIO0 = 5
if config_lora.IS_ESP32:
    PIN_ID_SS = 15
    PIN_ID_FOR_LORA_DIO0 = 5
if config_lora.IS_RPi:        
    PIN_ID_SS = 25
    PIN_ID_FOR_LORA_DIO0 = 17
    
 
def main():
    
    controller = config_lora.Controller()
    
    lora = controller.add_transceiver(sx127x.SX127x(name = 'LoRa'),
                                      pin_id_ss = PIN_ID_SS,
                                      pin_id_RxDone = PIN_ID_FOR_LORA_DIO0)
    print('lora', lora)
    
    # LoRaSender.send(lora)
    # LoRaReceiverCallback.receiveCallback(lora)
    LoRaDuplexCallback.duplexCallback(lora)

    
if __name__ == '__main__':
    main()