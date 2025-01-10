

function RoomDetected({ room }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 transition duration-300 ease-in-out hover:shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Patient is currently in the</h2>
      <p className="text-3xl font-bold text-green-600">{room}</p>
    </div>
  );
}

export default RoomDetected;
