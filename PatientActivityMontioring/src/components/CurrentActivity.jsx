function CurrentActivity({ activity, duration, timestamp, currentTime }) {
  const isFallen = activity.toLowerCase() === "fallen";
  const displayActivity = isFallen ? "Patient has fallen down!" : activity;
  const currentTimeSeconds = currentTime / 1000;

  return (
    <div
      className={`rounded-lg shadow-md p-6 transition duration-300 ease-in-out hover:shadow-lg 
                    ${isFallen ? "bg-red-600" : "bg-white"}`}
    >
      <h2
        className={`text-2xl font-bold mb-4 ${
          isFallen ? "text-white" : "text-gray-800"
        }`}
      >
        Current Activity
      </h2>
      <p
        className={`text-3xl font-bold mb-2 ${
          isFallen ? "text-white" : "text-blue-600"
        }`}
      >
        {displayActivity}
      </p>
      <p className={`${isFallen ? "text-red-100" : "text-gray-600"}`}>
        Duration:{" "}
        <span
          className={`font-semibold ${
            isFallen ? "text-white" : "text-gray-800"
          }`}
        >
          {duration.toFixed(2)} seconds
        </span>
      </p>
      <p className={`${isFallen ? 'text-red-100' : 'text-gray-600'}`}>
        Latency: <span className={`font-semibold ${isFallen ? 'text-white' : 'text-gray-800'}`}>
          {(currentTimeSeconds - timestamp).toFixed(2)} seconds
          
        </span>
      </p>
      {isFallen && (
        <div className="mt-4 bg-red-700 text-white p-3 rounded-md animate-pulse">
          <p className="font-bold">FALL DETECTED</p>
          <p className="text-sm">Immediate attention required!</p>
        </div>
      )}
    </div>
  );
}

export default CurrentActivity;
