import open3d as o3d
import numpy as np
from tqdm import tqdm
import os
import glob
import json
import time
import random
import logging
import sys
import select
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
from metrics_class import LatencyMeasurement

# AWS IoT Core settings
ENDPOINT = "us-east-1.amazonaws.com"
CLIENT_ID = "lidarEdgeDevice"
PATH_TO_CERT = "lidar_edge_device.cert.pem"
PATH_TO_KEY = "lidar_edge_device.private.key"
PATH_TO_ROOT = "root-CA.crt"
TOPIC = "lidar/data"


INPUT_DIR = "lidar_data"  

logging.basicConfig(level=logging.DEBUG)


ACTIVITIES = {
    "Walking": 300, 
    "Standing": 180,  
    "Sitting": 600,  
    "Sleeping": 1800,  
    "Fallen": 60  
}


def downsampling_function(pcd, voxel_size=0.05, num_points=4096):
    print("Applying voxel downsampling...")
    downsampled_pcd = pcd.voxel_down_sample(voxel_size)
    if len(downsampled_pcd.points) > num_points:
        points = np.asarray(downsampled_pcd.points)
        indices = np.random.choice(points.shape[0], num_points, replace=False)
        downsampled_pcd = downsampled_pcd.select_by_index(indices)

    return downsampled_pcd

def noise_removal_function(pcd):
    print("Applying noise removal...")
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    pcd_noise_removed = pcd.select_by_index(ind)
    return pcd_noise_removed

def ground_plane_removal(pcd, distance_threshold=0.02):
    print("Removing ground plane...")
    plane_model, inliers = pcd.segment_plane(distance_threshold=distance_threshold,
                                             ransac_n=3,
                                             num_iterations=1000)
    ground_plane_removed_pcd = pcd.select_by_index(inliers, invert=True)
    return ground_plane_removed_pcd

def point_cloud_normalisation(pcd):
    print("Normalizing point cloud by centering and scaling...")
    points = np.asarray(pcd.points)
    
    
    centroid = np.mean(points, axis=0)
    centered_points = points - centroid
    
   
    max_distance = np.max(np.linalg.norm(centered_points, axis=1))
    normalized_points = centered_points / max_distance
    
    normalized_pcd = o3d.geometry.PointCloud()
    normalized_pcd.points = o3d.utility.Vector3dVector(normalized_points)
    
    return normalized_pcd

def data_preprocessing_function(file_path):
    pcd = o3d.io.read_point_cloud(file_path)

    noise_removed_pcd = noise_removal_function(pcd)

    ground_plane_removed_pcd = ground_plane_removal(noise_removed_pcd)

    downsampled_pcd = downsampling_function(ground_plane_removed_pcd)

    normalized_pcd = point_cloud_normalisation(downsampled_pcd)

    return normalized_pcd


def patient_monitoring_data(activity):
    rooms = ["Living Room", "Kitchen", "Bedroom"]
    room = random.choice(rooms)
    return {
        "patientId": f"patient_10",
        "timestamp": int(time.time()),
        "patientAge": 78,
        "activityDetected": activity,
        "room": room,
        "stepLength": round(random.uniform(0.5, 1.0), 2) if activity == "walking" else None,
        "strideLength": round(random.uniform(1.0, 2.0), 2) if activity == "walking" else None,
        "cadence": round(random.uniform(80, 120), 2) if activity == "walking" else None,
        "activityDuration": round(random.uniform(1, 60), 2) 
    }

def check_for_input():
    if select.select([sys.stdin], [], [], 0.0)[0]:
        line = sys.stdin.readline().strip()
        return line
    return None

def main():
    # Set up MQTT connection
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

    ply_files = sorted(glob.glob(os.path.join(INPUT_DIR, '*.ply')))
    print(f"Found {len(ply_files)} PLY files in {INPUT_DIR}")

    activity_name = list(ACTIVITIES.keys())
    activity_index = random.randint(0, 4)
    activity_start_time = time.time()
    fall_probability = 0.01  

    print("Simulation started. Press Ctrl+C to stop.")
    print("Press f to simulate a fall event.")

    measure_latency = LatencyMeasurement()


    try:
        while True:
            
            start_time = time.time()
            user_input = check_for_input()
            if user_input and user_input.lower() == 'f':
                current_activity = "Fallen"
                activity_index = activity_name.index(current_activity)
                activity_start_time = time.time()
                print("\nManual fall event triggered!")

            # Simulate deep learning model inference
            file_path = random.choice(ply_files)
            processed_pcd = data_preprocessing_function(file_path)
            current_activity = activity_name[activity_index]
            elapsed_time = time.time() - activity_start_time
            data = patient_monitoring_data(current_activity)
            message = json.dumps(data)
            mqtt_connection.publish(
                topic=TOPIC,
                payload=message,
                qos=mqtt.QoS.AT_LEAST_ONCE
            )
            print(f"\rCurrent activity: {current_activity}. Elapsed time: {elapsed_time:.2f}s", flush=True)
            print(" ")

            
            if elapsed_time >= ACTIVITIES[current_activity] or (user_input and user_input.lower()) == 'a':
                activity_index = (activity_index + 1) % len(activity_name)
                activity_start_time = time.time()
                print(f"\nChanging activity to: {activity_name[activity_index]}")

            # Simulate a random fall event
            if current_activity != "Fallen" and random.random() < fall_probability:
                current_activity = "Fallen"
                activity_start_time = time.time()
                print("\nRandom fall event occurred!")
            
            end_to_end_latency = measure_latency.measure_end_to_end_latency(start_time)
            print(f"End-to-end latency: {end_to_end_latency:.2f} ms")

            # print(f"Current timestamp: {int(time.time())}")
            # print(f"Current date and time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
            

            
            time.sleep(2)  

    except KeyboardInterrupt:
        print("\nStopping program execution...")
    finally:
        print("Disconnecting...")
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected!")

if __name__ == "__main__":
    main()