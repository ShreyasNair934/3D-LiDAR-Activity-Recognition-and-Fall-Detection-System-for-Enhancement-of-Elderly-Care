import json
import time
import random
import logging
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder

# AWS IoT Core settings
ENDPOINT = "us-east-1.amazonaws.com"
CLIENT_ID = "lidarEdgeDevice"
PATH_TO_CERT = "lidar_edge_device.cert.pem"
PATH_TO_KEY = "lidar_edge_device.private.key"
PATH_TO_ROOT = "root-CA.crt"
TOPIC = "lidar/data"

logging.basicConfig(level=logging.DEBUG)

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERT,
    pri_key_filepath=PATH_TO_KEY,
    client_bootstrap=client_bootstrap,
    ca_filepath=PATH_TO_ROOT,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30
)

print(f"Connecting to {ENDPOINT} with client ID '{CLIENT_ID}'...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

def generate_lidar_data():
    activities = ["walking", "standing", "sitting", "fallen"]
    rooms = ["living_room", "kitchen", "bedroom"]
    activity = random.choice(activities)
    room = random.choice(rooms)
    
    return {
        "patientId": f"patient_10",  
        "timestamp": int(time.time()),
        "patientAge": random.randint(60, 90),
        "activityDetected": activity,
        "room": room, 
        "stepLength": round(random.uniform(0.5, 1.0), 2) if activity == "walking" else None,
        "strideLength": round(random.uniform(1.0, 2.0), 2) if activity == "walking" else None,
        "cadence": round(random.uniform(80, 120), 2) if activity == "walking" else None,
        "activityDuration": round(random.uniform(1, 60), 2)  # Duration in seconds
    }

try:
    while True:
        data = generate_lidar_data()
        message = json.dumps(data)
        mqtt_connection.publish(
            topic=TOPIC,
            payload=message,
            qos=mqtt.QoS.AT_LEAST_ONCE
        )
        print(f"Published: {message}")
        time.sleep(5)  # Send data every 5 seconds
except KeyboardInterrupt:
    print("Stopping the simulator...")
finally:
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")