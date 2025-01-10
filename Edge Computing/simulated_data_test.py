import argparse
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
import json
import random
import traceback

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--endpoint', required=True)
parser.add_argument('--ca_file', required=True)
parser.add_argument('--cert', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--client_id', required=True)
parser.add_argument('--topic', required=True)
parser.add_argument('--count', type=int, default=0)
parser.add_argument('--verbosity', choices=[x.name for x in io.LogLevel], default=io.LogLevel.NoLogs.name,
                    help='Logging level')

args = parser.parse_args()

io.init_logging(getattr(io.LogLevel, args.verbosity), 'stderr')

received_count = 0
received_all_event = threading.Event()

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print(f"Connection interrupted. error: {error}")

# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print(f"Connection resumed. return_code: {return_code} session_present: {session_present}")

# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print(f"Received message from topic '{topic}': {payload}")
    global received_count
    received_count += 1
    if args.count != 0 and received_count >= args.count:
        received_all_event.set()

# Generate simulated LIDAR data
def generate_lidar_data():
    activities = ["walking", "standing", "sitting", "fallen"]
    activity = random.choice(activities)
    return {
        "timestamp": int(time.time()),
        "activity": activity,
        "position_x": random.uniform(0, 10),
        "position_y": random.uniform(0, 10),
        "position_z": random.uniform(0, 3) if activity != "fallen" else random.uniform(0, 0.5)
    }

if __name__ == '__main__':
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    proxy_options = None
    credentials_provider = auth.AwsCredentialsProvider.new_default_chain(client_bootstrap)

    mqtt_connection = mqtt_connection_builder.websockets_with_default_aws_signing(
        endpoint=args.endpoint,
        client_bootstrap=client_bootstrap,
        region="us-east-1",
        credentials_provider=credentials_provider,
        http_proxy_options=proxy_options,
        ca_filepath=args.ca_file,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=args.client_id,
        clean_session=False,
        keep_alive_secs=30)

    print(f"Connecting to {args.endpoint} with client ID '{args.client_id}'...")
    connect_future = mqtt_connection.connect()
    connect_future.result()
    print("Connected!")

    # Subscribe
    print(f"Subscribing to topic '{args.topic}'...")
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=args.topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)

    subscribe_result = subscribe_future.result()
    print(f"Subscribed with {str(subscribe_result['qos'])}")

    # Publish messages
    try:
        while True:
            lidar_data = generate_lidar_data()
            message = json.dumps(lidar_data)
            print(f"Publishing message to topic '{args.topic}': {message}")
            mqtt_connection.publish(
                topic=args.topic,
                payload=message,
                qos=mqtt.QoS.AT_LEAST_ONCE)
            time.sleep(5)
    except Exception as e:
        print(f"Exception occurred: {e}")
        print(traceback.format_exc())
    finally:
        print("Disconnecting...")
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected!")