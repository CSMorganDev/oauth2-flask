import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribe to topics upon successful connection
    client.subscribe("topic_name")  # Subscribe to a single topic
    # client.subscribe([("topic1", 0), ("topic2", 1)])  # Subscribe to multiple topics with QoS levels


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


# Create an MQTT client instance
client = mqtt.Client()

# Set up callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect("broker_address", 1883, 60)  # Replace "broker_address" with your broker's address

# Start the MQTT client loop
client.loop_start()

# Publish a message
client.publish("topic_name", "Hello, MQTT!")  # Replace "topic_name" with the topic you want to publish to

# Continue doing other tasks or sleep for some time

# To unsubscribe from a topic
# client.unsubscribe("topic_name")

# To disconnect from the broker
# client.disconnect()