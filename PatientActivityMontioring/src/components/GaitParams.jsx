function GaitParams({ metrics }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 transition duration-300 ease-in-out hover:shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Gait Parameters</h2>
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-gray-100 p-4 rounded-lg">
          <p className="text-sm font-medium text-gray-500 mb-1">Step Length</p>
          <p className="text-xl font-bold text-gray-800">0.98</p>
          <p className="text-xs text-gray-500">metres</p>
        </div>
        <div className="bg-gray-100 p-4 rounded-lg">
          <p className="text-sm font-medium text-gray-500 mb-1">
            Stride Length
          </p>
          <p className="text-xl font-bold text-gray-800">1.99</p>
          <p className="text-xs text-gray-500">metres</p>
        </div>
        <div className="bg-gray-100 p-4 rounded-lg">
          <p className="text-sm font-medium text-gray-500 mb-1">Cadence</p>
          <p className="text-xl font-bold text-gray-800">110</p>
          <p className="text-xs text-gray-500">steps/min</p>
        </div>
      </div>
    </div>
  );
}

export default GaitParams;
