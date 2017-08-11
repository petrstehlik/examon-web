"""
MQTT protocol holder

Subscribe to given topics and hold the last message.
Each value is computed as a moving average of values.
"""

import paho.mqtt.client as mqtt
import logging
import json

class Holder():

    # Callback function on what to do with the message before storing it in database
    on_receive = None

    # Callback function on what to do after storing the value in database
    on_store = None
    # Database dictionary
    # Records are organized by the metric (last value topic) and node ID
    db = dict()

    nodes = list()

    def __init__(self,
            mqtt_broker,
            mqtt_port = 1883,
            mqtt_topics = ["#"],
            alfa = 0.75):
        self.log = logging.getLogger(__name__)

        self.log.debug("Initializing MQTT Holder")

        self.broker = mqtt_broker
        self.port = mqtt_port
        self.topics = [(str(topic),0) for topic in mqtt_topics]
        self.log.debug(self.topics)

        self.db = dict()
        self.alfa = alfa

        self.client = mqtt.Client()

        # Register methods for connection and message receiving
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.on_store = self.default_on_store
        self.on_receive = self.default_on_receive

        self.client.connect(mqtt_broker, self.port, 60)

        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        """
        Subscribe to all topics
        """
        result, mid = client.subscribe(self.topics)

        if result == mqtt.MQTT_ERR_SUCCESS:
            self.log.info("Successfully subscribed to all topics")
        else:
            self.log.error("Failed to subscribe to topics")

    def on_message(self, client, userdata, msg):
        """
        Receiver for messages

        Parses topics and extracts data
        """
        # self.log.debug("Received MQTT message from topic %s" % msg.topic)

        if msg.payload == "CK":
            self.log.debug("Received CK msg from %s" % str(msg.topic) )
            topic = str(msg.topic).split('/')
            nodeID = topic[topic.index("node") + 1]

            if nodeID not in self.nodes:
                self.nodes.append(nodeID)
            return

        topic = str(msg.topic).split('/')
        metric = topic[-1]

        nodeID = topic[topic.index("node") + 1]

        # data[1] timestamp
        # data[0] value
        data = str(msg.payload).split(';')

        self.on_receive(nodeID, metric, data)

        try:
            if metric in self.db:
                if nodeID in self.db[metric]:
                    # We already have a previous value there, calculate WMA
                    value = self.db[metric][nodeID]["value"] * (1.0 - self.alfa) + float(data[0]) * self.alfa
                else:
                    # There was no previous data received, just insert the value
                    value = float(data[0])

                self.db[topic[-1]][nodeID] = {
                        "value" : value,
                        "timestamp" : data[1]
                    }

            else:
                self.log.debug("New metric found: %s" % topic[-1])
                self.db[topic[-1]] = {
                        nodeID : {
                                "value" : float(data[0]),
                                "timestamp" : data[1]
                            },
                        "max" : float(data[0]),
                        "min" : float(data[0])
                        }

            value = self.db[topic[-1]][nodeID]["value"]

            if value > self.db[topic[-1]]["max"]:
                self.db[topic[-1]]["max"] = value

            elif value < self.db[topic[-1]]["min"]:
                self.db[topic[-1]]["min"] = value

            self.on_store(nodeID, metric, self.db[metric][nodeID])

        except Exception as e:
            self.log.error(str(e))
            raise

    def minmax(self, metric):
        return({
                'min' : self.db[metric]['min'],
                'max' : self.db[metric]['max']
            })

    def default_on_store(self, nodeID, metric, payload):
        pass

    def default_on_receive(self, nodeID, metric, payload):
        pass
