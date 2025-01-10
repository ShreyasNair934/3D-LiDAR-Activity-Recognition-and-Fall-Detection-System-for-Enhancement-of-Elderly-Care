

function PatientInfo({ patientId, patientAge, room }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 transition duration-300 ease-in-out hover:shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Patient Information</h2>
      <div className="space-y-2">
        <p className="text-gray-600 text-xl">ID: <span className=" text-xl font-semibold text-gray-800">{patientId}</span></p>
        <p className="text-gray-600 text-xl">Age: <span className=" text-xl font-semibold text-gray-800">{patientAge} years</span></p>
        <p className="text-gray-600 text-xl">Current Room: <span className=" text-xl font-semibold text-gray-800">{room}</span></p>
      </div>
    </div>
  );
}

export default PatientInfo;
