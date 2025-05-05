import asyncio
from gmqtt import Client as MQTTClient

BROKER = 'mqtt-broker'
TOPIC = 'sensors/temperature'

client = MQTTClient("plc-1")

def on_connect(client, flags, rc, properties):
    print("PLC connected to MQTT broker")
    client.subscribe(TOPIC)

def on_message(client, topic, payload, qos, properties):
    print(f"PLC received from {topic}: {payload.decode()}°C")

client.on_connect = on_connect
client.on_message = on_message

async def main():
    await client.connect(BROKER)
    await asyncio.Event().wait()  # Keep it running

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
