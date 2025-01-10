// eslint-disable-next-line no-unused-vars
import React, { useEffect, useState } from "react";
import { generateClient } from "aws-amplify/api";
import { Amplify } from "aws-amplify";
import config from "../aws-exports";
import PatientInfo from "./PatientInfo";
import CurrentActivity from "./CurrentActivity";
import GaitParams from "./GaitParams";
import ActivityTimeline from "./ActivityTimeline";
import RoomDetected from "./RoomDetected";

const LIST_LIDAR_PATIENT_MONITORING = `
  query ListLidarPatientMonitorings($limit: Int) {
    listLidarPatientMonitorings(limit: $limit) {
      items {
        patientId
        timestamp
        patientAge
        activityDetected
        room
        stepLength
        strideLength
        cadence
        activityDuration
      }
    }
  }
`;

const ON_CREATE_LIDAR_PATIENT_MONITORING = `
  subscription OnCreateLidarPatientMonitoring {
    onCreateLidarPatientMonitoring {
      patientId
      timestamp
      patientAge
      activityDetected
      room
      stepLength
      strideLength
      cadence
      activityDuration
    }
  }
`;

Amplify.configure(config);
const client = generateClient();

function PatientDashboard() {
  const [apiStatus, setApiStatus] = useState("Connecting to API...");
  const [lidarData, setLidarData] = useState([]);
  const [currentActivity, setCurrentActivity] = useState({
    activity: "",
    duration: 0,
    timestamp: 0,
  });
  const [walkingMetrics, setWalkingMetrics] = useState({
    stepLength: 0,
    strideLength: 0,
    cadence: 0,
  });
  const [currentTime, setCurrentTime] = useState(Date.now());

  useEffect(() => {
    fetchLidarData();
    const subscription = subscribeToLidarData();
    return () => {
      subscription.unsubscribe();
    };
  });

  const fetchLidarData = async () => {
    try {
      const result = await client.graphql({
        query: LIST_LIDAR_PATIENT_MONITORING,
        variables: { limit: 10 },
      });
      const items = result.data.listLidarPatientMonitorings.items;
      const sortedItems = items.sort((a, b) => b.timestamp - a.timestamp);
      setLidarData(sortedItems);
      setCurrentTime(Date.now());
      setApiStatus("Connected");
      if (sortedItems.length > 0) {
        updateCurrentActivity(sortedItems[0]);
      }
    } catch (error) {
      setApiStatus("Error connecting to API");
      console.error("Error fetching LIDAR data:", error);
    }
  };

  const subscribeToLidarData = () => {
    return client
      .graphql({ query: ON_CREATE_LIDAR_PATIENT_MONITORING })
      .subscribe({
        next: ({ data }) => {
          const newData = data.onCreateLidarPatientMonitoring;
          setLidarData((prevData) => [newData, ...prevData].slice(0, 10));
          updateCurrentActivity(newData);
        },
        error: (error) => console.error("Subscription error:", error),
      });
  };

  const updateCurrentActivity = (newData) => {
    setCurrentActivity({
      activity: newData.activityDetected,
      duration: newData.activityDuration,
      timestamp: newData.timestamp,
    });
    setWalkingMetrics({
      stepLength: newData.stepLength || 0,
      strideLength: newData.strideLength || 0,
      cadence: newData.cadence || 0,
    });
  };

  const latestData = lidarData.length > 0 ? lidarData[0] : null;
  console.log(currentTime);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center">
      <div className="w-full max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl sm:text-4xl font-bold text-gray-800 mb-6 text-center">
          LiDAR Patient Monitoring Dashboard
        </h1>
        <p className="text-lg text-gray-600 mb-6 text-center">
          API Status:{" "}
          <span
            className={`font-semibold ${
              apiStatus === "Connected" ? "text-green-600" : "text-red-600"
            }`}
          >
            {apiStatus}
          </span>
        </p>

        {latestData ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <PatientInfo
              patientId={latestData.patientId}
              patientAge={latestData.patientAge}
              room={latestData.room}
            />
            <CurrentActivity
              activity={currentActivity.activity}
              duration={currentActivity.duration}
              timestamp={currentActivity.timestamp}
              currentTime={currentTime}
            />
            <GaitParams metrics={walkingMetrics} />
            <RoomDetected room={latestData.room} />
            <div className="md:col-span-2">
              <ActivityTimeline activities={lidarData} />
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <p className="text-xl text-gray-600">Loading patient data...</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default PatientDashboard;
