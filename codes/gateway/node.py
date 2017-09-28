# coding: utf-8

import config_mqtt
import commander
import gateway as worker_impl
    

class Node(commander.Commander):
    
    def __init__(self):
        super().__init__()
        self.worker = worker_impl.Worker(config_mqtt.BROKER_HOST, config_mqtt.HUB_PORT)
        self.worker.set_parent(self)

        
    def run(self):
        self.worker.run()
        
        
    def stop(self):
        self.worker.stop()
        self.worker.set_parent(None)

        
    def request(self, **message):
        return self.worker.request(message)


def main():
    try:
        node = Node()
        node.run()

    except KeyboardInterrupt:
        print("Ctrl C - Stopping.")
        node.stop()
        node = None
        sys.exit(1)


if __name__ == '__main__':
    main()
