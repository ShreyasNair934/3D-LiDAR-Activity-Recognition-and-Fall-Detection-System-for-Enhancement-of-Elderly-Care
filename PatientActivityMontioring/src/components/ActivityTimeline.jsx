function ActivityTimeline({ activities }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 transition duration-300 ease-in-out hover:shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">
        Activity Timeline
      </h2>
      <ul className="space-y-3">
        {activities.map((activity, index) => (
          <li
            key={index}
            className="flex justify-between items-center bg-gray-50 p-3 rounded-md"
          >
            <span className="font-medium text-gray-800">
              {activity.activityDetected}
            </span>
            <span className="text-sm text-gray-500">
              {new Date(activity.timestamp * 1000).toLocaleTimeString()}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ActivityTimeline;
