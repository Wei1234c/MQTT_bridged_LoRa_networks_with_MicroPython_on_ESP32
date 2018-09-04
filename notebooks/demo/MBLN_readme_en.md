# MQTT bridged LoRa networks - using MicroPython on ESP32

![MESH](https://1.bp.blogspot.com/-B-oEkVQMDWs/WjM3zK0zHDI/AAAAAAACV-U/MoXfIGxqBwYlW7HbTdqLJhaNJP4dYhlPwCLcBGAs/s400/mesh.png)  

Wei Lin  

## [Motivations]

   I did an experiment with [MQTT](https://github.com/Wei1234c/Elastic_Network_of_Things_with_MQTT_and_MicroPython) a while ago and recently started playing with [LoRa](https://forum.micropython.org/viewtopic.php?f=16&t=3871). It came to me that I might combine these two technologies - **using MQTT to connect and integrate distributed LoRa networks in a [Cellular Network](https://en.wikipedia.org/wiki/Cellular_network) fashion.**

  With constrains I could spend only a weekend in this POC(Proof Of Concept) experiment, which has not been stress-tested. Besides, I have only four LoRa transceivers at hand, therefor two sets of gateway + nodes at most.

  Not following the specifications of [LoRaWAN](https://www.thethingsnetwork.org/docs/lorawan/), just a personal POC experiment.


## [Advantages of LoRa]  

  [LoRa](https://en.wikipedia.org/wiki/LoRa) has been very popular recently, because its properties of long-range, low energy consumption and low cost:  
- Long range: 
  - only a few gateways are needed to cover a large geographical area.
- Low energy consumption: 
  - Sensitivity can be -148dbm, it means that signal can be transmitted over longer distances with low energy consumption.
- Low cost:
  - The cost of a end node is low: the transceiver of a single channel is not expensive.  

Therefor, LoRa is very suitable for a wide-area multiple-points scenario. I personally am more interested in constructing a M2M (machine to machine) event system. With properties mentioned above, LoRa seems a promising building-brick.  


## [Disadvantages of LoRa]  

  However, if you want to deploy a LoRa network in a city, you will encounter some difficulties, such as:
- LOS(Line of Sight) is rare: 
  - There are many buildings in a city, LOS is rare, which is cruical for transmitting range and speed.
  - There are high-points, roofs for example, which however may be restricted from access and also expensive.
- The gateway devices are not very cheap:
  - The LoRa gateway devices in the market are usually capable of transmitting and receiving multiple channels at the same time, and the price ranges from USD 60 to USD 300+.
- The data-throughput is not high, because of:
  - Obstacles: in a city signal is often affected by obstacles and interference, so the transmission rate is limited.
  - Signal collision:
    - The larger the coverage, the more nodes there are, the higher the probability of signal collision, and the overall data transmission-rate is more likely to be limited.
- Scale of network is limited:
    - In case of downlink(gateway to nodes), the messages are delivered to all nodes parallelly. However, if the more uplink (nodes to gateway) is needed, the higher the probability of signal collision, hence limits the the number of nodes.
- Rang is limited in need of speed:
  - Transmitting Speed/Range trade-off: accroding to [LoRa Link-budget](http://www.techplayon.com/lora-link-budget-sensitivity-calculations-example-explained/), the longer the transmitting range, the lower the data-rate, hence the range of LoRa network is limited in need of speed.


## [idea]  

    Therefor, the idea is:  

- Adopt [Cellular Network](https://en.wikipedia.org/wiki/Cellular_network) model:
![Cellular Network](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Frequency_reuse.svg/400px-Frequency_reuse.svg.png)  

  - There are many buildings and obstacles in a city. The line of sight is rare and therefor higher transmitting power is needed to maintined coverage, hence more power-consumption. 
  - On the other hand, the larger the covered range, the more nodes are covered, and hence the more signal collisions, the lower the overall performance.
  - It may be better to adopt the [Cellular Network](https://en.wikipedia.org/wiki/Cellular_network) model, use more small gateway devices, each gateway covers a small area with fewer nodes, hence the probability of signal collision is lower and the data-rate should be improved.
  - Although the coverage of each gateway is not large, but with more gateway devices, the overall coverage is enlarged, meanwhile it is also easier to circumvant buildings and obstacles, making it more suitable for deployment in a city.
- Using [MQTT](http://mqtt.org/) as backbone:
  - [MQTT](http://mqtt.org/) adopts the publish/subscribe model, it can convey messages in a broadcasting or end-to-end manner. It is quite flexible and efficient, and can be used as a backbone for trasmitting data between gateways.
  - A LoRa gateway is also an MQTT client that can send and receive MQTT messages.
- Gateway as woker:
  - From [Celery](http://www.celeryproject.org/)'s point of view, a gateway is also a ***worker***, and we can communicate messages to each gateways via MQTT, commanding them to do specific work. Each gateway can also communicate and cooperate with each other through this mechanism.


## [Design and Features]
  
- Addressing:
  - Each LoRa node or gateway has an EUI-64 address.
- Communicate via. MQTT:
  - A "LoRa gateway" is an ESP32, it is also a MQTT client and a worker (like a [Celery worker](http://docs.celeryproject.org/en/latest/userguide/workers.html)).
  - Gateways communicate via. MQTT protocol, and can be integrated with existing MQTT-based system easily.
  - Via MQTT, gateways can do RPC (Remote-Procedure-Call) to communicate and cooperate with each others.
- Symmetrical architecture, no central controller:
  - Gateways will share and exchange information with each other, there is no central controller.
- Routing table is automatically generated and updated:
  - Each time a LoRa node transmits signal, the node is automatically clustered to the closest gateway according to the signal strength. The gateway is responsible for responding to the ACK or sending and receiving other LoRa packets. 
  - The topogical information is exchanged between gateways whenever a LoRa node sends packages, hence LoRa nodes can roam between gateways.
  - The topogical information among gateways contains RSSI data, which can be used for geolocation.
- Two modes of package routing:
  - With a destinated EUI address:
    - When a LoRa node sends a package, if it contains an EUI indicating the destination, it will be routed to the closest gateway via MQTT and then broadcast to the destinated LoRa node.
    - **A LoRa node can "dial" and pass data to a specific remote LoRa node**. As long as the EUI address of the other party is specified, the payload will be automatically routed by the gateways to reduce interrupting unrelated LoRa nodes in other areas.
  - Without a destinated EUI address:
    - If a destinated EUI address is not indicated in the package, the package is transmitted to each gateway via MQTT, and then the LoRa signal is broadcasted to LoRa nodes in each network. 
    - The effect is equivalent to a global broadcast. Therefore, **all LoRa networks in, for example, Taipei and New York city can be bridged and seemed as a single LoRa network**.    
- Low cost and more affordable:
    - With ESP32 the cost is lower. The cheaper each gateway is, the more volunteers can afford it.
  - Gateway used (ESP32 + RFM96W)  
  
    ![](https://3.bp.blogspot.com/-ull0K2sMp0M/WY8ep6nwB9I/AAAAAAACN6w/WmM1GYxTUfEYInGtMBWbkGbVtScAiUZDQCPcBGAYYCw/s640/IMG_20170812_225846.jpg)  
    
    - There are also integrated ESP32+SX1278_LoRa+SSD1306_OLED modules. The cost can be as low as USD 11.  
    
      ![](https://4.bp.blogspot.com/-aqrlAOG8_yY/Wc75_f86UuI/AAAAAAACQHk/JlNcYTv2CIslMAWbtp6cgxIDqe_NgTiFgCKgBGAs/s640/IMG_20170930_085659.jpg)

- Easy to deploy:
  - Minimum setup. Just connect a gateway to WiFi network, it will service those LoRa nodes within a few hundred meters.
- Enhanced through-put:
  - Reduce the chance of collision
    - Packages may be routed based on the destinatd EUI address, it is possible to avoid global broadcasts, and hence minimum collision.
- Bidirectional data exchange between MQTT and LoRa:
  - An MQTT message from external can be sent to a gateway, commanding it to send a LoRa package and wire the data to a specific node.
  - The data transmitted by LoRa nodes can be collected by the MQTT mechanism easily.


## [Test and Results]  

Experimental model description:  

For an ESP32 to function as a gateway to bridge LoRa networks, it needs three parts of code (in the order of uploading to ESP32):

1. [MQTT client as a worker - so ESP32 can communicate and cooperate with each others](https://github.com/Wei1234c/Elastic_Network_of_Things_with_MQTT_and_MicroPython)
2. [SX127x driver - for ESP32 to drive SX127x](https://forum.micropython.org/viewtopic.php?f=16&t=3871)
3. [LoRa gateway - for ESP32 to bridge LoRa networks](https://github.com/Wei1234c/MQTT_bridged_LoRa_networks_with_MicroPython_on_ESP32)  

 
[![MBLN](https://raw.githubusercontent.com/Wei1234c/MQTT_bridged_LoRa_networks_with_MicroPython_on_ESP32/master/jpgs/MBLN.jpeg)](https://youtu.be/0rhd3wtU1Ak)  

- From left to right are node2, gateway2, gateway1, node1
- Use SF (Spreading Factor) isolation: node2, gateway2 SF = 9, node1, gateway1 SF = 8. This simulates two LoRa networks that are quite far apart and could not communicate with each other.
- Node1, node2 randomly send a packet to their respective gateway every 2~4 seconds.
- Node or gateway, on-board LED will flash after receiving a packet.
- Node1 is made of ESP8266, the LED light is on the top, which can be seen more clearly with reflection of the computer screen.
- After receiving a package from node:
  - Internet topology data will be exchanged through MQTT, and routing tables are built among gateways.
  - The ACK is echoed by the closest gateway.
  - The package is routed according to the destinated EUI address.
- The [MQTT message command can be sent from a PC, in order to send a message to a LoRa node with destinated EUI address](https://github.com/Wei1234c/Elastic_Network_of_Things_with_MQTT_and_MicroPython/blob/master/notebooks/demo/MQTT%20bridged%20LoRa%20networks%20-%20demo.ipynb).  


### [Notes]
- Capacity:
  - With only four LoRa transceivers at hand, I didn't do stress test on this device set. The capacity should varies with how many nodes are there and how frequently nodes send packages, ...and so on.