from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt


print("🚀 app.py has started")
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

MQTT_BROKER = "mqtt-broker"  # Docker Compose hostname
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/temperature"


@app.route("/")
def index():
    return render_template("index.html")


# MQTT callbacks
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"[MQTT] Connected with reason code {reason_code}")
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    temperature = msg.payload.decode()
    print(f"[MQTT] Received: {temperature}")
    socketio.emit("temperature_update", {"value": temperature})
    print(f"📤 Emitted temperature_update: {temperature}")


def on_disconnect(client, userdata, rc):
    print(f"[MQTT] Disconnected with result code {rc}")


def start_mqtt():
    print("🚀 Initializing MQTT Client...")
    mqtt_client = mqtt.Client(client_id="dashboard", protocol=mqtt.MQTTv5)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.reconnect_delay_set(min_delay=1, max_delay=120)
    import time
    for i in range(10):
        try:
            mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            break
        except Exception as e:
            print(f"⚠️ MQTT connection failed (try {i+1}/10): {e}")
            time.sleep(2)

    mqtt_client.loop_start()
    return mqtt_client


if __name__ == "__main__":
    print("📡 Starting dashboard service...")
    mqtt_client = start_mqtt()
    socketio.run(app, host="0.0.0.0", port=5000)
