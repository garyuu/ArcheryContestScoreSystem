import mqtt_client as mqtt

def on_message(client, userdata, message):
    print("message")

c = mqtt.create(on_message)
mqtt.publish(c, "GGININ")

